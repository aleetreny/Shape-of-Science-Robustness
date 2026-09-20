"""Index reading copies, without treating metadata or downloads as completed reading."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/qss_structure_review_v1"
metadata = json.loads((DATA / "selected_crossref.json").read_text())
urlmap = {x["resource"]["primary"]["URL"]: x["DOI"].split("/")[-1] for x in metadata}
arxiv = {"1901.05273": "qss_a_00004", "1908.09120": "qss_a_00006", "1810.00577": "qss_a_00011", "2001.02733": "qss_a_00014", "1901.06815": "qss_a_00035", "2005.10732": "qss_a_00112", "2007.15254": "qss_a_00108", "2212.12263": "qss_a_00267", "2308.15706": "qss_a_00349", "2309.14984": "qss.a.9", "2406.15154": "qss.a.406", "2601.15062": "qss.a.506", "2302.00390": "qss.a.2"}
urlmap.update({"https://oro.open.ac.uk/103702/8/103702final.pdf": "qss_a_00363", "https://unipub.lib.uni-corvinus.hu/11909/1/qss.a.13.pdf": "qss.a.13"})
out = DATA / "reading"
out.mkdir(exist_ok=True)
copies = {}
for p in sorted(DATA.glob("exa_*.json")):
    t = "\n".join(x.get("text", "") for x in json.loads(p.read_text()).get("content", []))
    for seg in re.split(r"(?m)(?=^# [^\n]+\nURL: )", t):
        m = re.match(r"# ([^\n]+)\nURL: ([^\n]+)\n", seg)
        if not m:
            continue
        title, url = m.groups()
        ident = urlmap.get(url)
        doi = re.search(r"10\.1162/((?:qss_a_|qss\.a\.)\d+)", url, re.I)
        if doi:
            ident = doi[1].lower()
        if "arxiv.org" in url:
            aid = re.search(r"\d{4}\.\d{4,5}", url)
            ident = arxiv.get(aid[0]) if aid else None
        if "/1/4/1570/96116/" in url:
            ident = "qss_a_00085"
        if "/1/1/277/15560/" in url:
            ident = "qss_a_00006"
        if not ident:
            continue
        seg = re.split(r"\nError fetching ", seg)[0]
        invalid = ident == "qss_a_00357" and "Historical development and global standings" in seg
        copies.setdefault(ident, []).append(dict(url=url, raw=str(p.relative_to(ROOT)), text=seg, title=title, rejected_wrong_body=invalid, kind="publisher_html" if "direct.mit.edu" in url and "article-pdf" not in url else "reading_copy"))
for x in json.loads((DATA / "download_log.json").read_text()):
    if x.get("ok") and x.get("chars", 0) > 10000:
        copies.setdefault(x["id"], []).append(dict(url=x["url"], raw=x["raw_path"], text=(ROOT/x["text_path"]).read_text(), title="", rejected_wrong_body=False, kind=x["version"]))
index = []
for n, x in enumerate(metadata, 1):
    ident = x["DOI"].split("/")[-1]
    candidates = [c for c in copies.get(ident, []) if not c["rejected_wrong_body"] and len(c["text"]) > 10000]
    # Prefer verified identity later; this is an acquisition index, not automatic validation.
    candidates.sort(key=lambda c: (c["kind"] == "publisher_html", "article-pdf" in c["url"], len(c["text"])), reverse=True)
    chosen = candidates[0] if candidates else None
    entry = dict(study_id=f"Q{n:02}", id=ident, doi=x["DOI"], title=" ".join(" ".join(x["title"]).split()), year=x["published"]["date-parts"][0][0], authors=", ".join(a.get("family", "") for a in x.get("author", [])), has_reading_copy=bool(chosen), alternatives=[{k:v for k,v in c.items() if k!="text"} for c in copies.get(ident, [])])
    if chosen:
        path = out/(ident+".txt")
        path.write_text(chosen["text"])
        entry.update(source=chosen["url"], kind=chosen["kind"], text_path=str(path.relative_to(ROOT)), chars=len(chosen["text"]), text_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    index.append(entry)
(DATA/"reading_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2)+"\n")
for x in index:
    print(x["study_id"],x["id"],x.get("chars",0),x.get("kind","NO FULL TEXT"),x["title"][:85])
