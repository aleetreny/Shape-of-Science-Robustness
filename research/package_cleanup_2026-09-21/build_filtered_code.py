"""Create a scientific code distribution without manuscripts or internal work records.

Read only from the previously verified Git archive. Numerical archives and original
manuscript files are never modified. Record every delivered member's hash.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "output/zenodo"
BASE = ROOT / "data/public_release_history/2026-09-20"
NAME = "shape-of-science-code-v1.0.0-data-only.zip"

ROOT_FILES = set("""
ACADEMIC_MODEL_USAGE.md ANALYSIS_PROTOCOL.md ANALYSIS_RESULTS.md
CASE_ATLAS.md CASE_ATLAS_PROTOCOL.md CHECKLIST_PROTOCOL.md CHECKLIST_RESULTS.md
CITATION.cff CLEANING.md CONCLUSION_CONTROLS.md CORPUS_BALANCE.md CORPUS_PROTOCOL.md
DATA_CATALOG.md DOWNLOAD.md EMBEDDINGS.md EMBEDDINGS_AUDIT.md EMBEDDINGS_READY.md
FIELD_COUNTS.csv FIELD_PAIR_PROTOCOL.md FIELD_PAIR_RESULTS.md LICENSE LICENSING.md
METHODS_ANALYSIS.md METHODS_CHECKLIST.md METHODS_FIELD_PAIRS.md METHODS_MORPHOLOGY.md
METHODS_ROBUSTNESS.md METRICS.md MODEL_FAMILIES.md MODEL_SELECTION.md
MORPHOLOGY_PROTOCOL.md MORPHOLOGY_RESULTS.md POOLING.md PREPAPER_REVIEW.md
ROBUSTNESS_CLOSURE_PROTOCOL.md ROBUSTNESS_CLOSURE_REPORT.md ROBUSTNESS_CLOSURE_SCOPE.md
ROBUSTNESS_PROTOCOL.md ROBUSTNESS_RESULTS.md ROBUSTNESS_SCOPE.md SAMPLING_STABILITY.md
SCALES_AND_DISCIPLINES.md TEMPORAL_REVIEW.md
download.sh embed.sh prepare.sh start_embeddings.sh requirements-analysis.txt
requirements-audit.txt requirements-embeddings.txt requirements-preparation.txt requirements.txt
""".split())
ROOT_DIRS = {"config", "reports", "references", "reproducibility", "tests", "scripts"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def selected(name):
    top = name.split("/")[0]
    return name in ROOT_FILES or top in ROOT_DIRS or top.startswith("sos_")


def main():
    previous = json.loads((BASE / "CODE_VERSION.json").read_text())
    destination = OUT / NAME
    if destination.exists():
        raise SystemExit("Preserve the existing filtered archive before rebuilding.")
    content, originals, excluded = {}, {}, []
    with zipfile.ZipFile(BASE / previous["archive"]) as src:
        for item in src.infolist():
            if item.is_dir():
                continue
            if not selected(item.filename):
                excluded.append(item.filename)
                continue
            content[item.filename] = src.read(item)
            originals[item.filename] = sha(content[item.filename])
    # A technical guide in the original snapshot linked private work instructions.
    # Only the exported documentation changes; the original remains intact.
    name = "DOWNLOAD.md"
    doc = content[name].decode()
    old = "Leer `AGENTS.md`, `DECISIONS.md`, `progress.md` y `CORPUS_PROTOCOL.md`."
    assert old in doc
    content[name] = doc.replace(old, "Consultar `CORPUS_PROTOCOL.md` para las reglas del corpus.", 1).encode()
    for name in ["reproducibility/README.md", "reproducibility/DATA_DICTIONARY.md"]:
        content[name] = (ROOT / name).read_bytes()
    # The distribution has its own entry page, with links valid inside this ZIP.
    content["README.md"] = (OUT / "README.md").read_bytes()
    meta = {
        "source_git_commit": previous["git_commit"],
        "source_repository": previous["repository"],
        "distribution": "Scientific code, protocols, numerical reports and reproduction guides only",
        "excluded_scope": "Manuscripts, supplements, editorial archives and internal work records",
        "source_code_and_numerical_files": "Byte-identical to the source snapshot",
        "documentation_overrides": ["README.md", "DOWNLOAD.md", "reproducibility/README.md", "reproducibility/DATA_DICTIONARY.md"],
        "members": [{"path": n, "bytes": len(b), "sha256": sha(b)} for n, b in sorted(content.items())],
    }
    content["PACKAGE_MANIFEST.json"] = (json.dumps(meta, indent=2) + "\n").encode()
    for name in content:
        assert Path(name).suffix.lower() not in {".tex", ".zip", ".docx", ".doc", ".log"}, name
        assert not any(part in {"manuscript", "manuscript_es", "manuscript_variants", "research", "output"} for part in Path(name).parts), name
        assert Path(name).name != "AGENTS.md", name
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as dst:
        for name, data in sorted(content.items()):
            info = zipfile.ZipInfo(name, (2026, 9, 21, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            executable = name.endswith(".sh")
            info.external_attr = (0o100755 if executable else 0o100644) << 16
            dst.writestr(info, data)
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        for item in meta["members"]:
            assert sha(z.read(item["path"])) == item["sha256"]
    scientific = {n: h for n, h in originals.items() if n not in meta["documentation_overrides"]}
    assert all(sha(content[n]) == h for n, h in scientific.items())
    version = {
        **previous, "archive": NAME, "sha256": sha(destination.read_bytes()),
        "bytes": destination.stat().st_size, "files": len(content),
        "export_type": "Filtered scientific distribution; not a full repository mirror",
        "package_revision_date": "2026-09-21",
        "excluded_scope": meta["excluded_scope"],
        "manifest": "PACKAGE_MANIFEST.json inside the code ZIP",
        "documentation_overrides": meta["documentation_overrides"],
    }
    (OUT / "CODE_VERSION.json").write_text(json.dumps(version, indent=2) + "\n")
    report = {
        "source_archive": previous["archive"], "source_commit": previous["git_commit"],
        "new_archive": NAME, "included_files": len(content),
        "excluded_files": excluded, "unchanged_selected_files": len(scientific),
        "original_manuscripts_preserved": True, "zip_crc_verified": True,
        "member_checksums_verified": True, "code_version": version,
    }
    (HERE / "filtered_code_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"archive": NAME, "files": len(content), "excluded_files": len(excluded), "bytes": destination.stat().st_size}))


if __name__ == "__main__":
    main()
