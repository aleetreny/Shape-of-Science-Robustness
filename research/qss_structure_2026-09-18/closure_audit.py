"""Check delivery integrity; does not assess rhetoric or rerun science."""
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
DATA = ROOT / "data/qss_structure_review_v1"

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    target = HERE / "closure_audit.json"
    target.write_text(json.dumps(dict(all_complete=False, state="checking"))+"\n")
    catalog = read(DATA / "crossref_journal.json")
    assert catalog["reconciliation"]["complete"]
    assert catalog["reconciliation"]["expected_total"] == len(catalog["records"]) == 465
    inventory = read(HERE / "journal_inventory.json")
    matrix = read(HERE / "article_matrix.json")
    raw = read(DATA / "selected_crossref.json")
    assert len(matrix) == len(raw) == 34
    dois = {x["doi"].lower() for x in matrix}
    assert len(dois) == 34 and dois <= {x["doi"].lower() for x in inventory}
    assert dois == {x["DOI"].lower() for x in raw}
    assert all(x["container-title"][0] == "Quantitative Science Studies" for x in raw)
    coverage = read(HERE / "coverage.json")
    assert coverage["full_reading_copies"] == 33
    assert coverage["depth"] == dict(estructural=22, focal=11, parcial=1)
    with (HERE / "article_matrix.csv").open() as f: csv_rows=list(csv.DictReader(f))
    assert len(csv_rows)==34 and {x["doi"] for x in csv_rows}==dois
    readings=read(DATA / "reading_index.json")
    for x in readings:
        if x["has_reading_copy"]: assert sha(ROOT/x["text_path"])==x["text_sha256"]
    q25=next(x for x in readings if x["study_id"]=="Q25")
    assert not q25["has_reading_copy"] and any(x["rejected_wrong_body"] for x in q25["alternatives"])
    bib=read(HERE / "bib_validation.json")
    assert bib["total_entries"]==34 and not bib["errors"] and not bib["duplicates"]
    assert len(bib["warnings"])==1 and bib["warnings"][0]["entry"]=="QSSreviewQ34"

    baseline=read(HERE / "baseline_manifest.json")
    for name, digest in baseline["documents"].items(): assert sha(HERE/"baseline_documents"/name)==digest,name
    preceding=ROOT/"research/field_pair_summary_2026-09-18/closure_audit.json"
    assert sha(preceding)==baseline["closure_sha256"]
    previous=read(preceding)
    for name,digest in previous["evidence_hashes"].items(): assert sha(ROOT/name)==digest,name
    morphology=read(ROOT/"research/morphology_2026-09-18/closure_audit.json")
    for name,digest in morphology["evidence_hashes"].items(): assert sha(ROOT/name)==digest,name
    checked_sources=set(); checked_parents=set(); checked_reports=[]
    for version in ["morphology_pilot_v1","field_pair_summary_v1"]:
        manifest=read(ROOT/"data"/version/"manifest.json")
        for name,digest in manifest["source_files"].items():
            assert sha(ROOT/name)==sha(ROOT/"data"/version/"source_snapshot"/name)==digest,name
            checked_sources.add(name)
        for name,digest in manifest["parent_files"].items():
            assert sha(ROOT/name)==digest,name; checked_parents.add(name)
        c=read(ROOT/"reports"/version/"catalog.json")
        for name,digest in c["files"].items():
            assert sha(ROOT/"reports"/version/name)==digest,name; checked_reports.append(f"{version}/{name}")
    frozen_docs=["FIELD_PAIR_PROTOCOL.md","FIELD_PAIR_RESULTS.md","METHODS_FIELD_PAIRS.md",
                 "MORPHOLOGY_PROTOCOL.md","MORPHOLOGY_RESULTS.md","METHODS_MORPHOLOGY.md"]
    for name in frozen_docs: assert sha(ROOT/name)==baseline["documents"][name],name

    docs=[ROOT/n for n in ["QSS_STRUCTURE_REVIEW.md","PAPER_OUTLINE.md","AGENTS.md","NEXT_STEPS.md",
         "README.md","DATA_CATALOG.md","DECISIONS.md","progress.md","findings.md","task_plan.md",
         "docs/INDEX.md","docs/QSS_CHECK.md","references/README.md","references/RELATED_WORK.md"]]
    docs += [HERE/"READING_NOTES.md",HERE/"retrieval_protocol.md"]
    broken=[]; links=0
    for p in docs:
        for dest in re.findall(r"\]\(([^)]+)\)",p.read_text()):
            dest=dest.strip().split(' "')[0].strip('<>')
            if not dest or dest.startswith('#') or urlsplit(dest).scheme: continue
            links+=1
            if not (p.parent/unquote(dest.split('#')[0].split('?')[0])).exists():
                broken.append(dict(file=str(p.relative_to(ROOT)),target=dest))
    assert not broken,broken
    subprocess.run(["git","diff","--check"],cwd=ROOT,check=True)
    assert subprocess.run(["git","check-ignore","-q",str(DATA/"reading_index.json")],cwd=ROOT).returncode==0
    assert not subprocess.check_output(["git","ls-files","data/qss_structure_review_v1"],cwd=ROOT).strip()
    active=[]
    for line in subprocess.check_output(["ps","-axo","pid=,command="]).decode().splitlines():
        if re.search(r"python\S*\s+-m\s+sos_(?:embed|download|morphology|pair_summary|deep|followup)\.(?:run|analyze|parallel_run|download|input_embeddings)\b",line):
            active.append(line.strip().split(maxsplit=1)[0])
    assert not active,active
    evidence=[HERE/n for n in ["article_matrix.json","article_matrix.csv","READING_NOTES.md","curated_notes.json",
        "qss_review.bib","bib_validation.json","coverage.json","journal_inventory.json","build_review.py","closure_audit.py"]]
    evidence += [DATA/"selected_crossref.json",DATA/"reading_index.json",DATA/"crossref_journal.json",DATA/"official_guide_indexed.json"]
    result=dict(all_complete=True,created_at=datetime.now(timezone.utc).isoformat(),
        journal_metadata_records=465,selected_articles=34,structural_readings=33,focal_readings_within_33=11,partial_readings=1,
        version_counts=coverage["version_groups"],canonical_bibliography_unchanged=True,
        review_bibliography=dict(entries=34,errors=0,duplicates=0,warnings=1),
        prior_closure_unchanged=True,baseline_documents_verified=len(baseline["documents"]),
        scientific_source_files_verified=len(checked_sources),parent_files_verified=len(checked_parents),
        previous_report_files_verified=len(checked_reports),scientific_documents_unchanged=frozen_docs,
        local_links_checked=links,broken_links=broken,third_party_text_ignored_by_git=True,
        active_calculations=active,git_head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip(),
        evidence_hashes={str(p.relative_to(ROOT)):sha(p) for p in evidence},
        current_documents={str(p.relative_to(ROOT)):sha(p) for p in docs},
        scope="Metadata, recorded reading coverage, document links and artifact integrity. Manual interpretive review, not full-text exhaustive review, replication, editorial endorsement or proof of optimality.")
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in {"evidence_hashes","current_documents"}},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
