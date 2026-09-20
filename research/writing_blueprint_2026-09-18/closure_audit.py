"""Check writing-plan evidence and preservation, without rerunning research."""
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DATA = ROOT / "data/writing_blueprint_v1"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def main():
    baseline = read(HERE / "baseline_manifest.json")
    for name, digest in baseline["documents"].items():
        assert sha(HERE / "baseline_documents" / name) == digest, name
    preceding = ROOT / baseline["preceding_closure"]
    assert sha(preceding) == baseline["preceding_closure_sha256"]
    # Current planning documents changed deliberately; the recorded evidence did not.
    for name, digest in read(preceding)["evidence_hashes"].items():
        assert sha(ROOT / name) == digest, name
    preserved = set()
    for phase in ["morphology_2026-09-18", "field_pair_summary_2026-09-18"]:
        old = read(ROOT / "research" / phase / "closure_audit.json")
        for name, digest in old["evidence_hashes"].items():
            assert sha(ROOT / name) == digest, name
            preserved.add(name)
    scientific_sources, parents, reports = set(), set(), set()
    for version in ["morphology_pilot_v1", "field_pair_summary_v1"]:
        manifest = read(ROOT / "data" / version / "manifest.json")
        for name, digest in manifest["source_files"].items():
            assert sha(ROOT / name) == sha(ROOT / "data" / version / "source_snapshot" / name) == digest, name
            scientific_sources.add(name)
        for name, digest in manifest["parent_files"].items():
            assert sha(ROOT / name) == digest, name
            parents.add(name)
        for name, digest in read(ROOT / "reports" / version / "catalog.json")["files"].items():
            path = ROOT / "reports" / version / name
            assert sha(path) == digest, str(path)
            reports.add(str(path.relative_to(ROOT)))

    corpus = read(HERE / "author_corpus.json")
    provenance = read(HERE / "author_provenance.json")
    assert len(corpus) == 50 == len(rows(HERE / "author_corpus.csv"))
    assert len({x["slug"] for x in corpus}) == 50
    assert sum(x["words_es"] for x in corpus) == 12823
    assert all(x["status"] == "published" and x["read_status"] == "read_complete_spanish_narrative" for x in corpus)
    for name, digest in provenance["snapshot_hashes"].items():
        assert sha(DATA / "portfolio_snapshot" / name) == digest
        assert sha(Path("/Users/alejandrotreny/Documents/ChatGPT/Portfolio") / name) == digest
    original_entries = read(DATA / "portfolio_snapshot/fixtures/demo-content.json")
    assert [x["slug"] for x in original_entries] == [x["slug"] for x in corpus]
    notes = (HERE / "AUTHOR_READING_NOTES.md").read_text()
    assert all(f'| {x["slug"]} |' in notes for x in corpus)

    bib = read(HERE / "bib_validation.json")
    assert bib["total_entries"] == 4 and not bib["errors"] and not bib["duplicates"] and not bib["warnings"]
    blueprint = (ROOT / "MANUSCRIPT_BLUEPRINT.md").read_text()
    allocations = rows(HERE / "paragraph_plan.csv")
    found = re.findall(r"\*\*([IBMRDC]\d+) · (\d+)", blueprint)
    assert len(found) == len(allocations) == 48
    assert dict(found) == {x["paragraph"]: x["planned_words"] for x in allocations}
    assert sum(int(x["planned_words"]) for x in allocations) == 6750
    sums = {s: sum(int(x["planned_words"]) for x in allocations if x["section"] == s) for s in "123456"}
    assert list(sums.values()) == [800, 750, 1600, 2250, 1150, 200]
    displays = rows(HERE / "display_items.csv")
    assert len([x for x in displays if x["scope"] == "main"]) == 6
    assert len([x for x in displays if x["scope"] == "supplement"]) == 10
    assert all((ROOT / x["source"]).is_file() for x in displays)
    assert {x["after_paragraph"] for x in displays if x["scope"] == "main"} == {"M12", "M21", "R12", "R22", "R32", "R42"}
    assert len(rows(HERE / "table1_panels.csv")) == 6
    models = rows(HERE / "table2_models.csv")
    config_models = read(ROOT / "config/embeddings_v1.json")["models"]
    assert len(models) == len(config_models) == 10
    for row, model in zip(models, config_models):
        for target, source in [("repo_id", "repo_id"), ("revision", "revision"), ("dimension", "dimension"), ("native_max_tokens", "max_length"), ("text_format", "text_format")]:
            assert row[target] == str(model[source])
        expected = "mean" if model["key"] in {"bert", "scibert", "pubmedbert", "biobert"} else model["poolings"][0]
        assert row["primary_pooling"] == expected

    claims = read(HERE / "claim_evidence.json")
    assert len(claims) == 23 == len(rows(HERE / "claim_evidence.csv"))
    for claim in claims:
        source = ROOT / claim["source"]
        assert sha(source) == claim["source_sha256"]
        stored = json.loads(claim["values"])
        if claim["json_pointer"]:
            observed = read(source)
            for key in claim["json_pointer"].split("/"):
                observed = observed[int(key)] if isinstance(observed, list) else observed[key]
        else:
            filt = json.loads(claim["selector"])
            selected = [r for r in rows(source) if all(r[k] == v for k, v in filt.items())]
            assert len(selected) == 1
            observed = {k: selected[0][k] for k in stored}
        assert observed == stored
        cid = claim["claim_id"]
        if cid in {"E01", "E02"}:
            assert f"{stored * 100:.1f}%" == claim["displayed"]
        elif cid in {"E05", "E06", "E07"}:
            assert f'{float(stored["mean"]) * 100:.2f}%' == claim["displayed"]
        elif cid in {"E08", "E09", "E10"}:
            assert f'{float(stored["mean"]):.4f}' == claim["displayed"]
    keyed = {x["claim_id"]: json.loads(x["values"]) for x in claims}
    assert (keyed["E03"]["subfields_lower_agreement"], keyed["E03"]["subfields_higher_agreement"]) == ("127", "90")
    assert f'{float(keyed["E03"]["mean_difference"]) * 100:.2f}' == "-1.35"
    assert (keyed["E04"]["subfields_lower_agreement"], keyed["E04"]["subfields_higher_agreement"]) == ("109", "108")
    assert (keyed["E11"]["alerts26k"], keyed["E11"]["alerts52k"], keyed["E11"]["repeats"], keyed["E11"]["comparisons"]) == (72, 5, 100, 520)
    assert [int(keyed["E12"][k]) for k in ["unanimous", "contradiction", "unresolved"]] == [42, 262, 21]
    assert [int(keyed["E13"][k]) for k in ["unanimous", "contradiction", "unresolved"]] == [54, 221, 50]
    for cid, count in [("E14", 96), ("E15", 177), ("E16", 19), ("E17", 126), ("E20", 231), ("E21", 160)]:
        assert int(keyed[cid]["contradiction"]) == count
    assert (keyed["E18"]["contradiction_and_alternatives"], keyed["E19"]["contradiction_and_alternatives"]) == ("225", "196")
    assert (keyed["E22"]["same_original_witness_pair_retained"], keyed["E23"]["same_original_witness_pair_retained"]) == ("145", "218")

    bibliographies = [ROOT / "references/references.bib", ROOT / "research/qss_structure_2026-09-18/qss_review.bib"]
    available = set()
    for path in bibliographies:
        available.update(re.findall(r"@\w+\{([^,]+)", path.read_text()))
    keys = [x for x in re.findall(r"`([^`]+)`", blueprint) if x.startswith(("ref", "QSSreview")) and "…" not in x and x not in {"references.bib"}]
    assert all(k in available for k in keys), set(keys) - available

    names = ["MANUSCRIPT_BLUEPRINT.md", "AUTHOR_VOICE.md", "PAPER_OUTLINE.md", "AGENTS.md", "README.md", "NEXT_STEPS.md", "docs/INDEX.md", "DECISIONS.md", "progress.md", "findings.md", "task_plan.md"]
    docs = [ROOT / n for n in names] + [HERE / "STYLE_RESEARCH.md", HERE / "AUTHOR_READING_NOTES.md"]
    broken, checked = [], 0
    for path in docs:
        for dest in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            dest = dest.strip().split(' "')[0].strip("<>")
            if not dest or dest.startswith("#") or urlsplit(dest).scheme:
                continue
            checked += 1
            if not (path.parent / unquote(dest.split("#")[0].split("?")[0])).exists():
                broken.append(dict(file=str(path.relative_to(ROOT)), target=dest))
    assert not broken, broken
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    assert subprocess.run(["git", "check-ignore", "-q", str(DATA / "author_texts_es.txt")], cwd=ROOT).returncode == 0
    assert not subprocess.check_output(["git", "ls-files", "data/writing_blueprint_v1"], cwd=ROOT).strip()
    active = []
    for line in subprocess.check_output(["ps", "-axo", "pid=,command="]).decode().splitlines():
        if re.search(r"python\S*\s+-m\s+sos_(?:embed|download|morphology|pair_summary|deep|followup)\.(?:run|analyze|parallel_run|download|input_embeddings)\b", line):
            active.append(line.strip().split(maxsplit=1)[0])
    assert not active
    evidence = [p for p in HERE.iterdir() if p.is_file() and p.name != "closure_audit.json"]
    result = dict(
        all_complete=True, created_at=datetime.now(timezone.utc).isoformat(),
        author_entries_read=50, author_narrative_words=12823,
        voice_authorship_basis="User identification; no forensic authorship certification; Spanish repository snapshot, not live database",
        writing_primary_studies=4, bibliography=dict(entries=4, errors=0, duplicates=0, warnings=0),
        planned_paragraphs=48, planned_body_words=6750, section_word_totals=sums,
        main_tables=2, main_figures=4, supplementary_figure_bases=10, supplementary_tables_planned=17,
        numeric_evidence_rows_verified=23, main_model_rows_verified=10,
        prior_state_documents_preserved=len(baseline["documents"]), previous_closure_unchanged=True,
        prior_evidence_files_verified=len(preserved), scientific_source_files_verified=len(scientific_sources),
        parent_files_verified=len(parents), previous_report_files_verified=len(reports),
        canonical_bibliography_unchanged=True, portfolio_files_readonly_verified=len(provenance["snapshot_hashes"]),
        local_links_checked=checked, broken_links=broken, active_calculations=active,
        downloaded_fulltexts_ignored_by_git=True, manuscript_drafted=False,
        git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        evidence_hashes={str(p.relative_to(ROOT)): sha(p) for p in evidence},
        current_documents={str(p.relative_to(ROOT)): sha(p) for p in docs},
        scope="Document integrity, links, recorded reading coverage and saved numeric cells. Does not certify authorship, future prose quality, journal acceptance or thematic validity. No scientific rerun.")
    (HERE / "closure_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"evidence_hashes", "current_documents"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
