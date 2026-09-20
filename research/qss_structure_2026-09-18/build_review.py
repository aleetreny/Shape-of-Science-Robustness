"""Export manually reviewed notes and cached Crossref metadata. No new requests."""
import csv
import hashlib
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "data/qss_structure_review_v1"
SKILL = Path.home() / ".codex/skills/citation-management/scripts"
sys.path.insert(0, str(SKILL))
from extract_metadata import MetadataExtractor

notes = json.loads((OUT / "curated_notes.json").read_text())
index = {x["study_id"]: x for x in json.loads((DATA / "reading_index.json").read_text())}
crossref = {x["DOI"].lower(): x for x in json.loads((DATA / "selected_crossref.json").read_text())}
focal = {"Q03", "Q06", "Q07", "Q08", "Q09", "Q12", "Q17", "Q18", "Q24", "Q28", "Q33"}
versions = {
    "Q01": "Manuscrito arXiv 1901.05273; revisión exacta no marcada en la extracción.",
    "Q03": "Manuscrito arXiv 1810.00577; revisión exacta no marcada en la extracción.",
    "Q04": "Manuscrito arXiv 2001.02733; revisión exacta no marcada en la extracción.",
    "Q07": "Manuscrito arXiv 1901.06815; revisión exacta no marcada en la extracción.",
    "Q11": "arXiv 2007.15254v2, 12-11-2020; publicación QSS 2021.",
    "Q12": "Copia rotulada QSS Advance Publication en repositorio de Amberes.",
    "Q13": "Cuerpo completo recuperado mediante DOI; identidad/contenido comprobados, versión tipográfica sin certificar.",
    "Q14": "Copia con pie de descarga de QSS 2(2), p. 643, DOI 00135; extracción pierde algunos encabezados.",
    "Q21": "PDF editorial depositado en HAL; aceptación 24-06-2023 y copyright QSS visibles.",
    "Q24": "arXiv 2308.15706v2, 12-02-2025; texto de autor asociado al artículo publicado.",
    "Q25": "Resumen/inicio de página editorial indexada. Cuerpo ajeno devuelto por DOI rechazado.",
    "Q26": "PDF con datos editoriales QSS 6, 567–610 y aceptación 10-02-2025, alojado en Open University.",
    "Q28": "Cuerpo recuperado desde URL de PDF editorial; sin marcas suficientes para certificar versión del cuerpo.",
    "Q29": "Copia QSS Advance Publication con DOI y copyright de los tres autores, en Corvinus.",
    "Q32": "Manuscrito HAL hal-04715237v1; no atribuir su orden a la maquetación final de 2026.",
    "Q33": "Manuscrito aceptado: portada Version 3, 23-04-2026. OSF preprint q8szh, archivo d5cbe.",
    "Q34": "arXiv 2601.15062v1, 21-01-2026; no es la versión editorial final de agosto."
}
extractor = MetadataExtractor()
records, bib, bibmeta = [], [], []
for n in notes:
    x = index[n["study_id"]]
    c = crossref[x["doi"].lower()]
    title = html.unescape(re.sub(r"<[^>]+>", "", c["title"][0]))
    m = dict(type="doi", entry_type=extractor._crossref_type_to_bibtex(c.get("type")),
             doi=x["doi"], title=title,
             authors=extractor._format_authors_crossref(c.get("author", [])),
             year=extractor._extract_year_crossref(c) or str(x["year"]),
             journal=c["container-title"][0], volume=c.get("volume", ""),
             issue=c.get("issue", ""), pages=c.get("page", ""),
             issn=(c.get("ISSN") or [""])[0])
    bib.append(extractor.metadata_to_bibtex(m, citation_key="QSSreview"+n["study_id"]))
    bibmeta.append(m)
    records.append(dict(title=title, authors=x["authors"],
        year=int(m["year"]), doi=x["doi"], article_url=c["resource"]["primary"]["URL"],
        reading_url=x.get("source", c["resource"]["primary"]["URL"]),
        reading_depth="parcial" if n["study_id"] == "Q25" else "focal" if n["study_id"] in focal else "estructural",
        version_detail=versions.get(n["study_id"], "Texto editorial de QSS; título, contexto y datos de aceptación concordantes."),
        reading_text_sha256=x.get("text_sha256", ""), **n))
(OUT / "article_matrix.json").write_text(json.dumps(records, ensure_ascii=False, indent=2)+"\n")
with (OUT / "article_matrix.csv").open("w", newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
(OUT / "qss_review.bib").write_text("\n\n".join(bib)+"\n")
(OUT / "bibliographic_metadata.json").write_text(json.dumps(bibmeta,ensure_ascii=False,indent=2)+"\n")
header = """# Registro de lectura de 34 artículos de QSS

18-09-2026. Selección dirigida para orientar estructura y argumentación, no metaanálisis ni revisión exhaustiva del contenido científico. **33 lecturas estructurales**, de las cuales once incluyen lectura focal adicional; un artículo solo parcialmente accesible. Lectura estructural significa revisar resumen, secuencia de secciones y pasajes de introducción, método/resultados y cierre. Lectura focal añade pasajes sobre interpretación, comparabilidad, validación o límites. No significa lectura íntegra de todas las páginas, referencias o suplementos ni reproducción técnica.

Las secuencias se normalizan al español por función. No son transcripciones exactas de todos los encabezados: la extracción puede perder numeración o confundir tablas y pies con títulos. Esas pérdidas se corrigieron mediante lectura contextual o se declaran. No se calculan porcentajes de una estructura supuestamente obligatoria. Las versiones de autor no certifican el orden editorial definitivo.

La identidad se contrastó por DOI/metadatos y por el contenido del cuerpo leído. Se descartó una devolución incorrecta para Q25. Las copias completas están solo en `data/qss_structure_review_v1/`, fuera de Git. Esta entrega incluye metadatos, enlaces y notas propias.

[Síntesis y recomendación](../../QSS_STRUCTURE_REVIEW.md) · [Matriz CSV](article_matrix.csv) · [Bibliografía de esta revisión](qss_review.bib).

"""
lines=[header]
for r in records:
    lines += [f"## {r['study_id']} · {r['authors']} ({r['year']})\n",
              f"**[{r['title']}](https://doi.org/{r['doi']})**\n",
              f"- Lectura: **{r['reading_depth']}**. Tipo: {r['paper_type']}.\n- [Copia consultada]({r['reading_url']}): {r['version_detail']}\n- Organización: {r['section_flow_normalized']}.\n- Lección: {r['rhetorical_lesson']}\n- Límite: {r['limit']}\n"]
(OUT / "READING_NOTES.md").write_text("\n".join(lines))
summary=dict(selected=len(records), full_reading_copies=sum(r["reading_depth"]!="parcial" for r in records),
    depth=dict(Counter(r["reading_depth"] for r in records)),
    version_groups=dict(Counter(r["version_group"] for r in records)),
    years=dict(sorted(Counter(r["year"] for r in records).items())),
    missing_pages=[r["doi"] for r in bibmeta if not r.get("pages")],
    bibliography_formatter=str(SKILL/"extract_metadata.py"),
    bibliography_formatter_sha256=hashlib.sha256((SKILL/"extract_metadata.py").read_bytes()).hexdigest())
(OUT / "coverage.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
print(json.dumps(summary,ensure_ascii=False,indent=2))
