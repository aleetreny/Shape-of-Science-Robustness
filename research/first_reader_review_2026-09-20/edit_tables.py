from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
replacements={
'en':{
'T01':[
('Ten models: relations among area or specialty centres, and among individual papers inside groups.','Ten models: relationships between groups, summarised by their average positions, and between papers within groups.'),
('256 papers per centre; repeated choices and size checks at 128 and 512.','256 papers per group to calculate its centre; repeated choices and size checks at 128 and 512.'),
("The overlap between two models' lists of 25 neighbours.","How many of the 25 closest papers appear in both models' lists."),
('Which area has more spread or more directions of variation?','Do models agree on how papers spread within areas?'),
('Two geometric properties for all 325 pairs of areas, under ten models.','Angles between paper vectors and how their variation spreads across directions; all 325 area pairs under ten models.'),
('Models use the same paper IDs within each comparison.','Models use the same paper IDs within each comparison. Candidates are the papers available for a neighbour search.')],
'T02':[
('CLS, pre-pooler','CLS'),
('Vector size is the number of coordinates.','Vector size is the number of coordinates, not the number of words read.'),
('Limits count tokens including special symbols. Mean: last-layer average over non-padding positions, including special symbols. CLS: first-position state before the pooler; SPECTER2 adds its proximity adapter.','Limits count tokens, the pieces into which a model divides text, including its special symbols. Mean averages the final token outputs (the last layer), including special symbols and excluding empty padding positions. CLS uses the first-position output before the additional transformation called the pooler. SPECTER2 also uses its proximity adapter, an additional trained component.'),
('not the exact checkpoint training','not the exact training of these published versions')]
},
'es':{
'T01':[
('Diez modelos: relaciones entre centros de áreas o especialidades y entre artículos dentro de los grupos.','Diez modelos: relaciones entre grupos, resumidos por sus posiciones medias, y entre artículos dentro de los grupos.'),
('256 artículos por centro; elecciones repetidas y controles con 128 y 512.','256 artículos por grupo para calcular su centro; elecciones repetidas y controles con 128 y 512.'),
('Cuánto coinciden las listas de 25 vecinos de dos modelos.','Cuántos de los 25 artículos más cercanos aparecen en las listas de ambos modelos.'),
('Qué área tiene más dispersión o más direcciones de variación?','Coinciden los modelos sobre la dispersión dentro de áreas?'),
('Dos propiedades geométricas para las 325 parejas de áreas, con diez modelos.','Ángulos entre vectores de artículos y reparto de su variación entre direcciones; las 325 parejas de áreas, con diez modelos.'),
('Los modelos usan los mismos identificadores en cada comparación.','Los modelos usan los mismos identificadores en cada comparación. Los candidatos son los artículos disponibles para buscar vecinos.')],
'T02':[
('CLS, antes del pooler','CLS'),
('Tamaño indica cuántas coordenadas contiene el vector.','Tamaño indica cuántas coordenadas contiene el vector, no cuántas palabras lee el modelo.'),
('Los límites cuentan tokens, incluidos los símbolos especiales. Media: promedio de posiciones sin relleno de la última capa, con símbolos especiales. CLS: primera posición antes del pooler; SPECTER2 añade su adaptador de proximidad.','Los límites cuentan tokens, las piezas en que el modelo divide el texto, incluidos sus símbolos especiales. Media promedia las salidas finales de tokens (la última capa), con símbolos especiales y sin posiciones vacías de relleno. CLS usa la salida de la primera posición antes de la transformación adicional llamada pooler. SPECTER2 utiliza también su adaptador de proximidad, un componente adicional entrenado.')]
}}
for lang,folder in [('en','manuscript'),('es','manuscript_es')]:
 mpath=ROOT/folder/'tables/manifest.json';manifest=json.loads(mpath.read_text())
 for key,changes in replacements[lang].items():
  p=ROOT/folder/f'tables/editorial/{key}.tex';s=(HERE/'baseline'/folder/f'tables/editorial/{key}.tex').read_text()
  for old,new in changes:assert old in s,(lang,key,old);s=s.replace(old,new)
  if key=='T01':s=r'\begin{table}[!htbp]'+'\n'+s+r'\end{table}'+'\n'
  p.write_text(s);(ROOT/folder/f'tables/tex/{key}.tex').write_text(s)
  manifest[key]['editorial_source']['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  manifest[key]['summary_rule']='Full first-reader revision requested by the author, 20 September 2026. Explanations and terminology clarified; article sets, model settings and scientific CSV sources unchanged.'
 mpath.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Both editorial tables clarified in both languages; scientific sources unchanged.')
