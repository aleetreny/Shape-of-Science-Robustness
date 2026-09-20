from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
items={
'en':{
 'caption':'Questions, comparisons and article sets.',
 'headers':['Question','What is compared','Articles used'],
 'rows':[
 ['Does the broad arrangement stay similar?', 'Ten models: relations among area or specialty centres, and among individual papers inside groups.', '256 papers per centre; repeated choices and size checks at 128 and 512.'],
 ['Do models find the same nearby papers?', 'The overlap between two models\' lists of 25 neighbours.', 'All papers within each area and period; a separate check fixes 2,048 candidates per group. Global search: 13,000 starting papers among 400,000 candidates.'],
 ['Does changing the input text matter?', 'The same model reads only the title, only the abstract, or both.', '52,000: 2,000 per area, 400 per period. Includes the first 26,000-paper trial.'],
 ['Does reading the same passage matter?', 'Each model\'s usual input versus a common passage that fits every model.', 'A different set of 52,000, with 400 per area and period.'],
 ['Which area has more spread or more directions of variation?', 'Two geometric properties for all 325 pairs of areas, under ten models.', 'The same 52,000 as in the input-text experiment; further article choices test whether the comparisons repeat.'],
 ['Does searching a narrower specialty matter?', 'For example, Cardiology and Cardiovascular Medicine versus Medicine, with 256 candidates in each search.', '50 fixed starting papers per specialty; ten choices of the other 206 candidates. In total, 10,850 starting papers across 217 specialties.'],
 ],
 'note':'All sets come from the same 500,000-paper collection: 400,000 general records plus 100,000 added to strengthen small area--period groups. Rows are not added together. Models use the same paper IDs within each comparison. In the scope comparison, both candidate sets include the same 50 starting papers. Methods and Supplements S1--S4 and S9 give the full controls. The 1,300 software-test papers are not another scientific sample.'},
'es':{
 'caption':'Preguntas, comparaciones y conjuntos de artículos.',
 'headers':['Pregunta','Qué se compara','Artículos utilizados'],
 'rows':[
 [r'\textquestiondown{}Se conserva la organización general?', 'Diez modelos: relaciones entre centros de áreas o especialidades y entre artículos dentro de los grupos.', '256 artículos por centro; elecciones repetidas y controles con 128 y 512.'],
 [r'\textquestiondown{}Encuentran los modelos los mismos artículos cercanos?', 'Cuánto coinciden las listas de 25 vecinos de dos modelos.', 'Todos los artículos de cada área y período; otro control fija 2.048 candidatos por grupo. Búsqueda global: 13.000 artículos de partida entre 400.000 candidatos.'],
 [r'\textquestiondown{}Importa cambiar el texto de entrada?', 'El mismo modelo lee solo el título, solo el resumen o ambos.', '52.000: 2.000 por área, 400 por período. Incluye la primera prueba de 26.000.'],
 [r'\textquestiondown{}Importa que todos lean el mismo fragmento?', 'La entrada habitual de cada modelo frente a un fragmento común que cabe en todos.', 'Otro conjunto de 52.000, con 400 por área y período.'],
 [r'\textquestiondown{}Qué área tiene más dispersión o más direcciones de variación?', 'Dos propiedades geométricas para las 325 parejas de áreas, con diez modelos.', 'Los mismos 52.000 del experimento de texto; otras elecciones de artículos comprueban si las comparaciones se repiten.'],
 [r'\textquestiondown{}Importa limitar la búsqueda a una especialidad?', 'Por ejemplo, Cardiología y Medicina Cardiovascular frente a Medicina, con 256 candidatos en cada búsqueda.', '50 artículos de partida fijos por especialidad; diez elecciones de los otros 206 candidatos. En total, 10.850 artículos de partida en 217 especialidades.'],
 ],
 'note':'Todos los conjuntos proceden de la misma colección de 500.000 artículos: 400.000 registros generales y 100.000 para reforzar grupos pequeños de área y período. Las filas no se suman. Los modelos usan los mismos identificadores en cada comparación. En la comparación de alcance, ambos conjuntos incluyen los mismos 50 artículos de partida. Los métodos y los Suplementos S1--S4 y S9 detallan los controles. Los 1.300 artículos de prueba del programa no son otra muestra científica.'}
}
for lang,folder in [('en','manuscript'),('es','manuscript_es')]:
 d=items[lang]
 tex=r'''\par\noindent\begin{minipage}{\linewidth}
\small
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.10}
'''+r'\captionof{table}{'+d['caption']+r'}\label{tab:T01}'+ '\n'+r'''\begin{tabular}{@{}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{5.4cm}>{\raggedright\arraybackslash}p{5.75cm}@{}}
\toprule
'''+ ' & '.join(r'\textbf{'+h+'}' for h in d['headers'])+r' \\'+'\n'+r'\midrule'+'\n'
 tex+=('\n'+r'\addlinespace[8pt]'+'\n').join(' & '.join(row)+r' \\' for row in d['rows'])
 tex+='\n'+r'''\bottomrule
\end{tabular}
\par\smallskip
'''+d['note']+'\n'+r'\end{minipage}\par'+'\n'
 for path in ['tables/editorial/T01.tex','tables/tex/T01.tex']:(ROOT/folder/path).write_text(tex)
 p=ROOT/folder/'tables/manifest.json';manifest=json.loads(p.read_text());m=manifest['T01']
 m['rendered_parts']=[{'caption':d['caption'],'headers':d['headers'],'rows':len(d['rows'])}]
 m['editorial_source']['sha256']=hashlib.sha256(tex.encode()).hexdigest()
 m['summary_rule']='Author clarification comments, 20 September 2026: six explicit questions; starting corpus moved to the note; global organisation and neighbours separated. Article sets and frozen scientific results unchanged; full controls in methods and S1-S4/S9.'
 p.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('T01 clarified in both languages; six question rows; underlying scientific CSV unchanged.')
