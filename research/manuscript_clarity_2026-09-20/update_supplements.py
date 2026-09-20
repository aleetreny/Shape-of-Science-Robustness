"""Add explanatory entry points without changing saved technical definitions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
guides = {
    "en": r"""
\textbf{Which articles belong to which check?}
The 500,000 records are the starting collection. The text experiment uses 52,000 of them to compare title, abstract and both; its earlier 26,000-paper trial is included, not added. The geometric analysis in S6--S7 reuses that same set of 52,000. A different set of 52,000 is used for the shared-passage check in S1. The matched searches in S4 follow 10,850 starting papers while changing the papers available around them. These are overlapping uses of one collection, not separate downloads.

Here, Field means one of the 26 broad research areas and Subfield means a narrower specialty. The main article introduces the comparisons in that order; this supplement keeps the database names and technical definitions so that the calculations can be checked.
""",
    "es": r"""
\textbf{Qué artículos se usan en cada comprobación.}
Los 500.000 registros son la colección de partida. El experimento de texto utiliza 52.000 para comparar título, resumen y ambos; la primera prueba de 26.000 está incluida, no se suma. El análisis geométrico de S6--S7 reutiliza esos mismos 52.000. Otro conjunto distinto de 52.000 se utiliza para la comprobación del fragmento común en S1. Las búsquedas emparejadas de S4 siguen 10.850 artículos de partida y cambian los artículos disponibles a su alrededor. Son usos que se solapan dentro de una colección, no descargas separadas.

Field significa una de las 26 áreas amplias de investigación y Subfield una especialidad más estrecha. El artículo principal introduce las comparaciones en ese orden; este suplemento conserva los nombres de la base de datos y las definiciones técnicas para poder comprobar los cálculos.
""",
}
intros = {
    "en": {
        "Agreement measures and sampling stability": "This section explains how agreement between two models is calculated, then checks how much the result changes when other articles are selected. Those are two different questions.",
        "Text input, pooling and truncation": "This experiment keeps the papers fixed and changes what each model reads. The main question is whether that change matters more or less than choosing another model.",
        "Scale, neighbourhoods and concrete cases": "These checks move from broad areas to specialties and individual papers. They separate a change in search scope from a change in the number of available papers.",
        "Time, discipline composition and model traits": "These additional comparisons ask where agreement differs: across publication periods, areas and groups of models. Their controls assess possible explanations without identifying a single cause.",
        "Geometric properties and construct checks": "These checks ask what a numerical property actually describes. A measure can repeat reliably and still fail to distinguish separate groups from an elongated cloud or a few extreme points.",
        "All Field-pair comparisons": "Here, a pair is simply two different research areas, such as Medicine and Energy. The 325 pairs cover every such comparison among the 26 areas. The calculation asks which area has the larger geometric value, and whether changing the model reverses that answer.",
    },
    "es": {
        "Medidas de acuerdo y estabilidad del muestreo": "Este apartado explica cómo se calcula el acuerdo entre dos modelos y después comprueba cuánto cambia el resultado al elegir otros artículos. Son dos preguntas diferentes.",
        "Texto de entrada, combinación de salidas y recorte": "Este experimento mantiene los artículos y cambia lo que lee cada modelo. La pregunta principal es si ese cambio importa más o menos que elegir otro modelo.",
        "Escala, vecinos y casos concretos": "Estas comprobaciones pasan de las áreas amplias a las especialidades y los artículos individuales. Separan un cambio del alcance de búsqueda de un cambio en la cantidad de artículos disponibles.",
        "Tiempo, composición disciplinar y características de los modelos": "Estas comparaciones adicionales preguntan dónde cambia el acuerdo: entre períodos de publicación, áreas y grupos de modelos. Sus controles examinan posibles explicaciones sin identificar una causa única.",
        "Propiedades geométricas y comprobación de su significado": "Estas comprobaciones preguntan qué describe realmente una propiedad numérica. Una medida puede repetirse y, aun así, no distinguir grupos separados de una nube alargada o de unos pocos puntos extremos.",
        "Todas las comparaciones entre parejas de áreas": "Aquí, una pareja son simplemente dos áreas distintas, como Medicina y Energía. Las 325 parejas incluyen todas las comparaciones posibles entre las 26 áreas. El cálculo pregunta qué área tiene el valor geométrico mayor y si cambiar el modelo invierte esa respuesta.",
    },
}
for lang, folder in (("en", "manuscript"), ("es", "manuscript_es")):
    source = (HERE / "baseline_documents" / folder / "supplement.tex").read_text()
    source = source.replace("18 September 2026", "20 September 2026").replace("18 de septiembre de 2026", "20 de septiembre de 2026")
    start = source.index(r"\end{center}") + len(r"\end{center}")
    stop = source.index(r"\medskip", start)
    lead = (r"""
