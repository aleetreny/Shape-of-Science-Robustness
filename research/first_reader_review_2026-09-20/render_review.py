"""Render every delivered PDF and assemble page contact sheets for inspection."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "tmp/pdfs/first_reader_review"
POPPLER = "/Users/alejandrotreny/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm"
OUT.mkdir(parents=True, exist_ok=True)
manifest_path=HERE / 'render_manifest.json'
report = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for key, relative in [("en_main", "output/pdf/main.pdf"), ("es_main", "output/pdf/es/main.pdf"),
                      ("en_supplement", "output/pdf/supplement.pdf"), ("es_supplement", "output/pdf/es/supplement.pdf")]:
    if sys.argv[1:] and key not in sys.argv[1:]:
        continue
    pdf = ROOT / relative
    destination = OUT / key
    destination.mkdir(exist_ok=True)
    for old in [*destination.glob("page-*.png"), *destination.glob("sheet-*.jpg")]:
        old.unlink()
    subprocess.run([POPPLER, "-r", "96", "-png", str(pdf), str(destination / "page")], check=True, capture_output=True)
    images = sorted(destination.glob("page-*.png"))
    assert len(images) == len(PdfReader(pdf).pages)
    sheets = []
    for start in range(0, len(images), 4):
        selected = images[start:start+4]
        cell_w, cell_h = 816, 1092
        sheet = Image.new("RGB", (cell_w * 2, cell_h * 2), "#e2e4e7")
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(selected):
            picture = Image.open(path).convert("RGB")
            picture.thumbnail((cell_w-12, cell_h-34))
            x, y = (j % 2) * cell_w, (j // 2) * cell_h
            sheet.paste(picture, (x+(cell_w-picture.width)//2, y+27))
            draw.text((x+12, y+8), f"{key} - page {start+j+1}", fill="black")
        target = destination / f"sheet-{start//4+1:02d}.jpg"
        sheet.save(target, quality=86)
        sheets.append(str(target))
    report[key] = {"pdf": relative, "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                   "pages": len(images), "renders": [str(p) for p in images], "sheets": sheets}
(HERE / "render_manifest.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({k: {"pages": v["pages"], "sheets": len(v["sheets"])} for k,v in report.items()}))
