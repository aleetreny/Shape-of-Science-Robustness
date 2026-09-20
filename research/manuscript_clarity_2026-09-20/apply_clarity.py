"""Apply the authored bilingual prose to the archived canonical wrappers."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
for lang, folder in (("en", "manuscript"), ("es", "manuscript_es")):
    original = (HERE / "baseline_documents" / folder / "main.tex").read_text()
    marker = r"\section*{Declarations}" if lang == "en" else r"\section*{Declaraciones}"
    prefix = original.split(r"\begin{abstract}", 1)[0]
    prefix = prefix.replace("18 September 2026", "20 September 2026")
    prefix = prefix.replace("18 de septiembre de 2026", "20 de septiembre de 2026")
    tail = marker + original.split(marker, 1)[1]
    body = (HERE / f"body_{lang}.tex").read_text()
    methods = r"\section{Data and methods}" if lang == "en" else r"\section{Datos y métodos}"
    body = body.replace(methods, r"\clearpage" + "\n" + methods)
    results = r"\section{Results}" if lang == "en" else r"\section{Resultados}"
    discussion = r"\section{Discussion}" if lang == "en" else r"\section{Discusión}"
    before, after = body.split(results, 1)
    findings, end = after.split(discussion, 1)
    findings = findings.replace(r"\subsection", r"\FloatBarrier" + "\n" + r"\subsection")
    body = before + results + findings + r"\FloatBarrier" + "\n" + discussion + end
    (ROOT / folder / "main.tex").write_text(prefix + body + "\n" + tail)
    (ROOT / folder / "tables/tex/T01.tex").write_text((HERE / f"T01_{lang}.tex").read_text())

    table = ROOT / folder / "tables/tex/T02.tex"
    source = (HERE / "baseline_documents" / folder / "tables/tex/T02.tex").read_text()
    source = source.replace(r"\end{minipage}\par" + "\n", "")
    if lang == "en":
        source = source.replace(r"\textbf{Dim.}", r"\textbf{Vector size}")
        source = source.replace(r"\textbf{Tokens}", r"\textbf{Token limit}")
        source = source.replace(r"\textbf{Readout}", r"\textbf{Paper vector}")
        source = source.replace("MPNet and MiniLM use", "Vector size is the number of coordinates. MPNet and MiniLM use")
        source = source.replace("Readout variants are not additional models.", "Changing the pooling rule does not add a separately trained model.")
    else:
        source = source.replace(r"\textbf{Dim.}", r"\textbf{Tamaño}")
        source = source.replace(r"\textbf{Tokens}", r"\textbf{Límite de tokens}")
        source = source.replace(r"\textbf{Representación}", r"\textbf{Vector del artículo}")
        source = source.replace("MPNet y MiniLM utilizan", "Tamaño indica cuántas coordenadas contiene el vector. MPNet y MiniLM utilizan")
    source = source.replace("m{1.1cm}", "m{1.6cm}").replace("m{1.45cm}", "m{1.65cm}").replace("m{5.6cm}", "m{4.9cm}")
    table.write_text(r"\begin{table}[!htbp]" + "\n" + source.rstrip() + "\n" + r"\end{minipage}\par" + "\n" + r"\end{table}" + "\n")

print("Canonical article sources and model-table explanations updated in both languages.")
