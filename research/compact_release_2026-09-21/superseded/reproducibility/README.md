# Reproduce and inspect this release

Version 1.0.0, 20 September 2026. The accompanying numerical release contains **58,201 files in 19 ZIP archives (51,143,981,543 compressed bytes)**. It preserves frozen vectors, selections, candidate/query identities, per-condition measurements, controls and source snapshots. The public data deposit is **not yet published**. DOI `10.5281/zenodo.22863543` is reserved for its draft, not an available download. Code and data will be archived together in this versioned record, with separate licensing scopes. The code distribution was revised on 21 September 2026: it includes scientific programs, protocols, numerical reports and reproduction guides; manuscripts, supplements in either language, earlier manuscript copies and internal work records are excluded. The repository can continue to develop the article independently.

## Start without downloading vectors

From a repository checkout or the code ZIP, with Python 3.12 or later:

```sh
python3 -I -S reproducibility/reproduce_summaries.py
```

Only the Python standard library is needed; there is no network access. This recalculates repeated-centre means, all 217 matched search-scope summaries, repeated text/model-change means, eight area-pair classifications and retention of the same opposing models. The inputs are per-condition measurements, not the final displayed numbers. Expected results are separate frozen publication tables. Absolute tolerance is `1e-12`; integer classifications/counts must match exactly.

This checks aggregation for the four main figures. It does not regenerate embeddings or all upstream geometric measurements. `figure4/` also runs independently with `python3 -I -S reproduce.py`.

## Check the numerical downloads

Keep `DATA_MANIFEST.json` beside all 19 data ZIPs. Do not unzip them for these checks:

```sh
python3 -I -S reproducibility/verify_archives.py /path/to/downloads --full
```

The command verifies archive SHA-256 hashes and every individual decompressed file. Each archive contains its own `ARCHIVE_MANIFEST.json`; the global manifest identifies all files and their provenance. Archive extraction should preserve relative paths. Do not extract over an existing research checkout. The ZIPs include historical results and manifests; rerunning a historical coordinator against them may skip finished work and is not a new reproduction.

## Recalculate fixed checks from the vectors

Use a new Python 3.12 environment and the pinned analysis requirements. This does not need PyTorch, model weights, a GPU, plaintext abstracts or an OpenAlex account.

```sh
python3.12 -m venv .venv-reproduce
.venv-reproduce/bin/python -m pip install -r requirements-analysis.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv-reproduce/bin/python -I reproducibility/check_vectors.py \
  /path/to/downloads --output vector_checks.json
```

This independent program reads the ZIPs directly, verifies each file it uses, and recomputes:

| Figure | Fixed calculation checked |
| --- | --- |
| 1 | All ten models; repeat 0 of the 26-Field and 217-Subfield centres, observed and random groups; 40 centre arrays and 180 model-pair CKA values. |
| 2 | Subfield 1100, repeat 0; both 256-candidate scopes, 50 identical queries, all 45 model pairs and lists of 10/25/50; 13,500 exact intersection counts. |
| 3 | Field 11, repeat 0; 1,000 candidates, all 36 model/input/pooling representations and five recipe/list-size contrasts. |
| 4 | Field 11 in all ten models; primary, half 0 and external 0 selections; original and centred representations: 60 geometry cases, plus entropy and D80 for originals. |

The numerical tolerance was fixed at `1e-8` before this check. The maximum observed error was `1.28e-12`; all integer checks agreed. It completed in about 70 seconds in the existing Python 3.12 analysis environment on the author's Apple Silicon computer. This is a measured local run, not a time or portability guarantee for other computers. Allow several GB of RAM and about 52 GB of disk for compressed files. Full extraction requires additional disk space.

## What this release does and does not establish

These checks passed directly from the archives, with no imports of the original scientific programs. The compact check also passed from an isolated temporary directory. All archived files passed decompressed checksum validation.

The bounded vector checks do **not** repeat every condition or every supplementary analysis. The release retains their numerical inputs, outputs and frozen source snapshots so they can be inspected and extended; the historical executors are not all portable one-command entry points. A clean, complete rerun of every original analysis has not been certified. Re-running inference from historical text is outside this public route.

Historical title/abstract input tables are omitted because redistribution rights to plaintext abstracts have not been established. Non-text columns, IDs and hashes are exported under `public_metadata/`, deliberately at different paths: they are not byte-identical substitutes for the historical inputs. The corpus has not been replaced by a fresh OpenAlex query. `DATA_EXCLUSIONS.json` lists the omissions and replacements; `SCHEMAS.json` and `DATA_DICTIONARY.md` describe the data. Weights and third-party full-text publications are not included.

Original code is MIT. Original documents and numerical results are CC BY 4.0, within the author's rights. OpenAlex metadata retain CC0. See [licensing](../LICENSING.md) and [third-party provenance](THIRD_PARTY.md).

Before journal submission, publish the prepared record, verify its public files, and update the manuscript's availability statement and dataset citation. A reserved DOI alone does not satisfy public access.
