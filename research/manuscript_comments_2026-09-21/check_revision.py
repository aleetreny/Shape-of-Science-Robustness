"""Check scientific invariants, bilingual correspondence and delivery integrity."""
from pathlib import Path
from collections import Counter
from decimal import Decimal
from datetime import datetime, timezone
import ast
import hashlib
import json
import re

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())

# Reuse only pure text helpers; never execute the historical audit or analysis.
helpers = {"re": re, "Decimal": Decimal}
for relative, names in [
    ("research/manuscript_full_2026-09-18/check_text.py", {"group", "remove", "prose"}),
    ("research/manuscript_spanish_2026-09-18/verify_translation.py", {"numbers", "equations"}),
]:
    tree = ast.parse((ROOT / relative).read_text())
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<pure text helpers>", "exec"), helpers)

def count(text):
    text = re.sub(r"\\Needspace\{[^}]*\}", "", text)
    return len(re.findall(r"\b[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)*\b", helpers["prose"](text)))

baseline = read(HERE / "baseline_hashes.json")
changed = sorted(name for name, digest in baseline.items() if sha(ROOT / name) != digest)
allowed = {
    f"{folder}/{name}"
    for folder in ("manuscript", "manuscript_es")
    for name in ("main.tex", "references.bib", "tables/editorial/T01.tex", "tables/tex/T01.tex", "tables/manifest.json")
} | {"output/pdf/main.pdf", "output/pdf/es/main.pdf", "output/manuscript_source.zip", "output/manuscript_source_es.zip"}
assert set(changed) == allowed, changed

texts = {}
bodies = {}
documents = {}
for language, folder, pdf_folder, intro, declarations in [
    ("en", "manuscript", "output/pdf", "Introduction", "Declarations"),
    ("es", "manuscript_es", "output/pdf/es", "Introducción", "Declaraciones"),
]:
    current = (ROOT / folder / "main.tex").read_text()
    previous = (HERE / "baseline" / folder / "main.tex").read_text()
    # Exclude the updated draft date; retain every scientific number thereafter.
    content = current.split(r"\begin{abstract}", 1)[1]
    old_content = previous.split(r"\begin{abstract}", 1)[1]
    assert helpers["numbers"](content, language == "es") == helpers["numbers"](old_content, language == "es")
    assert helpers["equations"](current) == helpers["equations"](previous)
    for command in ("label", "ref", "input"):
        pattern = r"\\" + command + r"\{([^}]*)\}"
        assert re.findall(pattern, current) == re.findall(pattern, previous), (language, command)
    declaration_marker = r"\section*{" + declarations + "}"
    assert current.split(declaration_marker)[1] == previous.split(declaration_marker)[1]
    assert next(line for line in previous.splitlines() if r"\LARGE\bfseries" in line) in current
    original_bib = (HERE / "baseline" / folder / "references.bib").read_text()
    assert (ROOT / folder / "references.bib").read_text() == original_bib.replace("Information Processing & Management", r"Information Processing \& Management")
    old_manifest = read(HERE / "baseline" / folder / "tables/manifest.json")
    manifest = read(ROOT / folder / "tables/manifest.json")
    assert {k: v for k, v in manifest.items() if k != "T01"} == {k: v for k, v in old_manifest.items() if k != "T01"}
    assert manifest["T01"]["sources"] == old_manifest["T01"]["sources"]
    assert manifest["T01"]["editorial_source"]["sha256"] == sha(ROOT / folder / "tables/editorial/T01.tex")
    assert (ROOT / folder / "tables/editorial/T01.tex").read_bytes() == (ROOT / folder / "tables/tex/T01.tex").read_bytes()
    abstract = current.split(r"\begin{abstract}")[1].split(r"\end{abstract}")[0]
    body = current.split(r"\section{" + intro + "}")[1].split(declaration_marker)[0]
    texts[language], bodies[language] = current, body
    pdf_path = ROOT / pdf_folder / "main.pdf"
    pages = [page.extract_text() for page in PdfReader(pdf_path).pages]
    assert all(len(page.strip()) > 60 for page in pages)
    pdf_text = "\n".join(pages)
    assert all(token not in pdf_text for token in ("??", "\ufffd", "TODO"))
    log = pdf_path.with_suffix(".log").read_text()
    assert all(token not in log for token in ("Overfull", "Missing character", "undefined references", "undefined citations", "Citation `"))
    for label, total in [("Table" if language == "en" else "Tabla", 2), ("Figure" if language == "en" else "Figura", 4)]:
        for number in range(1, total + 1):
            assert re.search(label[0] + r"\s*" + label[1:] + r"\s+" + str(number) + r"\s*:", pdf_text)
    (HERE / f"{language}_main_text.txt").write_text(pdf_text)
    documents[language] = {"path": str(pdf_path.relative_to(ROOT)), "sha256": sha(pdf_path), "pages": len(pages), "abstract_words": count(abstract), "body_words": count(body)}
