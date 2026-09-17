"""Rebuild the expanded presentation from audited outputs, without inference."""
import json
import shutil
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
from sos_deep.artifacts import ROOT,read_csv,save_csv,verify_audit
from sos_embed.storage import file_sha,write_json,utcnow

BASE=ROOT/'data/robustness_v2';OUT=ROOT/'reports/robustness_v2/final'
STRUCT=BASE/'structural_review_v3';CONTROL=BASE/'control_review_v2';INPUT=BASE/'input_review'
BLUE='#2463a1';ORANGE='#d97a25';GREEN='#188775';RED='#be4c51';GRAY='#97a4b0'
MODELS=list(json.loads((ROOT/'config/analysis_v1.json').read_text())['poolings'])
LABELS=['SPECTER','SPECTER2','SciNCL','SciBERT','BERT','MPNet','MiniLM','PubMedBERT','BioBERT','SimCSE']


def savefig(name,fig):
    for extension in ['png','pdf','svg']:
        fig.savefig(OUT/'figures'/f'{name}.{extension}',dpi=180,bbox_inches='tight',facecolor='white')
    plt.close(fig)


def averages(rows,keys,value):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in keys)].append(float(r[value]))
    return {k:float(np.mean(v)) for k,v in groups.items()}


def input_figure():
    r=read_csv(INPUT/'input_effect_by_field.csv');fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    for ax,metric,title in zip(axes,['cka','neighbors25'],['Shape: 1 − corrected CKA','Local: fraction of 25 neighbors changed']):
        values=[]
        for cond,measure in [('title','model_change_at_full'),('title','input_change_from_full'),('abstract','input_change_from_full')]:
            values.append([float(x['mean']) for x in r if x['metric']==metric and x['input_condition']==cond and x['measure']==measure])
        ax.boxplot(values,positions=[0,1,2],widths=.5,showfliers=False,patch_artist=True,
                   boxprops={'facecolor':'#dfe9f1'},medianprops={'color':BLUE})
        for i,v in enumerate(values):ax.scatter(np.full(len(v),i)+np.linspace(-.13,.13,len(v)),v,s=15,color=[BLUE,ORANGE,GREEN][i],alpha=.65,zorder=3)
        ax.set_xticks([0,1,2],['Change model\n(full input)','Use title only','Use abstract only']);ax.set_title(title);ax.set_ylabel('Change');ax.grid(axis='y',alpha=.2)
    fig.suptitle('Model choice and text choice, on the same 52,000 articles',fontweight='bold')
    fig.supxlabel('Each dot is one Field averaged over the ten fixed models; spread is not a confidence interval.',fontsize=9)
    savefig('01_input_effect',fig)


def scale_figure():
    rows=read_csv(BASE/'centroid_scales/comparisons.csv');means=averages(rows,['condition','groups'],'cka_debiased')
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    # Conditions explicitly hold group sizes or number of centers as stated.
    names=['matched_field','matched_subfield','one_subfield_per_field'];labels=['26 Field centers','217 Subfield centers','26 Subfield centers']
    x=np.arange(3)
    for offset,kind,color in [(-.17,'real',BLUE),(.17,'null',GRAY)]:
        vals=[]
        for name in names:
            vals.append(means[(name,'real' if kind=='real' else 'random_period_preserved')])
        axes[0].bar(x+offset,vals,.34,label='Real groups' if kind=='real' else 'Random groups',color=color)
    axes[0].set_xticks(x,labels,rotation=16);axes[0].set_ylim(0,1);axes[0].set_ylabel('Corrected CKA');axes[0].set_title('Relations between group centers');axes[0].legend(fontsize=9,loc='upper center',bbox_to_anchor=(.5,-.25),ncol=2)
    r=read_csv(STRUCT/'matched_size_agreement.csv')
    for level,label,color in [('field','Fields',BLUE),('subfield','Same 183 Subfields',ORANGE)]:
        y=[float(next(a['mean'] for a in r if a['population']=='same_183_subfields' and a['recipe']=='mean'
                       and a['level']==level and a['selection']==str(n) and a['measure']=='shape')) for n in [128,256,512]]
        axes[1].plot([128,256,512],y,'o-',label=label,color=color)
    axes[1].set_xticks([128,256,512]);axes[1].set_ylim(.5,.75);axes[1].set_title('Relations between articles within groups');axes[1].set_xlabel('Articles per group');axes[1].set_ylabel('Corrected CKA');axes[1].legend(fontsize=9)
    fig.suptitle('A shared broad map does not imply identical local structure',fontweight='bold')
    fig.supxlabel('Left: 256 articles per center; random groups preserve dates and sizes. Right: fixed eligible groups.',fontsize=9)
    savefig('02_scales',fig)


