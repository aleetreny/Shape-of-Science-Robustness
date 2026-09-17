"""Render final coverage and diagnostic language disagreements; no scientific filtering."""
import csv
from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/corpus_audit_2026-09-15'
names={int(r['field_id']):r['field_name'] for r in csv.DictReader((ROOT/'FIELD_COUNTS.csv').open())}
db=sqlite3.connect((ROOT/'data/corpus_audit/audit.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
ld=sqlite3.connect((ROOT/'data/corpus_audit/language.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
assert db.execute('SELECT count(*) FROM selected').fetchone()[0]==500000
assert ld.execute('SELECT count(*) FROM predictions').fetchone()[0]==500000
fields=list(range(11,37));periods=list(range(2000,2025,5))
cells={(f,p):n for f,p,n in db.execute('SELECT field_id,period_start,count(*) FROM selected GROUP BY 1,2')}
base=dict(db.execute("SELECT field_id,count(*) FROM selected WHERE cohort='base' GROUP BY 1"))
extra=dict(db.execute("SELECT field_id,count(*) FROM selected WHERE cohort='extra' GROUP BY 1"))
language={f:(n,k) for f,n,k in ld.execute("SELECT field_id,count(*),sum(abstract_language!='en') FROM predictions GROUP BY 1")}
table=[]
for field in fields:
    n,k=language[field]
    table.append([field,names[field],base.get(field,0),extra.get(field,0),n,
                  min(cells[(field,p)] for p in periods),k,round(k/n*100,4)])
with (OUT/'field_summary.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['field_id','field_name','base','extra','total','minimum_period','non_en_top_label','non_en_top_label_pct']);w.writerows(table)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
matrix=np.array([[cells[(f,p)] for p in periods] for f in fields])
fig,ax=plt.subplots(figsize=(11,11),layout='constrained')
fig.get_layout_engine().set(rect=(0,0.03,1,0.97))
img=ax.imshow(matrix,cmap='Blues',norm=LogNorm(vmin=matrix.min(),vmax=matrix.max()),aspect='auto')
ax.set_yticks(range(26),[names[f] for f in fields]);ax.set_xticks(range(5),[f'{p}–{p+4}' for p in periods])
ax.xaxis.tick_top();ax.tick_params(axis='both',length=0)
for i in range(26):
    for j in range(5):
        ax.text(j,i,f'{matrix[i,j]:,}'.replace(',','.'),ha='center',va='center',fontsize=9,
                color='white' if matrix[i,j]>matrix.max()*.35 else '#17283b')
ax.set_title('500.000 trabajos · 26 áreas y cinco períodos',loc='left',pad=30,weight='bold',fontsize=16)
fig.colorbar(img,ax=ax,shrink=.5,label='Trabajos (escala logarítmica)')
fig.text(.01,.003,'Base general + complemento. Recuento previo a las decisiones de limpieza adicional.',fontsize=9,color='#555555')
fig.savefig(OUT/'field_period_coverage.png',dpi=180);fig.savefig(OUT/'field_period_coverage.pdf');plt.close(fig)
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(14,11),sharey=True,gridspec_kw={'width_ratios':[2,1]},layout='constrained')
fig.get_layout_engine().set(rect=(0,0.03,1,0.97))
ordered=sorted(fields,key=lambda f:base.get(f,0)+extra.get(f,0))
ys=range(len(ordered));b=np.array([base.get(f,0) for f in ordered]);e=np.array([extra.get(f,0) for f in ordered])
ax1.barh(ys,b,color='#526d82',label='Base general');ax1.barh(ys,e,left=b,color='#eaaa51',label='Complemento')
ax1.set_yticks(ys,[names[f] for f in ordered]);ax1.set_xlabel('Número de trabajos');ax1.legend(frameon=False)
rates=[100*language[f][1]/language[f][0] for f in ordered]
ax2.barh(ys,rates,color='#a14642');ax2.set_xlabel('% señalado por el detector de idioma')
ax1.set_title('Reparto del corpus',loc='left',weight='bold');ax2.set_title('Posible abstract fuera del inglés',loc='left',weight='bold')
fig.suptitle('Cobertura y control de idioma',fontsize=17,weight='bold')
fig.text(.01,.003,'Idioma: primera etiqueta de fastText distinta de inglés. Son alertas diagnósticas, no errores confirmados ni descartes.',fontsize=9,color='#555555')
fig.savefig(OUT/'field_coverage_and_language.png',dpi=180);plt.close(fig)
db.close();ld.close()
print('Recuentos por Field y figuras guardados.')
