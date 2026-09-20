"""Assemble complete review alternatives from the preserved draft and hand-written edits.

This only changes presentation text. No scientific program is imported or executed.
Run explicitly to regenerate sources; build.py alone preserves any direct source edits.
"""
from pathlib import Path
import json
import re
import runpy

HERE = Path(__file__).resolve().parent
NAMES = {
    "en": {1: "Direct and restrained", 2: "Author reasoning", 3: "Distinctive and reflective"},
    "es": {1: "Directa y sobria", 2: "Razonamiento propio", 3: "Voz marcada y reflexiva"},
}


def prose_positions(lines):
    return [i for i, line in enumerate(lines)
            if line and not line.startswith(("\\", "%", "{", "Independent", "Investigador"))
            and not line.endswith(r"\par")]


def main():
    records = {}
    for version in (1, 2, 3):
        for language in ("en", "es"):
            key = f"v{version}_{language}"
            source = (HERE / "base" / language / "main.tex").read_text()
            lines = source.splitlines()
            positions = prose_positions(lines)
            assert len(positions) == 58
            edits = runpy.run_path(str(HERE / "edits" / f"{key}.py"))["EDITS"]
            assert all(0 <= index <= 52 and index != 10 for index in edits)
            for index, paragraph in edits.items():
                assert "\n" not in paragraph
                lines[positions[index]] = paragraph
            result = "\n".join(lines) + "\n"
            name = NAMES[language][version]
            if language == "en":
                label = f"Voice option {version}: {name}"
                result = result.replace("Manuscript draft \\textbullet{} 18 September 2026",
                                        label + r" \textbullet{} 19 September 2026")
                header = f"Voice option {version}"
            else:
                label = f"Opción {version}: {name}"
                result = result.replace("Versión española para revisión personal \\textbullet{} 18 de septiembre de 2026",
                                        label + r" \textbullet{} 19 de septiembre de 2026")
                header = f"Opción de voz {version}"
            result = result.replace(r"\begin{document}",
                                    r"\fancyhead[R]{\small " + header + "}\n" +
                                    r"\hypersetup{pdfsubject={" + label + "}}\n" +
                                    r"\begin{document}", 1)
            target = HERE / "versions" / key / "main.tex"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(result)
            records[key] = {"language": language, "version": version, "name": name,
                            "edited_paragraph_indices": sorted(edits),
                            "edited_paragraphs": len(edits),
                            "complete_main_article": True,
                            "supplement": f"base/{language}/supplement.tex",
                            "source": str(target.relative_to(HERE)),
                            "first_paragraph": edits[1],
                            "discussion_opening": edits[43]}
    (HERE / "variants.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    print(f"Prepared {len(records)} complete article sources.")


if __name__ == "__main__":
    main()