def paired_figure():
    r=read_csv(STRUCT/'paired_scope_changes.csv');vals=averages([a for a in r if a['k']=='25'],['subfield_id','field_id'],'subfield')
    broad=averages([a for a in r if a['k']=='25'],['subfield_id','field_id'],'field')
    fig,ax=plt.subplots(figsize=(7,6),layout='constrained')
    for med,label,color in [(False,'Other Subfields',BLUE),(True,'Medicine Subfields',ORANGE)]:
        keys=[k for k in vals if (k[1]=='27')==med];ax.scatter([broad[k] for k in keys],[vals[k] for k in keys],s=30,alpha=.7,color=color,label=label)
    ax.plot([.25,.75],[.25,.75],'--',color=GRAY);ax.set(xlim=(.25,.75),ylim=(.25,.75),
        xlabel='Agreement searching within the parent Field',ylabel='Agreement searching within the Subfield',
        title='A closer view does not always reduce agreement')
    ax.legend();ax.set_aspect('equal');ax.grid(alpha=.15)
    fig.supxlabel('217 Subfields · same 50 query articles · 256 candidates · matched dates · mean of 10 selections · k=25',fontsize=8)
    savefig('03_paired_neighbors',fig)


def temporal_figure():
    rows=read_csv(BASE/'temporal_review/trajectories.csv');fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    years=[2000,2005,2010,2015,2020];x=np.arange(5)
    for ax,outcomes in [(axes[0],[('cka_equal2048',BLUE,'Corrected CKA, equal size')]),
                        (axes[1],[('neighbors_2048_mean_k25',GREEN,'2,048 candidates'),('neighbors_all_k25',ORANGE,'All candidates')])]:
        for outcome,color,label in outcomes:
            matrix=[]
            for f in range(11,37):
                selected=[r for r in rows if r['outcome']==outcome and r['field_id']==str(f)]
                matrix.append([np.mean([float(r['value_'+str(y)]) for r in selected]) for y in years])
            matrix=np.array(matrix);matrix-=matrix[:,[0]]
            if len(outcomes)==1:
                for line in matrix:ax.plot(x,line,color=color,alpha=.14,linewidth=.7)
            ax.plot(x,matrix.mean(0),'o-',color=color,label=label,linewidth=2.4)
        ax.axhline(0,color=GRAY,linewidth=.7);ax.set_xticks(x,['2000–04','2005–09','2010–14','2015–19','2020–24'],rotation=25)
        ax.set_ylabel('Change from 2000–04');ax.legend(fontsize=9);ax.grid(alpha=.15)
    axes[0].set_title('Shape: Fields vary');axes[1].set_title('Neighbors: candidate count changes the sign')
    fig.suptitle('Descriptive time patterns, with comparable search sets',fontweight='bold')
    fig.supxlabel('Equal weight for Fields and fixed model pairs. These are not causal historical trends.',fontsize=9)
    savefig('04_time_controls',fig)


def medicine_figure():
    rows=read_csv(STRUCT/'medicine_composition_summary.csv');fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    fields=['27','21','26','31'];labels=['Medicine','Energy*','Mathematics','Physics'];x=np.arange(4)
    cases=[('observed_eligible_composition','all','Observed / 10 models',BLUE),
           ('equal_subfield_composition','all','Balanced / 10 models',GREEN),
           ('observed_eligible_composition','without_biomedical','Observed / without biomedical',ORANGE),
           ('equal_subfield_composition','without_biomedical','Balanced / without biomedical',RED)]
    for ax,metric in zip(axes,['cka_debiased','neighbors_k25']):
        for j,(condition,group,label,color) in enumerate(cases):
            chosen=[next(r for r in rows if r['field_id']==f and r['condition']==condition and r['model_group']==group and r['metric']==metric) for f in fields]
            y=np.array([float(r['mean']) for r in chosen]);lo=np.array([float(r['min']) for r in chosen]);hi=np.array([float(r['max']) for r in chosen])
            ax.bar(x+(j-1.5)*.19,y,.18,label=label,color=color,yerr=[y-lo,hi-y],error_kw={'linewidth':.7,'capsize':2})
        ax.set_xticks(x,labels);ax.set_ylim(0,.9 if metric=='cka_debiased' else .4);ax.grid(axis='y',alpha=.15)
    axes[0].set_title('Shape: corrected CKA');axes[1].set_title('Neighbors: overlap at k=25');axes[1].legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.15),ncol=2)
    fig.suptitle('Medicine: balancing specialties does not remove its shape difference',fontweight='bold')
    fig.supxlabel('2,048 articles per Field, identical date quotas. Whiskers: range of 10 selections. *Energy has one eligible Subfield.',fontsize=8)
    savefig('05_medicine_composition',fig)


