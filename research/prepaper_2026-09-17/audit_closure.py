"""Seal the local pre-paper delivery; read-only checks, no inference or network."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "research/prepaper_2026-09-17"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify_files(base, records):
    for filename, expected in records.items():
        assert sha(base / filename) == expected, filename
    return len(records)


def main():
    baseline = read(REVIEW / "baseline.json")
    assert sha(ROOT / "research/robustness_2026-09-17/closure_audit.json") == baseline["prior_closure_sha256"]
    baseline_count = verify_files(REVIEW / "baseline_documents", baseline["prior_documents_verified_and_preserved"])

    prior = ROOT / "reports/robustness_v2/final"
    prior_count = verify_files(prior, read(prior / "catalog.json")["files"])
    numerical = read(REVIEW / "numerical_audit.json")
    assert numerical["all_complete"] and len(numerical["components"]) == 15
    assert numerical["script_sha256"] == sha(REVIEW / "numerical_audit.py")
    assert numerical["real_full_sort_neighbor_queries"] == 300
    assert len(numerical["real_gram_formula_checks"]) == 6
    assert all(r["absolute_error"] < 1e-10 for r in numerical["real_gram_formula_checks"])
    science_sources = {}
    for component in numerical["components"]:
        base = ROOT / "data/robustness_v2" / component["component"]
        records = read(base / "manifest.json")["source_files"]
        verify_files(ROOT, records)
        verify_files(base / "source_snapshot", records)
        science_sources.update(records)

    atlas = ROOT / "data/prepaper_v1/case_atlas"
    atlas_audit = read(atlas / "audit.json")
    assert atlas_audit["all_complete"] and atlas_audit["queries"] == 10850
    assert atlas_audit["directed_article_relations"] == 531650
    assert atlas_audit["subfield_center_pairs"] == 23436
    atlas_count = verify_files(atlas, atlas_audit["files"])
    manifest = read(atlas / "manifest.json")
    verify_files(ROOT, manifest["source_files"])
    verify_files(atlas / "source_snapshot", manifest["source_files"])
    verify_files(ROOT, manifest["parent_files"])
    verify_files(ROOT, atlas_audit["parent_neighbor_hashes"])

    quality = ROOT / "data/prepaper_v1/source_quality"
    quality_audit = read(quality / "audit.json")
    assert quality_audit["all_complete"] and quality_audit["raw_pages_reverified"] == 30
    verify_files(quality, quality_audit["files"])
    verify_files(ROOT, quality_audit["parent_files"])
    assert quality_audit["script_sha256"] == sha(REVIEW / "source_quality_audit.py")

    report = ROOT / "reports/prepaper_v1"
    catalog = read(report / "catalog.json")
    report_count = verify_files(report, catalog["files"])
    assert catalog["source_audit_sha256"] == sha(atlas / "audit.json")
    assert catalog["exporter_sha256"] == sha(ROOT / "sos_review/report.py")
    assert catalog["visual_review"] == "complete"
    assert catalog["visual_review_sha256"] == sha(ROOT / catalog["visual_review_record"])
    visual = read(ROOT / catalog["visual_review_record"])
    verify_files(report, visual["figures"])
    assert len(visual["figures"]) == 6
    assert len(list(report.glob("*.csv"))) == 9
    for filename, count in [("subfields.csv", 217), ("subfield_sensitivity_panels.csv", 4941),
                            ("paper_examples.csv", 12), ("article_relation_examples.csv", 24),
                            ("subfield_relation_examples.csv", 16)]:
        with (report / filename).open() as handle:
            assert len(list(csv.DictReader(handle))) == count, filename

    bib = read(REVIEW / "bibliography_validation.json")
    assert bib["valid_entries"] == bib["total_entries"] == 45
    assert not bib["errors"] and not bib["duplicates"]
    assert len(bib["warnings"]) == 1 and bib["warnings"][0]["field"] == "pages"
    assert len(re.findall(r"(?m)^@\w+\{", (ROOT / "references/references.bib").read_text())) == 45
    assert len(read(REVIEW / "reference_verification.json")) == 41
    assert len(read(REVIEW / "reference_supplement.json")) == 4
    for filename, count in [("tests_analysis_correct_environment.txt", 32), ("tests_embedding.txt", 20)]:
        output = (REVIEW / filename).read_text()
        assert f"Ran {count} tests" in output and output.rstrip().endswith("OK")

    names = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
    paths = sorted({ROOT / p for p in names if p and p != "research/prepaper_2026-09-17/closure_audit.json"})
    patterns = {
        "credential_prefix": rb"(?<![A-Za-z0-9])(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|hf_[A-Za-z0-9]{25,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,})",
        "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "literal_api_key": rb"(?i)[\"']?(?:api_key|apikey|openalex_api_key)[\"']?\s*[:=]\s*[\"']([A-Za-z0-9_./+-]{16,})[\"']",
        "url_api_key": rb"(?i)[?&](?:api_key|apikey)=([A-Za-z0-9_-]{16,})",
    }
    local_links = 0
    broken = []
    secrets = []
    text_files = 0
    eligible_bytes = 0
    for path in paths:
        if not path.is_file() or path.is_symlink():
            continue
        content = path.read_bytes()
        eligible_bytes += len(content)
        if b"\0" not in content[:8192]:
            text_files += 1
            for rule, pattern in patterns.items():
                if re.search(pattern, content):
                    secrets.append({"path": str(path.relative_to(ROOT)), "rule": rule})
        if path.suffix != ".md" or "baseline_documents" in path.parts or path.name == "legacy_bibliography_original.md":
            continue
        for match in re.finditer(r"\[[^\]\n]*\]\(([^\n]+?)\)", content.decode(errors="replace")):
            url = match.group(1).split(' "')[0].strip("<>")
            if url.startswith(("https:", "http:", "mailto:", "app:", "#", "codex:")) or "\\" in url or "{" in url:
                continue
            target = unquote(url.split("#")[0])
            local_links += 1
            if not (path.parent / target).exists():
                broken.append({"source": str(path.relative_to(ROOT)), "target": target})
    assert not broken, broken
    # Never print matched credential text, including when a check fails.
    assert not secrets, secrets
    assert not any(p.relative_to(ROOT).parts[0] == "data" or p.suffix in {".swp", ".swo"} or p.name == ".env" for p in paths)
    assert ROOT / "research/model_review_2026-09-15/academic_sources/studies.json" in paths

    documents = sorted(set(ROOT.glob("*.md")) | set((ROOT / "docs").glob("*.md")) | set((ROOT / "references").glob("*.md")))
    evidence = [p for p in REVIEW.glob("*") if p.is_file() and p.name != "closure_audit.json"]
    result = {
        "all_complete": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "baseline_document_copies_verified": baseline_count,
        "prior_closure_unchanged": True,
        "prior_report_files_verified": prior_count,
        "prior_scientific_source_files_verified": len(science_sources),
        "numerical_audit_sha256": sha(REVIEW / "numerical_audit.json"),
        "atlas_files_verified": atlas_count,
        "atlas_audit_sha256": sha(atlas / "audit.json"),
        "quality_audit_sha256": sha(quality / "audit.json"),
        "report_files_verified": report_count,
        "report_catalog_sha256": sha(report / "catalog.json"),
        "tests_passed": {"analysis": 32, "embedding": 20},
        "bibliography": {"valid": 45, "errors": 0, "duplicates": 0, "documented_warning": "ReSi ICLR pages absent"},
        "local_markdown_links_checked": local_links,
        "broken_links": broken,
        "git_eligible_scan": {"files": len(paths), "bytes": eligible_bytes, "text_files": text_files,
                              "credential_pattern_findings": secrets, "scope": "Pattern scan only; no guarantee of detecting every possible secret format."},
        "current_documents": {str(p.relative_to(ROOT)): sha(p) for p in documents},
        "review_evidence": {str(p.relative_to(ROOT)): sha(p) for p in evidence},
        "new_computations": "Derived atlas and read-only audits; no new inference or corpus extraction.",
        "limits": ["Exploratory selected examples; agreement is not thematic correctness.",
                   "Source label errors remain documented; no external semantic validation.",
                   "Public deposit, authorship declarations and manuscript remain future work.",
                   "QSS indexed guidance and literature require refresh before submission."],
    }
    (REVIEW / "closure_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"current_documents", "review_evidence"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
