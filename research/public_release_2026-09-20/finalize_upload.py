"""Archive an explicit Git commit and inventory the already verified data delivery."""
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/zenodo"
HERE = Path(__file__).resolve().parent


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024**2), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit", help="Explicit reviewed Git commit; never a working tree")
    args = parser.parse_args()
    commit = subprocess.check_output(
        ["git", "rev-parse", args.commit + "^{commit}"], cwd=ROOT, text=True
    ).strip()
    archive = OUT / "shape-of-science-code-v1.0.0.zip"
    if archive.exists():
        raise SystemExit("Code archive already exists; preserve it and inspect before replacing.")
    subprocess.run(
        ["git", "archive", "--format=zip", "--output=" + str(archive), commit],
        cwd=ROOT, check=True,
    )
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert "reproducibility/reproduce_summaries.py" in z.namelist()
        assert "reproducibility/check_vectors.py" in z.namelist()
        assert not any(n.startswith(("data/", ".benchmark-models/", "output/zenodo/")) for n in z.namelist())
        code_files = len([n for n in z.namelist() if not n.endswith("/")])
    version = {
        "version": "1.0.0", "git_commit": commit,
        "repository": "https://github.com/aleetreny/Shape-of-Science-Robustness",
        "commit_url": "https://github.com/aleetreny/Shape-of-Science-Robustness/commit/" + commit,
        "archive": archive.name, "sha256": sha256(archive),
        "bytes": archive.stat().st_size, "files": code_files,
        "license": "MIT for original software; see LICENSING.md for documents and third parties",
        "data_record_doi": "10.5281/zenodo.22863543",
        "data_record_status_at_packaging": "draft, DOI reserved; no public data access yet",
    }
    (OUT / "CODE_VERSION.json").write_text(json.dumps(version, indent=2) + "\n")
    data = json.loads((OUT / "DATA_MANIFEST.json").read_text())
    known = {x["archive"]: x for x in data["archives"]}
    lines = []
    for path in sorted(OUT.iterdir()):
        if path.name in {"SHA256SUMS", "UPLOAD_FILES.txt"}:
            continue
        if path.name in known:
            assert path.stat().st_size == known[path.name]["archive_bytes"]
            # These 19 hashes and every member were verified by verify_archives --full.
            checksum = known[path.name]["archive_sha256"]
        else:
            checksum = sha256(path)
        lines.append(checksum + "  " + path.name)
    (OUT / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    list_path = OUT / "UPLOAD_FILES.txt"
    list_path.write_text("")
    for _ in range(8):
        files = sorted(OUT.iterdir())
        total = sum(p.stat().st_size for p in files)
        content = (
            "Upload every file listed below, without extracting the ZIPs.\n"
            "Destination: https://zenodo.org/uploads/22863543\n"
            "Version: 1.0.0; DOI reserved, not published at packaging time.\n"
            f"Files: {len(files)}; total bytes (including this list): {total}\n"
            "19 data ZIPs + one code ZIP + documentation and integrity records.\n"
            "SHA256SUMS covers all payloads except itself and this list.\n\n"
            + "\n".join(f"{p.stat().st_size:>14}  {p.name}" for p in files) + "\n"
        )
        previous_size = list_path.stat().st_size
        list_path.write_text(content)
        if list_path.stat().st_size == previous_size:
            break
    files = sorted(OUT.iterdir())
    summary = {
        "files": len(files), "bytes": sum(p.stat().st_size for p in files),
        "data_archives": len(known), "code_version": version,
        "upload_files": [{"name": p.name, "bytes": p.stat().st_size} for p in files],
        "data_hashes": "reused from the completed full decompressed-file verification",
        "new_code_zip_crc_verified": True,
    }
    (HERE / "upload_inventory.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ["files", "bytes", "data_archives"]}))


if __name__ == "__main__":
    main()