This supplement supplies definitions, checks and complete result files. Each table has a printed summary and unrounded CSV files in \nolinkurl{tables/data/Sxx/}. Figure data are in \nolinkurl{figures/data/}. Summaries do not replace those files.
""" if lang == "en" else r"""
Este suplemento aporta definiciones, comprobaciones y archivos completos de resultados. Cada tabla tiene un resumen impreso y archivos CSV sin redondear en \nolinkurl{tables/data/Sxx/}. Los datos de las figuras están en \nolinkurl{figures/data/}. Los resúmenes no sustituyen esos archivos.
""")
    source = source[:start] + "\n" + lead + source[stop:]
    anchor = r"\medskip" + "\n" + r"{\small\setstretch{1}"
    assert source.count(anchor) == 1
    source = source.replace(anchor, guides[lang] + "\n" + anchor)
    for name, intro in intros[lang].items():
        anchor = r"\section{" + name + "}"
        assert source.count(anchor) == 1, name
        source = source.replace(anchor, anchor + "\n" + intro + "\n")
    if lang == "en":
        source = source.replace("The expanded panel uses 400 articles per Field-period group, 2,000 per Field, selected by a fixed ID-based order. It retains the 26,000 pilot IDs.", "The title/abstract experiment uses 52,000 articles: 400 per Field-period group and 2,000 per Field, selected by a fixed ID-based order. The first trial used 26,000; all those IDs remain in the larger set.")
        source = source.replace("The primary effective dimension is $1/\\sum_j p_j^2$, equivalent to the participation ratio in the main text.", r"The participation ratio is $\mathrm{PR}=1/\sum_j p_j^2=(\mathrm{tr}\,C)^2/\mathrm{tr}(C^2)$, where $C$ is the centred covariance matrix. This is the main measure of effective linear dimension.")
    else:
        source = source.replace("La muestra ampliada usa 400 artículos por grupo de área y período, 2.000 por área, seleccionados mediante un orden fijo basado en identificadores. Conserva los 26.000 del piloto.", "El experimento de título y resumen utiliza 52.000 artículos: 400 por grupo de área y período y 2.000 por área, seleccionados mediante un orden fijo basado en identificadores. La primera prueba utilizó 26.000; todos esos identificadores se conservan en el conjunto ampliado.")
        source = source.replace("La dimensión efectiva principal es $1/\\sum_j p_j^2$, equivalente al cociente de participación del texto principal.", r"La razón de participación es $\mathrm{PR}=1/\sum_j p_j^2=(\mathrm{tr}\,C)^2/\mathrm{tr}(C^2)$, donde $C$ es la matriz de covarianza centrada. Es la medida principal de dimensión lineal efectiva.")
    size_heading = "Sample size" if lang == "en" else "Tamaño de muestra"
    size_intro = ("This check varies the number of articles per area while keeping the model and measure fixed. Figure S7 shows how far each value is from the result at 2,000 articles per area." if lang == "en" else "Esta comprobación cambia la cantidad de artículos por área y mantiene el modelo y la medida. La Figura S7 muestra cuánto se aleja cada valor del resultado con 2.000 artículos por área.")
    size_anchor = r"\subsection{" + size_heading + "}"
    assert source.count(size_anchor) == 1
    source = source.replace(size_anchor, size_anchor + "\n" + size_intro + "\n")
    (ROOT / folder / "supplement.tex").write_text(source)
print("Supplement guides updated in both languages; technical definitions retained.")
