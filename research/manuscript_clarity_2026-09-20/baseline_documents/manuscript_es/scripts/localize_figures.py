"""Derive a Spanish display exporter without changing numeric operations."""
from pathlib import Path
import ast, json
ROOT=Path(__file__).resolve().parents[2]
PAIRS='''
Observed groups|||Grupos observados
Random groups|||Grupos aleatorios
Corrected CKA|||CKA corregida
A  Between group centres|||A  Entre centros
B  Within groups|||B  Dentro de los grupos
26 Fields|||26 áreas
Same 183 Subfields|||Mismas 183 especialidades
Articles per group|||Artículos por grupo
Higher within Subfield (90)|||Mayor en especialidad (90)
Lower within Subfield (127)|||Menor en especialidad (127)
Neighbour overlap within the parent Field|||Coincidencia de vecinos en el área
Neighbour overlap within the Subfield|||Coincidencia de vecinos en la especialidad
A  Shape change|||A  Cambio de forma
B  Neighbour change|||B  Cambio de vecinos
1 - corrected CKA|||1 - CKA corregida
Fraction of 25 neighbours changed|||Fracción de 25 vecinos sustituidos
A  Angular spread|||A  Apertura angular
B  Effective linear dimension (PR)|||B  Dimensión lineal efectiva (PR)
Field pairs (325 for each property)|||Parejas de áreas (325 por propiedad)
All ten agree|||Acuerdo de los diez
Persistent opposition|||Oposición persistente
Unresolved|||Sin resolver
Flagged input contrasts (out of 520)|||Contrastes de entrada con alerta (de 520)
Media Technology|||Tecnología de medios
Building and Construction|||Edificación y construcción
Renewable Energy, Sustainability and the Environment|||Energía renovable, sostenibilidad y medio ambiente
Toxicology|||Toxicología
Automotive Engineering|||Ingeniería del automóvil
Water Science and Technology|||Ciencia y tecnología del agua
Algebra and Number Theory|||Álgebra y teoría de números
Religious studies|||Estudios religiosos
Numerical Analysis|||Análisis numérico
History|||Historia
Literature and Literary Theory|||Literatura y teoría literaria
Geometry and Topology|||Geometría y topología
SIRT6 / cancer [b]|||SIRT6 / cáncer [b]
Mathematics education [a]|||Enseñanza matemática [a]
State-owned businesses|||Empresas estatales
Petrol dispatch|||Distribución de combustible
Persuasive talk [a]|||Persuasión [a]
Pedestrian injuries|||Lesiones de peatones
Invasion Strategy [a]|||Estrategia de invasión [a]
Witch trials [a]|||Juicios de brujería [a]
Cobalt / silica layers|||Cobalto / capas de sílice
Announcement [a]|||Anuncio [a]
Expert-system conversion|||Conversión de sistema experto
Arthurian poetry|||Poesía artúrica
Equal group size|||Tamaño igualado
2,048 candidates|||2.048 candidatos
All candidates|||Todos los candidatos
A  Shape|||A  Forma
B  Neighbours|||B  Vecinos
Change from 2000-04|||Cambio desde 2000-04
Observed / ten models|||Observada / diez modelos
Balanced / ten models|||Equilibrada / diez modelos
Observed / eight models|||Observada / ocho modelos
Balanced / eight models|||Equilibrada / ocho modelos
A  Shape: corrected CKA|||A  Forma: CKA corregida
B  Neighbour overlap at k = 25|||B  Coincidencia de vecinos con k = 25
Medicine|||Medicina
Energy*|||Energía*
Mathematics|||Matemáticas
Physics|||Física
A  Mean|||A  Media
B  Linear dimension|||B  Dimensión lineal
C  Connection|||C  Conexión
Articles per Field|||Artículos por área
Change from n = 2,000 (%)|||Cambio respecto a n = 2.000 (%)
Quality flags|||Marcas de calidad
Common fragment|||Fragmento común
Abstract only|||Solo resumen
Title only|||Solo título
Word BERTs: CLS|||BERT de palabras: CLS
Word BERTs: SEP|||BERT de palabras: SEP
Global centring|||Centrado global
A  Spread|||A  Apertura
B  Dimension|||B  Dimensión
Spearman agreement of Field rankings|||Acuerdo de rangos de áreas (Spearman)
One round cloud|||Nube redonda
One narrow cloud|||Nube estrecha
One wide cloud|||Nube ancha
One elongated cloud|||Nube alargada
One low-rank cloud|||Nube de rango bajo
Two separated groups|||Dos grupos separados
Four separated groups|||Cuatro grupos separados
Two groups with bridges|||Dos grupos con puentes
One cloud with outliers|||Nube con puntos atípicos
A  Spectral gap|||A  Brecha espectral
B  Radius ratio|||B  Cociente de radios
C  Edge ratio|||C  Cociente de aristas
Agriculture / biology|||Agricultura / biología
Arts / humanities|||Artes / humanidades
Biochemistry / genetics|||Bioquímica / genética
Business / management|||Negocios / gestión
Chemical engineering|||Ingeniería química
Chemistry|||Química
Computer science|||Informática
Decision sciences|||Ciencias de la decisión
Earth / planetary science|||Tierra / planetas
Economics / finance|||Economía / finanzas
Energy|||Energía
Engineering|||Ingeniería
Environmental science|||Ciencias ambientales
Immunology / microbiology|||Inmunología / microbiología
Materials science|||Ciencia de materiales
Neuroscience|||Neurociencia
Nursing|||Enfermería
Pharmacology / toxicology|||Farmacología / toxicología
Physics / astronomy|||Física / astronomía
Psychology|||Psicología
Social sciences|||Ciencias sociales
Veterinary|||Veterinaria
Dentistry|||Odontología
Health professions|||Profesiones sanitarias
'''
labels=dict(line.split('|||',1) for line in PAIRS.strip().splitlines())
labels.update({
'26 Field\ncentres':'26\náreas',
'217 Subfield\ncentres':'217\nespecial.',
'26 Subfield\ncentres':'26\nespecial.',
'Change\nmodel':'Cambiar\nmodelo','Remove\nabstract':'Quitar\nresumen','Remove\ntitle':'Quitar\ntítulo',
'Minimum\nrelative difference':'Diferencia\nrelativa mínima',
'20 selections\nOriginal check':'20 selecciones\nControl original',
'100 selections\nAdditional check':'100 selecciones\nControl adicional',
'Relative agreement rank (%)\nLower agreement to higher agreement':'Posición relativa de acuerdo (%)\nDe menor a mayor acuerdo',
'Upper triangle: angular spread\nLower triangle: effective linear dimension':'Triángulo superior: apertura angular\nTriángulo inferior: dimensión lineal efectiva',
})
class Translate(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str) and node.value in labels:
            return ast.copy_location(ast.Constant(labels[node.value]),node)
        return node
