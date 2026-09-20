"""Fit Spanish headings in display tables without changing any data cells."""
from pathlib import Path
import re
D=Path(__file__).resolve().parents[1]/'tables/tex'
widths={'S04':[5.6,1.7,3,2.1,2.1], 'S06':[3,2.1,1.6,1.6,1.9,1.9,1.5],
'S07':[.65,2.7,2.7,3,2.6,2.8], 'S10':[4.2,1.7,2.2,2.2,2.2,2.2],
'S11':[5.4,1.3,2.3,1.8,4.3], 'S12':[3.5,3.4,1.2,1.5,2.5,2.6],
'S13':[4.7,2.25,2.55,2.7,2.5]}
for name,values in widths.items():
 p=D/(name+'.tex');text=p.read_text();assert len(re.findall(r'p\{[0-9.]+cm\}',text))==len(values)
 it=iter(values);text=re.sub(r'p\{[0-9.]+cm\}',lambda m:'p{'+str(next(it))+'cm}',text)
 text=text.replace('Arista máx./mediana','Arista máx. / mediana')
 p.write_text(text)