def family_figure():
    rows=read_csv(ROOT/'reports/analysis_v1/final/tables/shape_all_stages.csv');fig,axes=plt.subplots(1,3,figsize=(13,5.3),layout='constrained')
    for ax,stage,title in zip(axes,['primary','cls','sep'],['Mean (primary)','CLS control','SEP control']):
        groups=defaultdict(list)
        for r in rows:
            if r['stage']==stage:groups[r['model_a'].split('/')[0],r['model_b'].split('/')[0]].append(float(r['cka_debiased']))
        a=np.eye(10)
        for (m,n),values in groups.items():i=MODELS.index(m);j=MODELS.index(n);a[i,j]=a[j,i]=np.mean(values)
        im=ax.imshow(a,vmin=0,vmax=1,cmap='viridis');ax.set_xticks(range(10),LABELS,rotation=70,ha='right',fontsize=8);ax.set_yticks(range(10),LABELS,fontsize=8);ax.set_title(title)
    fig.colorbar(im,ax=axes,shrink=.7,label='Corrected CKA');fig.suptitle('Apparent model families depend on how word BERTs are summarized',fontweight='bold')
    fig.supxlabel('Only BERT, SciBERT, BioBERT and PubMedBERT change recipe. A shared trait is not an isolated causal effect.',fontsize=9)
    savefig('06_recipe_families',fig)


def alerts_figure():
    r=read_csv(INPUT/'alert_transition_counts.csv');fig,ax=plt.subplots(figsize=(8,4.6),layout='constrained')
    x=np.arange(2)
    for offset,size,color in [(-.17,'26k',ORANGE),(.17,'52k',BLUE)]:
        y=[int(next(a['alerts'+size] for a in r if a['scope']=='individual_models' and a['repeats']==str(rep))) for rep in [20,100]]
        b=ax.bar(x+offset,y,.32,label=size,color=color);ax.bar_label(b)
    ax.set_xticks(x,['20 selections (original comparison)','100 selections (additional check)']);ax.set_ylabel('Input contrasts flagged, out of 520');ax.legend();ax.set_ylim(bottom=0);ax.margins(y=.15)
    ax.set_title('Input stability under larger samples',fontweight='bold')
    fig.supxlabel('Same thresholds and nested samples. These are selection checks within a fixed corpus, not population confidence intervals.',fontsize=8)
    savefig('07_input_alerts',fig)


def subfield_time():
    shapes=read_csv(BASE/'subfield_controls/shape.csv');nb=read_csv(BASE/'subfield_controls/neighbors.csv');output=[]
    for metric,rows,column in [('cka',shapes,'cka_debiased')]+[(f'neighbors{k}',[r for r in nb if r['k']==str(k)],'mean_overlap') for k in [10,25,50]]:
        values=averages([r for r in rows if r['level']=='subfield_period' and r['recipe']=='mean'],['group','field_id','selection'],column)
        groups=sorted({k[:2] for k in values})
        for sf,field in groups:
            y=np.array([values[sf,field,str(year)] for year in [2000,2005,2010,2015,2020]])
            output.append({'metric':metric,'subfield_id':sf,'field_id':field,**{f'value_{year}':float(y[i]) for i,year in enumerate([2000,2005,2010,2015,2020])},
                           'endpoint_change':float(y[-1]-y[0]),'all_four_steps_increase':bool(np.all(np.diff(y)>0))})
        assert len(groups)==125
    save_csv(OUT/'tables/subfield_time_fixed128.csv',output)


def main():
    audit=verify_audit(BASE/'final_audit');OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'figures').mkdir(exist_ok=True);(OUT/'tables').mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'svg.fonttype':'none','pdf.fonttype':42})
    # Small summary tables are copied; large raw artifacts remain in their frozen locations.
    for prefix,folder in [('input',INPUT),('structure',STRUCT),('controls',CONTROL),
                          ('time',BASE/'temporal_review'),('families',BASE/'family_traits')]:
        for path in folder.glob('*.csv'):
            if path.stat().st_size<2_000_000:shutil.copyfile(path,OUT/'tables'/f'{prefix}_{path.name}')
    subfield_time()
    input_figure();scale_figure();paired_figure();temporal_figure();medicine_figure();family_figure();alerts_figure()
    summary={key:json.loads((folder/'summary.json').read_text()) for key,folder in
             [('input',INPUT),('structure',STRUCT),('controls',CONTROL),('provenance',BASE/'provenance'),('audit',BASE/'final_audit')]}
    summary['created_at']=utcnow();write_json(OUT/'summary.json',summary)
    (OUT/'source_snapshot').mkdir(exist_ok=True);shutil.copyfile(__file__,OUT/'source_snapshot/report.py')
    write_json(OUT/'catalog.json',{'created_at':utcnow(),'parent_audit_sha256':file_sha(BASE/'final_audit/audit.json'),
        'files':{str(p.relative_to(OUT)):file_sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['catalog.json','audit.json']}})
    write_json(OUT/'audit.json',{'all_complete':True,'figures':len(list((OUT/'figures').glob('*.pdf'))),
        'tables':len(list((OUT/'tables').glob('*.csv'))),'parent_scientific_audit_verified':True,
        'catalog_sha256':file_sha(OUT/'catalog.json'),'visual_review':'pending separate human-visible inspection'})
    print('EXPANDED REPORT EXPORTED',flush=True)


if __name__=='__main__':main()
