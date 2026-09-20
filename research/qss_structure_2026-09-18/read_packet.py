"""Print bounded structural reading packets, with offsets for deeper follow-up."""
import json
import re
import sys
from pathlib import Path

data = Path("data/qss_structure_review_v1")
index = json.loads((data / "reading_index.json").read_text())
for ident in sys.argv[1:]:
    x = next(x for x in index if x["study_id"] == ident or x["id"] == ident)
    print("\nARTICLE", x["study_id"], x["title"], x["authors"], x["year"])
    if not x["has_reading_copy"]:
        print("NO VERIFIED FULL COPY")
        continue
    t = Path(x["text_path"]).read_text()
    # Markdown headings are strongest; plain-text PDF headers are candidate labels only.
    matches = list(re.finditer(r"(?m)^(?:#{1,6}[ \t]*)?([1-9](?:\.\d+)*\.?[ \t\u2003]+[A-Za-z][^\n]{1,145})[ \t]*$", t))
    if "## " in t:
        heads = [(m.start(),m[1]) for m in re.finditer(r"(?m)^#{2,6}\s+([^\n]+)", t) if re.match(r"\d+\.?\s|\d+\.\d",m[1])]
    else:
        heads = [(m.start(),m[1]) for m in matches]
    print("HEADINGS", json.dumps(heads[:60], ensure_ascii=False))
    intro = [(p,h) for p,h in heads if re.match(r"1\.?\s+INTRODUCTION",h,re.I)]
    pos = intro[-1][0] if intro else 0
    print("INTRO START", t[pos:pos+1100])
    main = [(p,h) for p,h in heads if re.match(r"[2-9]\.?\s+[A-Z]",h,re.I)]
    ends = [(p,h) for p,h in main if re.search(r'discussion|conclusion|limitation|summary',h,re.I)]
    for p,h in ends[-3:]:
        q = next((p2 for p2,h2 in heads if p2>p and re.match(r"\d\.?\s+[A-Z]",h2,re.I)),len(t))
        s = t[p:q]
        s = re.split(r"(?mi)^#{0,4}\s*(?:AUTHOR CONTRIBUTIONS|ACKNOWLEDGMENTS|REFERENCES|COMPETING INTERESTS)\s*$",s)[0]
        print("END SECTION",h,"offset",p,"length",len(s),s[:2100])
    for p,h in main:
        if not re.search(r'discussion|conclusion|limitation|summary',h,re.I):
            print("SECTION OPEN",h,t[p:p+350])
