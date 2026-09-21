"""Apply verified public availability to both manuscripts; no scientific edits."""
from pathlib import Path
import argparse,csv,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preview-root',type=Path);args=parser.parse_args()
if args.preview_root:
 ROOT=args.preview_root.resolve()
 print('Preparing a local preview only; publication is still checked before changing the canonical manuscript.')
else:
 public=json.loads((HERE/'public_verification.json').read_text());assert public['published'] is True and public['record']==22876602
release=json.loads((ROOT/'output/compact_release/release-manifest.json').read_text())
paragraphs={
'en':r'''Code and analysis data (version 1.1.0) are archived at \url{https://doi.org/10.5281/zenodo.22876602} \citep{treny2026reproduction}. A \href{https://github.com/aleetreny/Shape-of-Science-Reproducibility}{GitHub mirror} provides the same files and commands. They preserve article identifiers, exact selections, measurements by model, counts by query and controls. The public route repeats the documented statistical comparisons from those frozen measurements; it excludes stored vectors, neighbour lists and model weights. Historical title/abstract tables are not redistributed because rights to the plaintext abstracts have not been established. Fresh OpenAlex retrieval may return different text, so an exact rerun from the historical inputs is not guaranteed. Code is MIT; original results and documentation are CC BY 4.0; OpenAlex metadata retain CC0. Supplement S8 details the tested scope.''',
'es':r'''El código y los datos de análisis (versión 1.1.0) están archivados en \url{https://doi.org/10.5281/zenodo.22876602} \citep{treny2026reproduction}. Una \href{https://github.com/aleetreny/Shape-of-Science-Reproducibility}{copia en GitHub} ofrece los mismos archivos y comandos. Conservan identificadores de artículos, selecciones exactas, medidas por modelo, recuentos por consulta y controles. La vía pública repite las comparaciones estadísticas documentadas desde esas medidas congeladas; excluye los vectores guardados, las listas de vecinos y los pesos de los modelos. No se distribuyen las tablas históricas de títulos y resúmenes porque no se han establecido los permisos sobre el texto de los resúmenes. Recuperar de nuevo los registros de OpenAlex puede devolver textos distintos, por lo que no se garantiza una repetición exacta desde las entradas históricas. El código usa MIT; resultados y documentos propios, CC BY 4.0; metadatos OpenAlex, CC0. El Suplemento S8 detalla el alcance comprobado.'''}
access={
'en':r'''\subsection{Public statistical reproduction}
The compact data and code release is archived at \url{https://doi.org/10.5281/zenodo.22876602} \citep{treny2026reproduction}. After extracting the code and data archives together, \nolinkurl{python reproducibility/reproduce_analysis.py} verifies the supplied hashes and recalculates 25 tables with 106,445 rows. It checks 17,550 local neighbour scores from per-query intersection counts, recalculates the balanced local and global averages, and runs the aggregation checks for all four main figures. The regenerated table contents match the saved references exactly in the tested environment. Pinned dependencies, commands and tolerances are provided in the release README.

This route starts from frozen model-derived measurements. It does not regenerate embeddings from historical text, reconstruct the excluded nearest-neighbour lists or certify a new run of every supplementary analysis. Historical title/abstract input tables are withheld because redistribution rights to the plaintext abstracts have not been established. Exact identifiers and input hashes are retained, but fresh OpenAlex retrieval may differ. Manuscripts and supplements are separate from the data release and may be edited without changing the archived measurements.
''',
'es':r'''\subsection{Reproducción pública de las comparaciones}
La entrega compacta de datos y código está archivada en \url{https://doi.org/10.5281/zenodo.22876602} \citep{treny2026reproduction}. Tras extraer juntos los archivos de código y datos, \nolinkurl{python reproducibility/reproduce_analysis.py} verifica sus huellas y recalcula 25 tablas con 106.445 filas. Comprueba 17.550 medidas locales de vecinos desde los recuentos por consulta, recalcula las medias local y global equilibradas y ejecuta las comprobaciones de agregación de las cuatro figuras principales. El contenido de las tablas recalculadas coincide exactamente con las referencias guardadas en el entorno probado. El README de la entrega indica versiones, comandos y tolerancias.

Esta vía parte de medidas congeladas producidas por los modelos. No regenera los embeddings desde el texto histórico ni reconstruye las listas de vecinos excluidas; tampoco certifica una nueva ejecución de todos los análisis suplementarios. Las tablas históricas de títulos y resúmenes no se distribuyen porque no se han establecido los permisos sobre el texto de los resúmenes. Se conservan identificadores y huellas de entrada, pero recuperar de nuevo los registros de OpenAlex puede dar un contenido distinto. Artículos y suplementos están separados del depósito de datos y pueden editarse sin modificar las medidas archivadas.
'''}
bib='''\n@misc{treny2026reproduction,\n  author = {Treny Ortega, Alejandro},\n  title = {How much does the map of science depend on the embedding model? Compact reproducibility data and code},\n  year = {2026},\n  howpublished = {Zenodo, version 1.1.0, data set},\n  doi = {10.5281/zenodo.22876602},\n  url = {https://doi.org/10.5281/zenodo.22876602}\n}\n'''
archives=[r for r in release['files'] if r['name'].endswith('.zip')]
for lang,folder,heading,oldsub,authors in [('en','manuscript',r'\textbf{Data and code availability.}',r'\subsection{Access limits of this draft}','The author has confirmed'),('es','manuscript_es',r'\textbf{Disponibilidad de datos y código.}',r'\subsection{Límites de acceso de este borrador}','El autor ha confirmado')]:
 base=ROOT/folder;p=base/'main.tex';s=p.read_text();a=s.index(heading)+len(heading);b=s.index(r'\begingroup',a);p.write_text(s[:a]+'\n'+paragraphs[lang]+'\n\n'+s[b:])
 p=base/'references.bib';s=p.read_text();assert 'treny2026reproduction' not in s;p.write_text(s+bib)
 p=base/'supplement.tex';s=p.read_text();a=s.index(oldsub);b=s.index(authors,a);s=s[:a]+access[lang]+'\n'+s[b:]
 s=s.replace('The source package reproduces this display, not the unavailable corpus.','The separate data release supports the statistical reproduction described in S8.')
 s=s.replace('El paquete fuente reproduce esta presentación, no el corpus que no se distribuye.','La entrega separada de datos permite la reproducción estadística descrita en S8.')
 p.write_text(s)
 caption='Public release archives and their SHA-256 checksums.' if lang=='en' else 'Archivos públicos de la entrega y sus huellas SHA-256.'
 labels=['Code and guides','Corpus metadata','Initial comparisons','Text pilot','Model configuration','Area pairs','Geometry','Source cases','Final controls','Expanded comparisons'] if lang=='en' else ['Código y guías','Metadatos del corpus','Comparaciones iniciales','Piloto de texto','Configuración de modelos','Parejas de áreas','Geometría','Casos de origen','Controles finales','Comparaciones ampliadas']
 # Match labels explicitly to archive names rather than file-system ordering.
 names=['code-and-guides.zip','data-analysis-ready-v1.zip','data-analysis-v1.zip','data-checklist-v1.zip','data-embeddings-v1.zip','data-field-pair-summary-v1.zip','data-morphology-pilot-v1.zip','data-prepaper-v1.zip','data-robustness-closure-v1.zip','data-robustness-v2.zip']
 lookup={r['name']:r for r in archives};rows=[]
 for label,name in zip(labels,names):
  r=lookup[name];rows.append(label+r' & {\footnotesize\nolinkurl{'+name+r'}}\newline{\ttfamily\seqsplit{'+r['sha256']+r'}} & '+f"{r['bytes']/1e6:.2f}"+r' MB \\')
 headers=r'\textbf{Contents} & \textbf{Archive / SHA-256} & \textbf{Size} \\' if lang=='en' else r'\textbf{Contenido} & \textbf{Archivo / SHA-256} & \textbf{Tamaño} \\'
 note=r'All listed archives are public under DOI \nolinkurl{10.5281/zenodo.22876602}. \nolinkurl{SELECTION.json} lists the selected data files and their origins. These are analysis-level data; historical texts and vector caches are excluded. Code is MIT, original results/documents CC BY 4.0, and OpenAlex metadata CC0.' if lang=='en' else r'Todos los archivos indicados son públicos bajo el DOI \nolinkurl{10.5281/zenodo.22876602}. \nolinkurl{SELECTION.json} enumera los archivos de datos seleccionados y su origen. Son datos para repetir el análisis estadístico; se excluyen textos históricos y cachés de vectores. El código usa MIT; resultados y documentos propios, CC BY 4.0; metadatos OpenAlex, CC0.'
 table=r'''\par\noindent\begin{minipage}{\linewidth}
\small
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.13}
\captionof{table}{'''+caption+r'''}\label{tab:S17}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{3.05cm}>{\raggedright\arraybackslash}p{10.0cm}>{\raggedright\arraybackslash}p{2.2cm}@{}}
\toprule
'''+headers+'\n'+r'\midrule'+'\n'+'\n'.join(rows)+'\n'+r'''\bottomrule
\end{tabular}
\end{minipage}\par
\par\smallskip{\small '''+note+r'\par}'+'\n'
 for sub in ['tables/tex','tables/editorial']:
  p=base/sub/'S17.tex';p.parent.mkdir(exist_ok=True);p.write_text(table)
 p=base/'tables/data/S17/release-manifest.json';p.write_text(json.dumps(release,indent=2)+'\n')
 p=base/'tables/manifest.json';d=json.loads(p.read_text());d['S17']={'sources':[{'source':'Public compact release v1.1.0','included':'tables/data/S17/release-manifest.json','sha256':hashlib.sha256((base/'tables/data/S17/release-manifest.json').read_bytes()).hexdigest(),'rows':len(archives)}],'editorial_source':{'path':'tables/editorial/S17.tex','sha256':hashlib.sha256(table.encode()).hexdigest()},'summary_rule':'Verified public archive sizes and hashes. No scientific results changed.'};p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
(HERE/'availability_paragraphs.json').write_text(json.dumps(paragraphs,indent=2,ensure_ascii=False)+'\n')
print('Updated availability, citation and S8 in both languages; scientific sections untouched.')
