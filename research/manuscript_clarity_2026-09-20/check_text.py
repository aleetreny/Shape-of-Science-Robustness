"""Editorial integrity checks; no scientific calculations are executed."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import ast
import hashlib
import importlib.util
import json
import re

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

tree = ast.parse((ROOT / "research/manuscript_full_2026-09-18/check_text.py").read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"group", "remove", "prose"}]
namespace = {"re": re}
exec(compile(ast.Module(body=functions, type_ignores=[]), "<pure text helpers>", "exec"), namespace)
prose = namespace["prose"]
spec = importlib.util.spec_from_file_location("translation_helpers", ROOT / "research/manuscript_spanish_2026-09-18/verify_translation.py")
translation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(translation)
count = lambda text: len(re.findall(r"\b[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)*\b", prose(text)))
citations = lambda text: [key for group in re.findall(r"\\cite[pt]\{([^}]+)\}", text) for key in group.split(",")]
baseline = json.loads((HERE / "baseline_manifest.json").read_text())
for name, digest in baseline["archived_files"].items():
    assert sha(HERE / "baseline_documents" / name) == digest, ("archive", name)
for name, digest in baseline["protected_files"].items():
    assert sha(ROOT / name) == digest, ("protected", name)

preserved = []
for name, digest in baseline["archived_files"].items():
    if name.startswith(("manuscript/", "manuscript_es/")) and (
        "/figures/" in name or "/tables/data/" in name or name.endswith(".bib") or "/tables/tex/S" in name
    ):
        assert sha(ROOT / name) == digest, ("scientific exhibit", name)
        preserved.append(name)

report = {"created_at": datetime.now(timezone.utc).isoformat(), "documents": {}, "archive_files": len(baseline["archived_files"]),
          "protected_files": len(baseline["protected_files"]), "scientific_exhibits_unchanged": len(preserved)}
bodies = {}
for lang, folder, pdfdir in (("en", "manuscript", "output/pdf"), ("es", "manuscript_es", "output/pdf/es")):
    text = (ROOT / folder / "main.tex").read_text()
    original = (HERE / "baseline_documents" / folder / "main.tex").read_text()
    decl = r"\section*{Declarations}" if lang == "en" else r"\section*{Declaraciones}"
    intro = r"\section{Introduction}" if lang == "en" else r"\section{Introducción}"
    assert text.split(decl, 1)[1] == original.split(decl, 1)[1], (lang, "declarations")
    assert next(line for line in original.splitlines() if r"\LARGE\bfseries" in line) in text
    assert set(citations(text)) == set(citations(original))
    body = text.split(intro, 1)[1].split(decl, 1)[0]
    abstract = text.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
    sections = {p.split("{", 1)[1].split("}", 1)[0]: count(p)
                for p in re.split(r"(?=\\section\{)", intro + body) if p.startswith(r"\section{")}
    # Paragraph pairing tests formal equivalence; semantic review is recorded separately.
    bodies[lang] = (HERE / f"body_{lang}.tex").read_text().split("\n\n")
    if lang == "en":
        assert count(abstract) <= 200
    for document in ("main", "supplement"):
        path = ROOT / pdfdir / f"{document}.pdf"
        reader = PdfReader(path)
        pages = [p.extract_text() for p in reader.pages]
        all_text = "\n".join(pages)
        assert all(len(p.strip()) > 60 for p in pages)
        assert not any(s in all_text for s in ["??", "\ufffd", "TODO", "Writing plan"])
        log = path.with_suffix(".log").read_text()
        bad = [t for t in ["Overfull", "Missing character", "undefined references", "undefined citations", "Citation " + chr(96)] if t in log]
        assert not bad, (lang, document, bad)
        tableword, figureword = ("T\\s*able", "Figure") if lang == "en" else ("T\\s*abla", "Figura")
        tableids = [str(i) for i in range(1,3)] if document == "main" else ["S"+str(i) for i in range(1,18)]
        figureids = [str(i) for i in range(1,5)] if document == "main" else ["S"+str(i) for i in range(1,11)]
        for n in tableids:
            assert re.search(tableword + r"\s+" + n + r"\s*:", all_text), (lang, document, "table", n)
        for n in figureids:
            assert re.search(figureword + r"\s+" + n + r"\s*:", all_text), (lang, document, "figure", n)
        (HERE / f"{lang}_{document}_text.txt").write_text(all_text)
        record = {"path": str(path.relative_to(ROOT)), "sha256": sha(path), "pages": len(pages)}
        if document == "main":
            record.update({"body_words": count(body), "abstract_words": count(abstract), "sections": sections,
                           "title_and_declarations_unchanged": True, "citation_key_set_unchanged": True})
        report["documents"][f"{lang}_{document}"] = record

assert len(bodies["en"]) == len(bodies["es"])
for i, (en, es) in enumerate(zip(bodies["en"], bodies["es"])):
    # Figure width arguments are programming values, not localised prose.
    en = re.sub(r"(?<=\})\{0\.90\}", "{0,90}", en)
    # Remove the final two figure arguments before comparing narrative numbers.
    en = re.sub(r"\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}", "}", en)
    es = re.sub(r"\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}", "}", es)
    a, b = Counter(translation.numbers(en)), Counter(translation.numbers(es, True))
    assert a == b, (i, "numbers", a-b, b-a)
    assert citations(en) == citations(es), (i, "citations")
    ae = [v.replace(",", ".") for v in translation.equations(en)]
    be = [v.replace(",", ".") for v in translation.equations(es)]
    assert ae == be, (i, "math", ae, be)
report["bilingual_paragraphs_checked"] = len(bodies["en"])
report["bilingual_numeric_formula_citation_alignment"] = True
en_supp = (ROOT / "manuscript/supplement.tex").read_text()
es_supp = (ROOT / "manuscript_es/supplement.tex").read_text()
for command in ("citep", "citet", "label", "ref", "input"):
    pattern = r"\\" + command + r"\{([^}]*)\}"
    assert re.findall(pattern, en_supp) == re.findall(pattern, es_supp), ("supplement", command)
assert translation.equations(en_supp) == translation.equations(es_supp), "supplement formulas"
supp_a = Counter(translation.numbers(translation.body(en_supp)))
supp_b = Counter(translation.numbers(translation.body(es_supp), True))
assert supp_a == supp_b, ("supplement numbers", supp_a-supp_b, supp_b-supp_a)
report["supplement_bilingual_numbers_formulas_citations_refs_inputs_aligned"] = True
report["word_count_method"] = "Same pure helper as earlier editions; excludes headings, captions, tables, citations, math and declarations."
report["limits"] = "Formal checks supplement an editorial claim review. They do not certify readability, scientific truth, human authorship or author approval."
(HERE / "text_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
print(json.dumps(report["documents"], indent=2, ensure_ascii=False))
