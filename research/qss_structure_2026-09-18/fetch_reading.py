"""Fetch public reading copies; keep all third-party text under ignored data/."""
import hashlib
import io
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/qss_structure_review_v1"


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "div", "section", "h1", "h2", "h3", "h4", "li", "br"):
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag in ("p", "div", "section", "h1", "h2", "h3", "h4", "li"):
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def main():
    queue = json.loads(Path(sys.argv[1]).read_text())
    out = DATA / "texts"
    out.mkdir(exist_ok=True)
    logpath = DATA / "download_log.json"
    log = json.loads(logpath.read_text()) if logpath.exists() else []
    for item in queue:
        if any(x.get("url") == item["url"] and x.get("ok") for x in log):
            continue
        record = dict(item, retrieved_at=datetime.now(timezone.utc).isoformat())
        try:
            req = urllib.request.Request(item["url"], headers={"User-Agent": "Academic literature reading/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read(30_000_000)
                record.update(final_url=response.url, status=response.status)
            pdf = content.startswith(b"%PDF")
            suffix = ".pdf" if pdf else ".html"
            rawpath = out / (item["id"] + suffix)
            rawpath.write_bytes(content)
            if pdf:
                pages = PdfReader(io.BytesIO(content)).pages
                text = "\n\n".join(f"[PDF page {i+1}]\n{p.extract_text()}" for i, p in enumerate(pages))
                record["pages"] = len(pages)
            else:
                parser = TextParser()
                parser.feed(content.decode("utf-8", errors="replace"))
                text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines() if line.strip())
            txtpath = out / (item["id"] + ".txt")
            txtpath.write_text(text)
            record.update(ok=True, format="pdf" if pdf else "html", raw_path=str(rawpath.relative_to(ROOT)), text_path=str(txtpath.relative_to(ROOT)), bytes=len(content), chars=len(text), sha256=hashlib.sha256(content).hexdigest())
            print(item["id"], record["format"], record.get("pages"), len(text), flush=True)
        except Exception as error:
            record.update(ok=False, error=str(error))
            print(item["id"], str(error), flush=True)
        log.append(record)
        logpath.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n")
        if "arxiv.org" in item["url"]:
            time.sleep(3)


if __name__ == "__main__":
    main()
