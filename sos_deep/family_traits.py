"""Separate documented traits without pretending this ten-model panel isolates causes."""
import itertools
import json
import numpy as np
from sos_deep.artifacts import ROOT,save_csv,verify_audit,freeze,finish
from sos_followup.existing_analysis_v2 import build_arrays
from sos_embed.storage import file_sha,write_json,run_lock

CONFIG=ROOT/'config/family_traits_v2.json';D=json.loads(CONFIG.read_text());OUT=ROOT/D['output']
BASE=json.loads((ROOT/'config/analysis_v1.json').read_text());MODELS=list(BASE['poolings'])
PAIRS=list(itertools.combinations(MODELS,2));I,J=np.triu_indices(10,1)


def identified_fit(x,y):
    rank=int(np.linalg.matrix_rank(x));coef=np.linalg.lstsq(x,y,rcond=None)[0]
    pred=x@coef;sst=np.sum((y-y.mean())**2)
    return {'rank':rank,'columns':x.shape[1],'identified':rank==x.shape[1],
            'coefficients':coef if rank==x.shape[1] else None,'predictions':pred,
            'r_squared':float(1-np.sum((y-pred)**2)/sst) if sst else None}


def profiles():
    rows=[];paths=[];traits={}
    for m in json.loads((ROOT/'config/embeddings_v1.json').read_text())['models']:
        folder=ROOT/'.benchmark-models'/('models--'+m['repo_id'].replace('/','--'))/'snapshots'/m['revision']
        c=json.loads((folder/'config.json').read_text());t=dict(D['traits'][m['key']])
        arch=f"{c['model_type']}:{c['num_hidden_layers']}:{c['hidden_size']}:{c['num_attention_heads']}"
        # Adapter status stays visible, never silently equated to the backbone dimensions.
        t['architecture']=arch;t['adapter']=bool(m.get('adapter'));traits[m['key']]=t
        row={'model':m['key'],**t,'revision':m['revision'],'repo_id':m['repo_id'],'vocab_size':c['vocab_size'],
             'primary_pooling':BASE['poolings'][m['key']],'config_sha256':file_sha(folder/'config.json'),
             'vocab_sha256':file_sha(folder/'vocab.txt'),'source_url':'https://huggingface.co/'+m['repo_id']+'/tree/'+m['revision']}
        rows.append(row);paths.extend([str((folder/n).relative_to(ROOT)) for n in ['config.json','vocab.txt']])
    return traits,rows,paths


def matrix(traits,recipe):
    rows=[]
    for a,b in PAIRS:
        t,u=traits[a],traits[b]
        pooling={m:(recipe if m in ['bert','scibert','biobert','pubmedbert'] else BASE['poolings'][m]) for m in MODELS}
        rows.append([1.,float(t['architecture']==u['architecture']),float(t['lineage']==u['lineage']),
                     float(t['final_corpus_group']==u['final_corpus_group']),float(t['objective']==u['objective']),
                     float(t['domain']==u['domain']),float(pooling[a]==pooling[b])])
    return np.array(rows)


def main():
    with run_lock(OUT):
        verify_audit(ROOT/'data/checklist_v1/existing_v2');traits,profile,paths=profiles()
        freeze(OUT,['sos_deep/family_traits.py','sos_deep/artifacts.py','config/family_traits_v2.json',
                    'sos_followup/existing_analysis_v2.py'],
               ['config/embeddings_v1.json','data/checklist_v1/existing_v2/audit.json',*paths],D)
        save_csv(OUT/'model_traits.csv',profile)
        arrays=build_arrays();coefs=[];loo=[];marginals=[];ranks=[];designs=[];reference=[];predictions=[]
        perms=np.array([np.random.default_rng(D['seed']+i).permutation(10) for i in range(D['permutations'])])
        for outcome in ['cka_primary','cka_equal2048','cka_quality','cka_cls','cka_sep',
                        'neighbors_2048_mean_k25','neighbors_2048_cls_k25','neighbors_2048_sep_k25']:
            recipe='cls' if outcome=='cka_cls' or '_cls_' in outcome else ('sep' if outcome=='cka_sep' or '_sep_' in outcome else 'mean')
            x=matrix(traits,recipe);y=arrays[outcome].mean((0,1));fit=identified_fit(x,y)
            names=['intercept',*D['features']]
            ranks.append({'outcome':outcome,'recipe':recipe,'rank':fit['rank'],'columns':len(names),
                          'identified':fit['identified'],'condition_number':float(np.linalg.cond(x)),
                          'r_squared':fit['r_squared']})
            for j,name in enumerate(names):
                coefs.append({'outcome':outcome,'feature':name,'coefficient':float(fit['coefficients'][j]) if fit['identified'] else None,
                              'identified':fit['identified'],'rank':fit['rank'],'columns':len(names)})
                if j:
                    mask=x[:,j].astype(bool)
                    marginals.append({'outcome':outcome,'feature':name,'same_pairs':int(mask.sum()),
                        'different_pairs':int((~mask).sum()),'same_mean':float(y[mask].mean()) if mask.any() else None,
                        'different_mean':float(y[~mask].mean()) if (~mask).any() else None,
                        'difference':float(y[mask].mean()-y[~mask].mean()) if mask.any() and (~mask).any() else None})
            for z,pair in enumerate(PAIRS):
                designs.append({'outcome':outcome,'model_a':pair[0],'model_b':pair[1],**dict(zip(names,map(float,x[z])))})
                predictions.append({'outcome':outcome,'model_a':pair[0],'model_b':pair[1],
                    'observed':float(y[z]),'descriptive_fit':float(fit['predictions'][z]),'residual':float(y[z]-fit['predictions'][z])})
            for m in MODELS:
                keep=np.array([m not in pair for pair in PAIRS]);other=identified_fit(x[keep],y[keep])
                for j,name in enumerate(names):
                    loo.append({'outcome':outcome,'omitted_model':m,'feature':name,'rank':other['rank'],
                        'columns':len(names),'identified':other['identified'],
                        'coefficient':float(other['coefficients'][j]) if other['identified'] else None,
                        'r_squared':other['r_squared']})
            mat=np.eye(10);mat[I,J]=y;mat[J,I]=y;yp=mat[perms[:,I],perms[:,J]]
            beta=yp@np.linalg.pinv(x).T;prediction=beta@x.T
            r2=1-((yp-prediction)**2).sum(1)/((yp-yp.mean(1,keepdims=True))**2).sum(1)
            reference.append({'outcome':outcome,'permutations':len(perms),'observed_r_squared':fit['r_squared'],
                'reference_fraction_ge_observed':float((1+(r2>=fit['r_squared']).sum())/(1+len(r2))),
                'interpretation':'Model-label permutation reference, not causal inference or 45 independent pairs'})
            np.save(OUT/(outcome+'_permutation_r2.npy'),r2,allow_pickle=False)
        for name,rows in [('coefficients',coefs),('leave_one_model',loo),('marginal_associations',marginals),
                          ('identifiability',ranks),('design',designs),('permutation_reference',reference),('pair_residuals',predictions)]:
            save_csv(OUT/(name+'.csv'),rows)
        finish(OUT,models=10,pairs=45,outcomes=len(ranks),verified_configurations=True,
               rank_checked_every_fit=True,unidentified_coefficients_null=True,architecture_corpus_objective_domain_separate=True)
        print('EXPANDED FAMILY TRAITS COMPLETE',flush=True)


if __name__=='__main__':main()