assert documents["en"]["abstract_words"] <= 200
for command in ("citep", "citet", "label", "ref", "input"):
    pattern = r"\\" + command + r"\{([^}]*)\}"
    assert re.findall(pattern, texts["en"]) == re.findall(pattern, texts["es"]), command
assert helpers["equations"](texts["en"]) == [x.replace(",", ".") for x in helpers["equations"](texts["es"])]
paragraphs = {language: text.split("\n\n") for language, text in bodies.items()}
assert len(paragraphs["en"]) == len(paragraphs["es"])
for i, (english, spanish) in enumerate(zip(paragraphs["en"], paragraphs["es"])):
    english = re.sub(r"\\Needspace\{[^}]*\}", "", english)
    spanish = re.sub(r"\\Needspace\{[^}]*\}", "", spanish)
    english = re.sub(r"\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}", "}", english)
    spanish = re.sub(r"\}\{(?:scales|paired|input|pairs)\}\{[^}]+\}", "}", spanish)
    assert Counter(helpers["numbers"](english)) == Counter(helpers["numbers"](spanish, True)), i

zenodo = read(HERE / "zenodo_baseline.json")
assert set(zenodo) == {p.name for p in (ROOT / "output/zenodo").iterdir()}
for name, previous in zenodo.items():
    path = ROOT / "output/zenodo" / name
    stat = path.stat()
    assert (stat.st_size, stat.st_mtime_ns, stat.st_ino) == (previous["size"], previous["mtime_ns"], previous["inode"]), name
    if "sha256" in previous:
        assert sha(path) == previous["sha256"], name

portable = read(HERE / "portable_source_audit.json")
for package in portable["packages"].values():
    assert sha(ROOT / package["path"]) == package["sha256"]
    for document in package["documents"].values():
        assert document["byte_identical"]
        assert sha(ROOT / document["path"]) == document["sha256"]

report = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "documents": documents,
    "changed_from_baseline": changed,
    "protected_files_unchanged": len(baseline) - len(changed),
    "bilingual_body_paragraphs_checked": len(paragraphs["en"]),
    "scientific_numeric_sequence_unchanged": True,
    "equations_unchanged": True,
    "supplement_pdfs_byte_identical": True,
    "editable_packages_reproduce_all_four_pdfs_exactly": True,
    "zenodo_files_unchanged": len(zenodo),
    "zenodo_check_scope": "Same exact filenames, sizes, modification times and inodes for all 32 files; SHA256 also checked for all companions below 2 MB. The frozen 51 GB of archives were not rehashed during this editorial revision.",
    "model_selection_claim_scope": "Most used within the directed set of science-mapping studies reviewed; not a census or global top-ten claim. Sources: ACADEMIC_MODEL_USAGE.md and MODEL_SELECTION.md.",
    "angular_reversal_evidence": "ROBUSTNESS_CLOSURE_REPORT.md records reversals of both model responses in 19 model-pair witnesses across ten area pairs; saved morphology_centering_witnesses.csv was inspected without recalculating it.",
    "word_count_method": "Same pure prose helpers as preceding revisions; headings, citations, figure captions, tables, formulae and declarations excluded from body counts.",
}
(HERE / "revision_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
