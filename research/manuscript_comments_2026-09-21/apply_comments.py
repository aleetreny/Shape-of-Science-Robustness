"""Apply the author's five editorial comments without changing saved results."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

changes = {
    "manuscript_es/main.tex": [
        (0, "20 de septiembre de 2026", "21 de septiembre de 2026"),
        (1,
         "Cuando medimos esa dispersión mediante ángulos desde un punto común, mover ese punto puede cambiar la comparación, incluso cuando elegir otros artículos no la cambia. Estas pruebas distinguen el acuerdo entre modelos de la estabilidad al elegir artículos.",
         "Una de las medidas de dispersión compara los ángulos entre líneas trazadas desde un mismo punto hasta la posición de cada artículo. Cambiar ese punto puede invertir qué disciplina parece más dispersa, aunque el resultado se mantenga al elegir otros artículos."),
        (2,
         "Incluyen los 26.000 de la primera prueba más pequeña.",
         "Incluyen los 26.000 de una primera prueba. La ampliación permite comprobar cómo cambian las medidas de acuerdo y su sensibilidad a la elección de artículos al aumentar la muestra."),
        (3,
         "Se eligieron por su uso para representar literatura académica y por sus distintas formas de entrenamiento.",
         r"Para elegirlos, di prioridad a los modelos más utilizados en los estudios de mapas de la ciencia revisados, como SPECTER y SciBERT. Completé el conjunto con modelos empleados como comparación en esos trabajos, cubriendo distintas formas de entrenamiento \citep{refbe130e2973,refc0e2cc29e0,ref07e33b3339}."),
        (4,
         "Mantengo esas configuraciones y pruebo MiniLM con 512 tokens por separado.",
         "Mantengo esas configuraciones en la comparación principal. Como MiniLM recorta parte del texto de casi la mitad de los artículos, lo pruebo por separado con 512 tokens para comprobar si leer más texto cambia su acuerdo con los otros modelos."),
    ],
    "manuscript/main.tex": [
        (0, "20 September 2026", "21 September 2026"),
        (1,
         "When spread is measured through angles from a common reference point, moving that point can change the comparison even when selecting other papers does not. These checks distinguish agreement between models from stability to article selection.",
         "One measure of spread compares angles between lines drawn from a common point to each paper's position. Moving that point can reverse which discipline appears more spread out, even when selecting other papers leaves the answer unchanged."),
        (2,
         "These include the 26,000 used in the first, smaller trial.",
         "These include the 26,000 used in an initial trial. The expansion tests how the agreement measures and their sensitivity to article selection change as more papers are included."),
        (3,
         "Their use in scholarly representation and their different training approaches motivated the selection.",
         r"I prioritised models used most often in the science-mapping studies reviewed, such as SPECTER and SciBERT. I added models used as comparators in those studies to cover different training approaches \citep{refbe130e2973,refc0e2cc29e0,ref07e33b3339}."),
        (4,
         "I retain those settings and test MiniLM at 512 tokens separately.",
         "I retain those settings for the main comparison. Because MiniLM cuts off text in almost half the papers, I also test it separately at 512 tokens to check whether reading more text changes its agreement with the other models."),
    ],
}
for folder, old, new in [
    ("manuscript_es", "Incluye la primera prueba de 26.000.", "Incluye una primera prueba de 26.000."),
    ("manuscript", "Includes the first 26,000-paper trial.", "Includes an initial 26,000-paper trial."),
]:
    for version in ("editorial", "tex"):
        changes[f"{folder}/tables/{version}/T01.tex"] = [(5, old, new)]

prepared = {}
log = []
for relative, edits in changes.items():
    content = (ROOT / relative).read_text()
    for comment, old, new in edits:
        assert content.count(old) == 1, (relative, comment, "match is not unique")
        content = content.replace(old, new)
        log.append({"comment": comment, "file": relative, "before": old, "after": new})
    prepared[relative] = content
for relative, content in prepared.items():
    (ROOT / relative).write_text(content)
(HERE / "comment_changes.json").write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n")
print(f"Applied five comments in both languages; {len(prepared)} source files updated.")