source=(ROOT/'manuscript/scripts/build_figures.py').read_text().replace("OUT = ROOT / 'manuscript'","OUT = ROOT / 'manuscript_es'")
source=source.replace("f'{mean_value:.3f}'", "format(mean_value, '.3f').replace('.', ',')")
source=source.replace("textwrap.wrap(x['name'], 34)","textwrap.wrap(SPANISH_LABELS.get(x['name'], x['name']), 34)")
source=source.replace("def save(item, fig):",'''def save(item, fig):
    from matplotlib.ticker import ScalarFormatter, FuncFormatter
    # Spanish decimal typography; values, ranges and plot geometry are unchanged.
    for axis in fig.axes:
        for dimension in (axis.xaxis, axis.yaxis):
            formatter = dimension.get_major_formatter()
            if isinstance(formatter, ScalarFormatter):
                dimension.set_major_formatter(FuncFormatter(lambda value, position: format(value, 'g').replace('.', ',')))
''')
node=Translate().visit(ast.parse(source));ast.fix_missing_locations(node)
text=ast.unparse(node)
text=text.replace('MANIFEST = {}','SPANISH_LABELS = '+repr(labels)+'\nMANIFEST = {}')
(ROOT/'manuscript_es/scripts/build_figures.py').write_text(text+'\n')
(ROOT/'manuscript_es/figures/translation_labels.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n')
print('Spanish figure exporter derived; no scientific operations changed.')
