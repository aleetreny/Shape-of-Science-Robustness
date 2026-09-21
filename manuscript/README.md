# Final manuscript and supplementary material

The official English manuscript, approved by the author on 21 September 2026. English is the authoritative version for journal submission, preprinting and citation. The Spanish version is a professional translation for the author.

- `main.tex`: article, with author details, declarations and the public dataset citation.
- `supplement.tex`: supplementary methods, controls and tables.
- `preamble.tex`, `figures/`, `tables/`, and bibliography files: shared presentation assets.
- `build.sh`: compile the article and supplement with Tectonic without running scientific analyses.

From the repository root run `./manuscript/build.sh`. In Overleaf, use XeLaTeX and select `main.tex` or `supplement.tex` as the main document.

Code and analysis data are public at https://doi.org/10.5281/zenodo.22876602. See Supplement S8 for the tested statistical reproduction scope and excluded historical inputs.

For arXiv, use the separate `output/arxiv_source.zip`: it contains only required source files and fixes article-before-supplement compilation. The complete editable package additionally retains the machine-readable table and figure data. No journal cover letter is included. Re-exporting tables and figures requires the complete research repository and its presentation scripts under `manuscript/scripts/` or `manuscript_es/scripts/`; it is not part of compilation from this ZIP.
