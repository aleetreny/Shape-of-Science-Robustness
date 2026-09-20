"""Descriptive comparisons and presentation, separate from frozen calculations."""
import csv
import itertools
import json
from pathlib import Path
import warnings
import numpy as np
import pyarrow.parquet as pq
from scipy.stats import spearmanr, rankdata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sos_embed.storage import file_sha, write_json, utcnow

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/morphology_pilot_v1'
OUT=ROOT/'reports/morphology_pilot_v1'
DESIGN=json.loads((ROOT/'config/morphology_pilot_v1.json').read_text())
MODELS=list(DESIGN['models']);FIELDS=DESIGN['fields']
METRICS=['angle_p50','pr','gap_25']
LABELS={'angle_p50':'Apertura angular (grados)','pr':'Direcciones efectivas (PR)',
        'gap_25':'Fuerza de conexión (k=25)'}
NAMES={'specter':'SPECTER','specter2':'SPECTER2','scincl':'SciNCL','scibert':'SciBERT',
       'bert':'BERT','mpnet':'MPNet','minilm':'MiniLM','pubmedbert':'PubMedBERT','biobert':'BioBERT','simcse':'SimCSE'}


def save_csv(name,rows):
    if not rows:raise ValueError(name)
    cols=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/(name+'.csv')).open('w') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)


def corr(a,b):
    if np.ptp(a)<1e-12 or np.ptp(b)<1e-12:return None
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');v=float(spearmanr(a,b).statistic)
    return v if np.isfinite(v) else None


def describe(vals):
    a=np.array([x for x in vals if x is not None],dtype=float)
    if not len(a):return {'n':0,'median':None,'min':None,'q10':None,'q90':None,'max':None}
    return {'n':len(a),'median':float(np.median(a)),'min':float(a.min()),'q10':float(np.quantile(a,.1)),
            'q90':float(np.quantile(a,.9)),'max':float(a.max())}


def decomposition(matrix):
    g=matrix.mean();rm=matrix.mean(1,keepdims=True);cm=matrix.mean(0,keepdims=True)
    ss=float(np.sum((matrix-g)**2))
    parts=[float(matrix.shape[1]*np.sum((rm-g)**2)),float(matrix.shape[0]*np.sum((cm-g)**2)),
           float(np.sum((matrix-rm-cm+g)**2))]
    assert abs(sum(parts)-ss)<max(ss,1)*1e-9
    return dict(zip(['model_share','field_share','interaction_share'],[s/ss for s in parts]))


def figure(name,fig):
    for ext in ['png','pdf','svg']:fig.savefig(OUT/(name+'.'+ext),dpi=180,bbox_inches='tight')
    plt.close(fig)


