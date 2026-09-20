"""Presentation of frozen final robustness results; no scientific computation."""
from pathlib import Path
import csv,json,hashlib,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import ScalarFormatter, FuncFormatter
BLUE,ORANGE,GREEN,GRAY='#0072B2','#D55E00','#009E73','#B7BDC3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def render(out):
 out=Path(out);root=out.parent;spanish=out.name=='manuscript_es';man={}
 def t(en,es):return es if spanish else en
 def read(item,name,source='reports/robustness_closure_v1/'):
  origin=root/source/name;dest=out/'figures/data'/item/name;dest.parent.mkdir(parents=True,exist_ok=True)
  if origin.exists():shutil.copyfile(origin,dest)
  with dest.open() as f:r=list(csv.DictReader(f))
  man.setdefault(item,{'sources':[],'displayed_values':{}})['sources'].append({'source':source+name,'included':str(dest.relative_to(out)),'sha256':sha(dest),'rows':len(r)})
  return r
 def save(item,fig):
  if spanish:
   for axis in fig.axes:
    for dimension in (axis.xaxis,axis.yaxis):
     if isinstance(dimension.get_major_formatter(),ScalarFormatter):
      dimension.set_major_formatter(FuncFormatter(lambda value,position:format(value,'g').replace('.',',')))
  paths=[]
  for ext in ['pdf','svg','png','tiff']:
   p=out/'figures'/f'{item}.{ext}';kw={'metadata':{'CreationDate':None}} if ext=='pdf' else {'metadata':{'Date':None}} if ext=='svg' else {'pil_kwargs':{'compression':'tiff_lzw'}} if ext=='tiff' else {}
   fig.savefig(p,dpi=300,**kw);paths.append(str(p.relative_to(out)))
  man[item]['files']=paths;man[item]['size_inches']=list(fig.get_size_inches());plt.close(fig)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'axes.titlesize':10,'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'sos-closure-v1','figure.facecolor':'white','savefig.facecolor':'white'})
 item='figure_01';summary=read(item,'centres_summary.csv');inner=read(item,'structure_matched_size_agreement.csv','reports/robustness_v2/final/tables/')
 fig,axes=plt.subplots(1,2,figsize=(6.8,3.8));fig.subplots_adjust(left=.09,right=.98,bottom=.30,top=.86,wspace=.47)
 designs=['repeat256_field','repeat256_subfield217','nested26'];x=np.arange(3)
 for off,typ,color,label in [(-.18,'observed',BLUE,t('Observed groups','Grupos observados')),(.18,'random',GRAY,t('Random groups','Grupos aleatorios'))]:
  r=[next(a for a in summary if a['design']==d and a['grouping']==typ) for d in designs];mean=np.array([float(a['mean']) for a in r]);lo=np.array([float(a['p025']) for a in r]);hi=np.array([float(a['p975']) for a in r]);axes[0].bar(x+off,mean,.34,color=color,label=label);axes[0].errorbar(x+off,mean,yerr=[mean-lo,hi-mean],fmt='none',ecolor='#303D49',capsize=3,elinewidth=1)
  man[item]['displayed_values'][typ]=r
 axes[0].set(xticks=x,xticklabels=t(['26 Field\ncentres','217 Subfield\ncentres','26 Subfield\ncentres'],['26\náreas','217\nespecial.','26\nespecial.']),ylim=(0,1),ylabel=t('Corrected CKA','CKA corregida'),title=t('A  Between group centres','A  Entre centros'))
 axes[0].legend(loc='upper left',bbox_to_anchor=(-.15,-.24),ncol=2,frameon=False,fontsize=7)
 spread=[]
 for level,label,color,off,marker in [('field',t('26 Fields','26 áreas'),BLUE,-.18,'o'),('subfield',t('Same 183 Subfields','Mismas 183 especialidades'),ORANGE,.18,'^')]:
  r=[next(a for a in inner if a['population']=='same_183_subfields' and a['recipe']=='mean' and a['level']==level and a['selection']==str(n) and a['measure']=='shape') for n in [128,256,512]];mean=[float(a['mean']) for a in r];lo=[float(a['p025']) for a in r];hi=[float(a['p975']) for a in r];y=np.arange(3)+off
  axes[1].hlines(y,lo,hi,color=color,lw=2,alpha=.55);axes[1].scatter(mean,y,color=color,marker=marker,s=27,label=label)
  for a,v,yy in zip(r,mean,y):axes[1].annotate(f'{v:.3f}'.replace('.',',') if spanish else f'{v:.3f}',(v,yy),xytext=(0,-10 if off>0 else 6),textcoords='offset points',ha='center',fontsize=6.6,color=color);spread.append(a)
 axes[1].set(yticks=range(3),yticklabels=['128','256','512'],ylim=(2.6,-.6),xlim=(0,1),xticks=[0,.2,.4,.6,.8,1],xlabel=t('Corrected CKA','CKA corregida'),ylabel=t('Articles per group','Artículos por grupo'),title=t('B  Within groups','B  Dentro de los grupos'));axes[1].legend(frameon=False,loc='upper left',bbox_to_anchor=(-.14,-.27),fontsize=6.5)
 for i,ax in enumerate(axes):ax.grid(axis='y' if i==0 else 'x',alpha=.15);ax.set_axisbelow(True)
 man[item]['displayed_values']['within_group_spread']=spread;save(item,fig)
 item='figure_04';rows=read(item,'morphology_classification.csv');fig,axes=plt.subplots(2,1,figsize=(6.8,4.75));fig.subplots_adjust(left=.24,right=.98,bottom=.18,top=.94,hspace=.57)
 for ax,metric,title in zip(axes,['angle_p50','pr'],[t('A  Angular spread','A  Apertura angular'),t('B  Effective linear dimension (PR)','B  Dimensión lineal efectiva (PR)')]):
  selected=[next(r for r in rows if r['metric']==metric and float(r['cutoff'])==cutoff and r['representation']==rep) for cutoff in [0,.05] for rep in ['original','global_centered']];left=np.zeros(4)
  for key,color in [('unanimous',BLUE),('contradiction',ORANGE),('unresolved',GRAY)]:
   vals=np.array([int(r[key]) for r in selected]);ax.barh(range(4),vals,left=left,color=color,height=.65)
   for y,(a,v) in enumerate(zip(left,vals)):
    if v>=9:ax.text(a+v/2,y,str(v),ha='center',va='center',fontsize=8,color='white' if key!='unresolved' else '#23313D')
   left+=vals
  assert np.all(left==325);ax.set(yticks=range(4),yticklabels=t(['0%  Original','0%  Centred','5%  Original','5%  Centred'],['0%  Original','0%  Centrada','5%  Original','5%  Centrada']),xlim=(0,325),xticks=[0,100,200,325],title=title);ax.invert_yaxis();ax.spines[['left','bottom']].set_visible(False);ax.tick_params(length=0);man[item]['displayed_values'][metric]=selected
 axes[1].set_xlabel(t('Field pairs (325 for each property)','Parejas de áreas (325 por propiedad)'))
 fig.legend(handles=[Patch(color=c,label=l) for c,l in [(BLUE,t('All ten agree','Acuerdo de los diez')),(ORANGE,t('Persistent opposition','Oposición persistente')),(GRAY,t('Unresolved','Sin resolver'))]],loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.015));save(item,fig)
 item='figure_S11';rows=read(item,'centres_summary.csv');head=read(item,'headline_grand_repetitions.csv');fig,axes=plt.subplots(1,2,figsize=(6.8,3.8));fig.subplots_adjust(left=.10,right=.97,bottom=.27,top=.87,wspace=.55)
 values=[]
 for lv,color,label in [('field',BLUE,t('26 Fields','26 áreas')),('subfield183',ORANGE,t('183 Subfields','183 especialidades'))]:
  for typ,style in [('observed','-'),('random','--')]:
   r=[next(a for a in rows if a['design']==f'size{n}_{lv}' and a['grouping']==typ) for n in [128,256,512]];v=np.array([float(a['mean']) for a in r]);lo=np.array([float(a['p025']) for a in r]);hi=np.array([float(a['p975']) for a in r]);axes[0].plot(range(3),v,style,color=color,marker='o',ms=3,label=label if typ=='observed' else None);axes[0].fill_between(range(3),lo,hi,color=color,alpha=.1);values+=r
 axes[0].set(xticks=range(3),xticklabels=['128','256','512'],ylim=(0,1),ylabel=t('Corrected CKA','CKA corregida'),xlabel=t('Articles per centre','Artículos por centro'),title=t('A  Centre size','A  Tamaño de los centros'));axes[0].legend(frameon=False,fontsize=7,loc='lower left');axes[0].text(.5,-.28,t('Solid: observed; dashed: random','Continua: observados; discontinua: aleatorios'),transform=axes[0].transAxes,ha='center',fontsize=6.7)
 hdata=[]
 for i,(recipe,k) in enumerate([('mean',10),('mean',25),('mean',50),('cls',25),('sep',25)]):
  r=[a for a in head if a['recipe']==recipe and int(a['k'])==k];v=np.array([float(a['title_minus_model'])*100 for a in r]);assert len(v)==50;axes[1].scatter(i+np.linspace(-.10,.10,50),v,s=8,color=BLUE if recipe=='mean' else ORANGE,alpha=.5);axes[1].plot([i-.20,i+.20],[np.median(v)]*2,color='#23313D',lw=1.5);hdata+=r
 axes[1].axhline(0,color='#70777D',lw=.8);axes[1].set(xticks=range(5),xticklabels=t(['Main\nk10','Main\nk25','Main\nk50','CLS\nk25','SEP\nk25'],['Base\nk10','Base\nk25','Base\nk50','CLS\nk25','SEP\nk25']),ylim=(-4,3),ylabel=t('Title-only minus model change\n(percentage points)','Solo título menos cambio de modelo\n(puntos porcentuales)'),title=t('B  Text versus model','B  Texto frente a modelo'));axes[1].text(.5,-.28,t('Each point: one of 50 selections','Cada punto: una de 50 selecciones'),transform=axes[1].transAxes,ha='center',fontsize=7)
 for ax in axes:ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
 man[item]['displayed_values']={'centres':values,'headline':hdata};save(item,fig)
 p=out/'figures/manifest.json';old=json.loads(p.read_text()) if p.exists() else {};old.update(man);p.write_text(json.dumps(old,indent=2,ensure_ascii=False)+'\n');return man
if __name__=='__main__':render(Path(__file__).resolve().parents[1])
