"""Compile the six article alternatives using their common, preserved presentation assets."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=[f"v{v}_{lang}" for v in (1, 2, 3) for lang in ("en", "es")])
    parser.add_argument("--output-dir", type=Path, default=HERE.parent / "output/pdf/voice_variants")
    parser.add_argument("--compiler", type=Path)
    args = parser.parse_args()
    compiler = args.compiler or HERE.parent / "data/manuscript_layout_v1/toolchain/tectonic"
    if not compiler.is_file():
        found = shutil.which("tectonic")
        if not found:
            parser.error("Tectonic is required; pass --compiler or install it on PATH.")
        compiler = Path(found)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "logs").mkdir(exist_ok=True)
    records = json.loads((HERE / "variants.json").read_text())
    environment = dict(os.environ, SOURCE_DATE_EPOCH="1789776000")
    for key, record in records.items():
        if args.only and key != args.only:
            continue
        with tempfile.TemporaryDirectory(prefix=f"science-voice-{key}-") as temp:
            stage = Path(temp) / "source"
            shutil.copytree(HERE / "base" / record["language"], stage)
            shutil.copy2(HERE / record["source"], stage / "main.tex")
            build = Path(temp) / "build"
            build.mkdir()
            result = subprocess.run([str(compiler.resolve()), "--keep-logs", "--outdir", str(build), "main.tex"],
                                    cwd=stage, env=environment, text=True, capture_output=True)
            (output / "logs" / f"{key}_compile.txt").write_text(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(f"{key}: compilation failed; see {output / 'logs'}")
            shutil.copy2(build / "main.pdf", output / f"{key}.pdf")
            shutil.copy2(build / "main.log", output / "logs" / f"{key}.log")
            print(f"{key}: {output / (key + '.pdf')}", flush=True)


if __name__ == "__main__":
    main()