def main():
    audit=json.loads((DATA/'audit.json').read_text());assert audit['all_complete']
    for n,h in audit['files'].items():assert file_sha(DATA/n)==h,n
    OUT.mkdir(exist_ok=True,parents=True)
    rows=pq.read_table(DATA/'metrics.parquet').to_pylist()
    rows=[{k:v for k,v in r.items() if v is not None} for r in rows]
    index={(r['model'],r['kind'],r['field_id'],r['repeat'],r['period'],r['n']):r for r in rows}
    assert len(index)==len(rows)
    def get(m,k,f,rep=0,p=0,n=None):
        if n is None:
            n=2000 if k in ['primary','external','common','common_native','minilm512','global'] else 400 if k=='period' else 200 if k=='period_half' else 950 if k.startswith('trim_') else 1000
        return index[m,k,f,rep,p,n]
    names={r['field_id']:r['field_display_name'] for r in pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet',columns=['field_id','field_display_name']).to_pylist()}
    primary=[dict(get(m,'primary',f),field_name=names[f]) for m in MODELS for f in FIELDS]
    save_csv('primary_metrics',primary)
    matrices={metric:np.array([[get(m,'primary',f)[metric] for f in FIELDS] for m in MODELS]) for metric in METRICS}
    model_summary=[];field_summary=[];pair_ranks=[];decomps=[]
    for metric,mat in matrices.items():
        ranks=np.stack([rankdata(x,method='average') for x in mat])
        for i,m in enumerate(MODELS):
            model_summary.append({'metric':metric,'model':m,'mean':float(mat[i].mean()),'median':float(np.median(mat[i])),
                'min_field':float(mat[i].min()),'max_field':float(mat[i].max()),'global_mixture':get(m,'global',0)[metric]})
        for j,f in enumerate(FIELDS):
            field_summary.append({'metric':metric,'field_id':f,'field_name':names[f],'min_model_value':float(mat[:,j].min()),
                'max_model_value':float(mat[:,j].max()),'median_rank':float(np.median(ranks[:,j])),
                'min_rank':float(ranks[:,j].min()),'max_rank':float(ranks[:,j].max()),'rank_range':float(np.ptp(ranks[:,j]))})
        for i,j in itertools.combinations(range(10),2):
            pair_ranks.append({'metric':metric,'model_a':MODELS[i],'model_b':MODELS[j],'field_rank_spearman':corr(mat[i],mat[j])})
        decomps.append({'metric':metric,'condition':'primary','scale':'native units',**decomposition(mat)})
        decomps.append({'metric':metric,'condition':'omit_MiniLM','scale':'native units',**decomposition(np.delete(mat,MODELS.index('minilm'),axis=0))})
        if metric=='pr':decomps.append({'metric':metric,'condition':'primary','scale':'log(PR)',**decomposition(np.log(mat))})
        baseline=np.array([get(m,'global',0)[metric] for m in MODELS])
        if np.all(baseline>1e-9):
            calibrated=mat/baseline[:,None]
            decomps.append({'metric':metric,'condition':'relative_to_global_mixture','scale':'ratio',**decomposition(calibrated)})
        else:
            decomps.append({'metric':metric,'condition':'relative_to_global_mixture','scale':'undefined: zero reference',
                            'model_share':None,'field_share':None,'interaction_share':None})
    save_csv('model_summary',model_summary);save_csv('field_summary',field_summary)
    save_csv('between_model_field_ranks',pair_ranks);save_csv('descriptive_decomposition',decomps)

    stability=[];size=[];rank_stability=[]
    for metric in METRICS:
        width_limit=DESIGN['stability']['relative_width_screen'][metric]
        bias_limit=DESIGN['stability']['median_size_change_screen'][metric]
        for m in MODELS:
            for f in FIELDS:
                ref=get(m,'primary',f)[metric]
                for kind,count in [('half',20),('external',5)]:
                    values=np.array([get(m,kind,f,rep)[metric] for rep in range(count)])
                    low,high=np.quantile(values,[.05,.95]);med=float(np.median(values))
                    denom=max(abs(ref),1e-9)
                    width=float((high-low)/denom);shift=abs(med-ref)/denom
                    stability.append({'metric':metric,'model':m,'field_id':f,'field_name':names[f],'kind':kind,
                        'repeats':count,'reference_n':2000,'reference':ref,'median':med,'q05':float(low),'q95':float(high),
                        'relative_width':width,'relative_median_shift':shift,'passes_width':width<=width_limit,
                        'passes_shift':shift<=bias_limit,'passes_both':width<=width_limit and shift<=bias_limit})
                for n in [500,1000,2000,4000]:
                    val=get(m,'size',f,n=n)[metric] if n in [500,4000] else get(m,'half' if n==1000 else 'primary',f)[metric]
                    size.append({'metric':metric,'model':m,'field_id':f,'n':n,'value':val,'reference':ref,'relative_to_2000':val/max(ref,1e-9)})
            for kind,count in [('half',20),('external',5)]:
                ref=[get(m,'primary',f)[metric] for f in FIELDS]
                for rep in range(count):
                    vals=[get(m,kind,f,rep)[metric] for f in FIELDS]
                    rank_stability.append({'metric':metric,'kind':kind,'model':m,'repeat':rep,'field_rank_spearman':corr(ref,vals)})
    save_csv('selection_stability',stability);save_csv('sample_size',size);save_csv('rank_stability',rank_stability)
    fraction=[]
    for m in MODELS:
        for f in FIELDS:
            for small,large in [(500,1000),(1000,2000),(2000,4000)]:
                a=get(m,'size',f,n=small) if small==500 else get(m,'half' if small==1000 else 'primary',f)
                b=get(m,'size',f,n=large) if large==4000 else get(m,'half' if large==1000 else 'primary',f)
                fraction.append({'model':m,'field_id':f,'small_n':small,'large_n':large,
                    'small_gap25':a['gap_25'],'large_gap25':b['gap_25'],'large_gap50':b['gap_50'],
                    'relative_change_fixed_k':(b['gap_25']-a['gap_25'])/max(a['gap_25'],1e-9),
                    'relative_change_approximately_fixed_fraction':(b['gap_50']-a['gap_25'])/max(a['gap_25'],1e-9),
                    'small_neighbor_fraction':25/(small-1),'large_neighbor_fraction':50/(large-1)})
    save_csv('connectivity_fixed_fraction',fraction)

    alternatives=[('angle_p50','angle_p10',1),('angle_p50','angle_p90',1),('angle_p50','center_angle_p50',1),
                  ('pr','erank',1),('pr','d80',1),('pr','pc1_share',-1),('gap_25','gap_10',1),('gap_25','gap_50',1),
                  ('gap_25','weighted_gap_25',1),('gap_25','mutual_giant_25',1),('gap_25','connect_ratio90_50',-1),
                  ('gap_25','connect_r90',-1),('gap_25','mst_max_median',-1)]
    coherence=[]
    for main,alt,sign in alternatives:
        for m in MODELS:
            coherence.append({'main':main,'alternative':alt,'comparison':'Fields within model','unit':m,
                'spearman_oriented':corr([get(m,'primary',f)[main] for f in FIELDS],[sign*get(m,'primary',f)[alt] for f in FIELDS])})
        for f in FIELDS:
            coherence.append({'main':main,'alternative':alt,'comparison':'models within Field','unit':f,
                'spearman_oriented':corr([get(m,'primary',f)[main] for m in MODELS],[sign*get(m,'primary',f)[alt] for m in MODELS])})
    save_csv('alternative_metric_agreement',coherence)

    comparisons=[('title','half'),('abstract','half'),('global_centered','half'),('quality','half'),
                 ('trim_extreme','trim_random'),('pool_cls','half'),('pool_sep','half'),('common','common_native'),('minilm512','primary')]
    contrasts=[];control_ranks=[]
    for condition,refkind in comparisons:
        models=DESIGN['controls']['word_bert_models'] if condition.startswith('pool_') else ['minilm'] if condition=='minilm512' else MODELS
        for metric in METRICS:
            for m in models:
                refvals=[];newvals=[]
                for f in FIELDS:
                    a=get(m,refkind,f);b=get(m,condition,f);assert a['n']==b['n']
                    if condition not in ['quality','trim_extreme']:assert a['selection_sha256']==b['selection_sha256']
                    av=a[metric];bv=b[metric];refvals.append(av);newvals.append(bv)
                    contrasts.append({'metric':metric,'model':m,'field_id':f,'condition':condition,'reference_kind':refkind,'n':a['n'],
                        'reference':av,'value':bv,'difference':bv-av,'relative_difference':(bv-av)/max(abs(av),1e-9),
                        'same_ids':a['selection_sha256']==b['selection_sha256']})
                control_ranks.append({'metric':metric,'model':m,'condition':condition,'field_rank_spearman':corr(refvals,newvals)})
    save_csv('paired_controls',contrasts);save_csv('control_rank_stability',control_ranks)
    panel_agreement=[]
    for panel in ['primary','half','title','abstract','pool_cls','pool_sep','common_native','common','global_centered','quality']:
        for metric in METRICS:
            vectors=[]
            for m in MODELS:
                kind=panel
                if panel in ['pool_cls','pool_sep'] and m not in DESIGN['controls']['word_bert_models']:kind='half'
                vectors.append([get(m,kind,f)[metric] for f in FIELDS])
            for i,j in itertools.combinations(range(10),2):
                panel_agreement.append({'panel':panel,'metric':metric,'model_a':MODELS[i],'model_b':MODELS[j],
                    'field_rank_spearman':corr(vectors[i],vectors[j])})
    save_csv('panel_field_rank_agreement',panel_agreement)
    cases=[]
    for field,metrics in [(35,['angle_p50','angle_p10','angle_p90','center_angle_p50']),(21,['pr','erank','d80'])]:
        for panel in ['primary','half','title','abstract','pool_cls','pool_sep','common','quality','global_centered']:
            for metric in metrics:
                for m in MODELS:
                    kind='half' if panel in ['pool_cls','pool_sep'] and m not in DESIGN['controls']['word_bert_models'] else panel
                    vector=[get(m,kind,f)[metric] for f in FIELDS]
                    cases.append({'field_id':field,'field_name':names[field],'metric':metric,'panel':panel,'model':m,
                                  'rank_1_is_smallest':float(rankdata(vector)[FIELDS.index(field)]),
                                  'selection':'illustrative cases selected after results: smallest worst-model rank for main spread/dimension'})
    save_csv('illustrative_case_checks',cases)
    reversals=[]
    for m in ['specter','bert']:
        for metric in ['angle_p50','angle_p10','angle_p90','center_angle_p50']:
            a=get(m,'primary',12)[metric];b=get(m,'primary',27)[metric]
            row={'model':m,'metric':metric,'arts_humanities':a,'medicine':b,'medicine_minus_arts':b-a}
            if metric=='angle_p50':
                for kind,count in [('half',20),('external',5)]:
                    changes=[get(m,kind,27,r)[metric]-get(m,kind,12,r)[metric] for r in range(count)]
                    row[kind+'_same_direction_count']=sum(np.sign(x)==np.sign(b-a) for x in changes)
                    row[kind+'_total']=count
            reversals.append(row)
    save_csv('illustrative_reversal',reversals)
    input_model=[]
    for metric in METRICS:
        for m in MODELS:
            for f in FIELDS:
                base=get(m,'half',f)[metric]
                changed_model=np.mean([abs(get(other,'half',f)[metric]-base) for other in MODELS if other!=m])
                for cond in ['title','abstract']:
                    changed_input=abs(get(m,cond,f)[metric]-base)
                    input_model.append({'metric':metric,'model':m,'field_id':f,'condition':cond,'model_difference_mean9':float(changed_model),
                        'input_difference':changed_input,'model_minus_input':float(changed_model-changed_input)})
    save_csv('input_vs_model',input_model)

    null=[]
    for m in MODELS:
        for f in FIELDS:
            ref=get(m,'half',f)
            for rep in range(3):
                val=get(m,'gaussian',f,rep)
                null.append({'model':m,'field_id':f,'repeat':rep,
                    **{k+'_observed':ref[k] for k in ['angle_p50','pr','gap_25','connect_ratio90_50']},
                    **{k+'_gaussian':val[k] for k in ['angle_p50','pr','gap_25','connect_ratio90_50']},
                    'gap_excess_observed_minus_reference':ref['gap_25']-val['gap_25'],
                    'spread_reference_relative_error':val['angle_p50']/ref['angle_p50']-1,
                    'pr_reference_relative_error':val['pr']/ref['pr']-1})
    save_csv('gaussian_reference_diagnostics',null)

    temporal=[];temporal_points=[]
    for metric in METRICS:
        for m in MODELS:
            for f in FIELDS:
                first=get(m,'period',f,p=2000)[metric];last=get(m,'period',f,p=2020)[metric]
                change=last-first
                draws=np.array([get(m,'period_half',f,rep,p=2020)[metric]-get(m,'period_half',f,rep,p=2000)[metric] for rep in range(10)])
                temporal.append({'metric':metric,'model':m,'field_id':f,'first':first,'last':last,'change':change,
                    'half_sample_median_change':float(np.median(draws)),'half_q05':float(np.quantile(draws,.05)),
                    'half_q95':float(np.quantile(draws,.95)),'same_sign_repeats':int(np.sum(np.sign(draws)==np.sign(change)))})
                for p in DESIGN['periods']:
                    temporal_points.append({'metric':metric,'model':m,'field_id':f,'period':p,'value':get(m,'period',f,p=p)[metric]})
    save_csv('temporal_endpoints',temporal);save_csv('temporal_points',temporal_points)

    geometry=[]
    with (ROOT/'data/robustness_v2/input_comparisons/shape.csv').open() as stream:
        cka=list(csv.DictReader(stream))
    for metric in METRICS:
        for f in FIELDS:
            pairs=[r for r in cka if int(r['field_id'])==f and r['input_a']==r['input_b']=='title_abstract' and r['kind']=='model']
            assert len(pairs)==45
            dv=[abs(get(r['model_a'],'primary',f)[metric]-get(r['model_b'],'primary',f)[metric]) for r in pairs]
            ds=[1-float(r['cka_debiased']) for r in pairs]
            geometry.append({'metric':metric,'field_id':f,'spearman_absolute_morphology_difference_vs_1_CKA':corr(dv,ds),'dependent_model_pairs':45})
    save_csv('relation_to_CKA',geometry)

    # Summary contains no inferential p-values or automatic success narrative.
    summary={'generated_at':utcnow(),'metric_sets':len(rows),'primary_cells':len(primary),
        'primary_ranges':{k:describe([r[k] for r in primary]) for k in METRICS},
        'between_model_field_ranks':{k:describe([r['field_rank_spearman'] for r in pair_ranks if r['metric']==k]) for k in METRICS},
        'decomposition':decomps,'stability':[], 'alternative_agreement':[], 'control_ranks':[],
        'connectivity':{'union25_fully_connected':sum(r['union_giant_25']==1 for r in primary),
            'union10_fully_connected':sum(r['union_giant_10']==1 for r in primary),
            'union50_fully_connected':sum(r['union_giant_50']==1 for r in primary),
            'mutual25_giant':describe([r['mutual_giant_25'] for r in primary]),
            'zero_distance_pairs_max':max(r['zero_distance_pairs'] for r in primary)},
        'gaussian_reference':{k:describe([r[k] for r in null]) for k in ['spread_reference_relative_error','pr_reference_relative_error','gap_excess_observed_minus_reference']},
        'temporal':[],'source_audit_sha256':file_sha(DATA/'audit.json')}
    for metric in METRICS:
        for kind in ['half','external']:
            ss=[r for r in stability if r['metric']==metric and r['kind']==kind]
            summary['stability'].append({'metric':metric,'kind':kind,'passes_both':sum(r['passes_both'] for r in ss),'total':len(ss),
                'relative_width':describe([r['relative_width'] for r in ss]),'relative_median_shift':describe([r['relative_median_shift'] for r in ss]),
                'field_rank_spearman':describe([r['field_rank_spearman'] for r in rank_stability if r['metric']==metric and r['kind']==kind])})
        tt=[r for r in temporal if r['metric']==metric]
        summary['temporal'].append({'metric':metric,'positive_endpoint':sum(r['change']>0 for r in tt),
            'negative_endpoint':sum(r['change']<0 for r in tt),'same_sign_at_least9of10':sum(r['same_sign_repeats']>=9 for r in tt),'total':len(tt)})
    for main,alt,sign in alternatives:
        for scope in ['Fields within model','models within Field']:
            ss=[r['spearman_oriented'] for r in coherence if r['main']==main and r['alternative']==alt and r['comparison']==scope]
            summary['alternative_agreement'].append({'main':main,'alternative':alt,'scope':scope,**describe(ss)})
    for cond,_ in comparisons:
        for metric in METRICS:
            summary['control_ranks'].append({'condition':cond,'metric':metric,
                **describe([r['field_rank_spearman'] for r in control_ranks if r['metric']==metric and r['condition']==cond])})
    write_json(OUT/'summary.json',summary)

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
        'figure.facecolor':'white','axes.titlepad':13,'svg.fonttype':'none','pdf.fonttype':42})
    colors=['#315c88','#326b5a','#ac5b2b']
    fig,axes=plt.subplots(1,3,figsize=(14,5.3))
    for ax,(metric,mat),color in zip(axes,matrices.items(),colors):
        for i,m in enumerate(MODELS):
            q=np.quantile(mat[i],[.25,.5,.75]);ax.plot(q[[0,2]],[i,i],color=color,linewidth=3,alpha=.65);ax.scatter(q[1],i,color=color,s=34,zorder=3)
        ax.set_yticks(range(10),[NAMES[m] for m in MODELS]);ax.invert_yaxis();ax.set_xlabel(LABELS[metric]);ax.grid(axis='x',alpha=.2)
    fig.suptitle('Los mismos artículos producen descripciones distintas',fontsize=17,y=1.01)
    fig.text(.5,-.035,'2.000 artículos por área · puntos: mediana entre 26 áreas · barras: mitad central de las áreas, no intervalos de confianza',ha='center',fontsize=10)
    fig.tight_layout();figure('01_model_properties',fig)

    fig,axes=plt.subplots(1,2,figsize=(14,10.5))
    for ax,metric,title in zip(axes,['angle_p50','pr'],['Orden por apertura','Orden por direcciones efectivas']):
        ranks=np.stack([rankdata(x) for x in matrices[metric]])
        im=ax.imshow(ranks.T,vmin=1,vmax=26,cmap='viridis',aspect='auto')
        ax.set_xticks(range(10),[NAMES[m] for m in MODELS],rotation=55,ha='right')
        ax.set_yticks(range(26),[names[f] for f in FIELDS]);ax.set_title(title)
        fig.colorbar(im,ax=ax,shrink=.65,label='Posición dentro de cada modelo (26 = valor mayor)')
    fig.suptitle('¿Las áreas quedan en el mismo orden al cambiar de modelo?',fontsize=16,y=1.01)
    fig.tight_layout();figure('02_field_rank_maps',fig)

    fig,axes=plt.subplots(1,3,figsize=(14,4.4))
    palette=plt.get_cmap('tab10')
    for ax,metric in zip(axes,METRICS):
        for i,m in enumerate(MODELS):
            vals=[np.median([r['relative_to_2000'] for r in size if r['model']==m and r['metric']==metric and r['n']==n]) for n in [500,1000,2000,4000]]
            ax.plot([500,1000,2000,4000],100*(np.array(vals)-1),marker='o',ms=3,label=NAMES[m],color=palette(i))
        ax.axhline(0,color='gray',ls='--',lw=1);ax.set_xscale('log',base=2);ax.set_xticks([500,1000,2000,4000],['500','1.000','2.000','4.000'])
        ax.set_xlabel('Artículos por área');ax.set_ylabel('Cambio frente a 2.000 artículos (%)');ax.set_title(LABELS[metric]);ax.grid(alpha=.2)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=5,bbox_to_anchor=(.5,-.13),frameon=False)
    fig.suptitle('Qué cambia al variar el tamaño de muestra',fontsize=15,y=1.14)
    fig.text(.5,1.025,'Cada panel usa su propia escala vertical · en conexión se mantienen 25 vecinos, no su proporción',ha='center',fontsize=10)
    fig.tight_layout();figure('03_sample_size',fig)

    sim=list(csv.DictReader((DATA/'synthetic/clouds.csv').open()))
    simnames={'one_round':'Una nube redonda','one_narrow':'Una nube estrecha','one_wide':'Una nube abierta','one_elongated':'Una nube alargada','low_rank':'Una nube, pocas direcciones','two_separated':'Dos grupos separados','four_separated':'Cuatro grupos separados','two_with_bridges':'Dos grupos con puentes','one_with_outliers':'Una nube con extremos'}
    fig,axes=plt.subplots(1,3,figsize=(14,5.3))
    for ax,key,title in zip(axes,['gap_25','connect_ratio90_50','mst_max_median'],['Fuerza de conexión\n(menor: enlace más débil)','Radio 90% / radio 50%\n(mayor: conexión más tardía)','Arista máxima / mediana\n(mayor: salto más grande)']):
        ax.barh(range(9),[float(r[key]) for r in sim],color=['#b76136' if r['cloud'] in ['one_elongated','low_rank','one_with_outliers'] else '#47738d' for r in sim]);ax.set_yticks(range(9),[simnames[r['cloud']] for r in sim]);ax.invert_yaxis();ax.set_title(title);ax.grid(axis='x',alpha=.15)
    fig.suptitle('Conexión débil no equivale siempre a grupos separados',fontsize=16,y=1.03)
    fig.tight_layout();figure('04_fragmentation_counterexamples',fig)

    fig,axes=plt.subplots(1,3,figsize=(14,4.4))
    kinds=['quality','common','abstract','title','pool_cls','pool_sep','global_centered']
    labels=['Marcas de calidad','Texto común','Solo resumen','Solo título','Cuatro BERT: CLS','Cuatro BERT: SEP','Quitar dirección global']
    for ax,metric,color in zip(axes,METRICS,colors):
        vals=[[r['field_rank_spearman'] for r in control_ranks if r['metric']==metric and r['condition']==kind and r['field_rank_spearman'] is not None] for kind in kinds]
        for j,v in enumerate(vals):
            ax.scatter(v,np.full(len(v),j),s=18,color=color,alpha=.7);ax.plot([min(v),max(v)],[j,j],color=color,alpha=.35)
        ax.set_yticks(range(len(kinds)),labels);ax.invert_yaxis();ax.set_xlim(-1.02,1.03);ax.axvline(.9,color='gray',ls='--',lw=1)
        ax.set_title(LABELS[metric]);ax.set_xlabel('Acuerdo del orden de las áreas');ax.grid(axis='x',alpha=.2)
    fig.suptitle('Qué decisiones conservan el orden de las áreas',fontsize=16,y=1.03);fig.tight_layout();figure('05_control_rank_agreement',fig)

    manifest={'created_at':utcnow(),'source_audit_sha256':file_sha(DATA/'audit.json'),'export_source_sha256':file_sha(Path(__file__)),
              'files':{str(p.relative_to(OUT)):file_sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='catalog.json'}}
    write_json(OUT/'catalog.json',manifest)
    print(json.dumps({k:summary[k] for k in ['metric_sets','primary_ranges','between_model_field_ranks','connectivity','stability','temporal']},indent=2))


if __name__=='__main__':main()
