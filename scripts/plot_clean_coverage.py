"""Plot verified clean-corpus coverage from the published counts."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/cleaning_2026-09-15'
assert json.loads((OUT/'final_validation.json').read_text())['status']=='passed'
rows=list(csv.DictReader((OUT/'field_period_counts.csv').open()))
names={int(r['field_id']):r['field_name'] for r in csv.DictReader((OUT/'field_summary.csv').open())}
cells={(int(r['field_id']),int(r['period_start'])):int(r['total']) for r in rows}
fields=list(range(11,37));periods=list(range(2000,2025,5))
matrix=np.array([[cells[(f,p)] for p in periods] for f in fields])
assert matrix.sum()==500000
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(11,11),layout='constrained')
fig.get_layout_engine().set(rect=(0,.045,1,.94))
img=ax.imshow(matrix,cmap='Blues',norm=LogNorm(vmin=matrix.min(),vmax=matrix.max()),aspect='auto')
ax.set_yticks(range(26),[names[f] for f in fields]);ax.set_xticks(range(5),[f'{p}–{p+4}' for p in periods])
ax.xaxis.tick_top();ax.tick_params(axis='both',length=0)
for i in range(26):
    for j in range(5):ax.text(j,i,f'{matrix[i,j]:,}'.replace(',','.'),ha='center',va='center',fontsize=9,color='white' if matrix[i,j]>matrix.max()*.35 else '#17283b')
ax.set_title('Corpus limpio · 500.000 trabajos',loc='left',pad=30,weight='bold',fontsize=17)
fig.colorbar(img,ax=ax,shrink=.5,label='Trabajos (escala logarítmica)')
fig.text(.01,.006,'400.000 base general + 100.000 complemento. Casos dudosos conservados y marcados.\nEl conjunto completo refuerza áreas pequeñas; la base general conserva el reparto proporcional.',fontsize=9,color='#555555')
fig.savefig(OUT/'field_period_coverage.png',dpi=180);fig.savefig(OUT/'field_period_coverage.pdf');plt.close(fig)
print('Figura final guardada.')
