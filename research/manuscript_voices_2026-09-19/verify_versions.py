"""Check all six editorial alternatives against the canonical scientific text."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import ast
import hashlib
import importlib.util
import json
import re
import runpy

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
VARIANTS = ROOT / "manuscript_variants"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prose_functions():
    # Reuse only pure text helpers; never execute or change the historical audit.
    tree = ast.parse((ROOT / "research/manuscript_full_2026-09-18/check_text.py").read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name in {"group", "remove", "prose"}]
    namespace = {"re": re}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<pure text helpers>", "exec"), namespace)
    return namespace["prose"]


def run():
    baseline = json.loads((HERE / "baseline_manifest.json").read_text())
    for rel, digest in baseline["protected_files"].items():
        assert sha(ROOT / rel) == digest, ("protected original", rel)
    spec = importlib.util.spec_from_file_location("translation_helpers",
        ROOT / "research/manuscript_spanish_2026-09-18/verify_translation.py")
    translation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(translation)
    spec2 = importlib.util.spec_from_file_location("assemble_helpers", VARIANTS / "assemble.py")
    assembly = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(assembly)
    prose = prose_functions()
    records = json.loads((VARIANTS / "variants.json").read_text())
    body_texts, result = {}, {}
    for key, record in records.items():
        lang = record["language"]
        origin = "manuscript" if lang == "en" else "manuscript_es"
        base_text = (VARIANTS / "base" / lang / "main.tex").read_text()
        assert base_text == (ROOT / origin / "main.tex").read_text()
        for p in (VARIANTS / "base" / lang).rglob("*"):
            if p.is_file():
                assert sha(p) == sha(ROOT / origin / p.relative_to(VARIANTS / "base" / lang)), p
        text = (VARIANTS / record["source"]).read_text()
        originals, lines = base_text.splitlines(), text.splitlines()
        old_blocks = [originals[i] for i in assembly.prose_positions(originals)]
        blocks = [lines[i] for i in assembly.prose_positions(lines)]
        assert len(blocks) == len(old_blocks) == 58
        edits = runpy.run_path(str(VARIANTS / "edits" / f"{key}.py"))["EDITS"]
        assert sum(a != b for a, b in zip(old_blocks, blocks)) == len(edits)
        for i, (a, b) in enumerate(zip(old_blocks, blocks)):
            assert Counter(translation.numbers(a, lang == "es")) == Counter(translation.numbers(b, lang == "es")), (key, i, "numbers")
            assert translation.equations(a) == translation.equations(b), (key, i, "equations")
            assert re.findall(r"\\cite[tp]\{([^}]+)\}", a) == re.findall(r"\\cite[tp]\{([^}]+)\}", b), (key, i, "citation association")
            if i not in edits:
                assert a == b
        assert old_blocks[53:] == blocks[53:], (key, "declarations")
        for command in ("section", "subsection", "input", "ref", "label"):
            pattern = r"\\" + command + r"\{([^}]+)\}"
            assert re.findall(pattern, base_text) == re.findall(pattern, text), (key, command)
        assert re.findall(r"(?m)^\\PanelFigure.*$", base_text) == re.findall(r"(?m)^\\PanelFigure.*$", text)
        assert next(s for s in originals if r"\LARGE\bfseries" in s) in text
        start = r"\section{Introduction}" if lang == "en" else r"\section{Introducción}"
        end = r"\section*{Declarations}" if lang == "en" else r"\section*{Declaraciones}"
        body = text.split(start, 1)[1].split(end, 1)[0]
        abstract = text.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
        pattern = r"\b[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)*\b"
        count = lambda value: len(re.findall(pattern, prose(value)))
        if lang == "en":
            assert count(abstract) <= 200
            assert 3900 <= count(body) <= 4900
        body_texts[key] = blocks
        pdf = ROOT / "output/pdf/voice_variants" / f"{key}.pdf"
        reader = PdfReader(pdf)
        pages = [p.extract_text() for p in reader.pages]
        extracted = "\n".join(pages)
        assert all(len(p.strip()) > 80 for p in pages)
        assert not any(s in extracted for s in ["??", "\ufffd", "£", "TODO", "Writing plan"])
        assert "OpenAI Codex" in extracted
        log = (pdf.parent / "logs" / f"{key}.log").read_text()
        assert not any(t in log for t in ["Overfull", "Missing character", "undefined references", "undefined citations", "Citation " + chr(96)])
        table_word, figure_word = ("Table", "Figure") if lang == "en" else ("Tabla", "Figura")
        for n in range(1, 3):
            assert re.search(table_word[0] + r"\s*" + table_word[1:] + r"\s+" + str(n) + r"\s*:", extracted)
        for n in range(1, 5):
            assert re.search(figure_word + r"\s+" + str(n) + r"\s*:", extracted)
        result[key] = {"source": record["source"], "pdf": str(pdf.relative_to(ROOT)),
                       "sha256": sha(pdf), "pages": len(reader.pages),
                       "body_words": count(body), "abstract_words": count(abstract),
                       "rewritten_paragraphs": len(edits),
                       "title_structure_figures_tables_and_declarations_preserved": True,
                       "numeric_occurrences_formulas_and_citation_associations_preserved": True,
                       "no_overflow_missing_glyphs_or_unresolved_references": True}
    for v in (1, 2, 3):
        for i, (a, b) in enumerate(zip(body_texts[f"v{v}_en"], body_texts[f"v{v}_es"])):
            assert Counter(translation.numbers(a)) == Counter(translation.numbers(b, True)), (v, i, "bilingual numbers")
            assert translation.equations(a) == translation.equations(b), (v, i, "bilingual formula")
            assert re.findall(r"\\cite[tp]\{([^}]+)\}", a) == re.findall(r"\\cite[tp]\{([^}]+)\}", b), (v, i, "bilingual citations")
    audit = {"created_at": datetime.now(timezone.utc).isoformat(), "status": "passed",
             "canonical_files_verified_unchanged": len(baseline["protected_files"]),
             "versions": result, "all_six_full_articles": True,
             "supplements_common_and_unchanged": True,
             "bilingual_numeric_formula_and_citation_equivalence": True,
             "new_scientific_computation": False,
             "limits": "Text checks preserve formal content; semantic and editorial review is recorded separately. No authorship detector was used."}
    (HERE / "text_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: {field: v[field] for field in ("pages", "body_words", "abstract_words", "rewritten_paragraphs")}
                      for k, v in result.items()}, indent=2))


if __name__ == "__main__":
    run()
