# How much does the map of science depend on the embedding model?

**Final author-approved manuscript, 21 September 2026.** Alejandro Treny Ortega, University College London, London, United Kingdom. English is the official version for submission and citation. A complete professional Spanish translation is also available.

The study compares ten embedding models on 500,000 OpenAlex publications across 26 research areas. It asks which relationships remain when the model, input text, selected articles or processing changes. The scientific calculations are complete and frozen. Journal submission and arXiv submission are the next steps; neither has been made by this repository release.

## Read or download

| Document | PDF | Editable sources |
| --- | --- | --- |
| Official article | [English article](output/pdf/main.pdf) | [English source package](output/manuscript_source.zip) |
| Supplementary material | [English supplement](output/pdf/supplement.pdf) | Same English source package |
| Spanish translation | [Article](output/pdf/es/main.pdf) · [Supplement](output/pdf/es/supplement.pdf) | [Spanish source package](output/manuscript_source_es.zip) |
| arXiv upload | Article and supplement in English | [arXiv LaTeX ZIP](output/arxiv_source.zip) |

The arXiv package contains the necessary LaTeX sources, figures, bibliography and a compilation-order file. It excludes internal notes, cover letters, data caches and Spanish documents. [Submission instructions and checks](docs/SUBMISSION_READY.md).

## Public data and code

- Permanent dataset: [Zenodo 10.5281/zenodo.22876602](https://doi.org/10.5281/zenodo.22876602).
- Download mirror and portable reproduction: [Shape-of-Science-Reproducibility v1.1.0](https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0).
- [Exact selection and tested scope](COMPACT_REPRODUCIBILITY.md).

The public distribution is 492 MB. It retains identifiers, article selections, per-query counts, measurements and controls. Starting from those frozen measurements, the documented check reproduced 25 tables with 106,445 identical rows and checked 17,550 neighbour scores, including in a fresh Linux environment. It does not regenerate embeddings from historical text or certify a complete rerun of all supplementary analyses. Large vector caches, model weights and historical plaintext inputs are excluded; the article and Supplement S8 explain the boundary.

## Build the documents

Run `./manuscript/build.sh` for English and `./manuscript_es/build.sh` for Spanish. These commands compile the included presentation files; they do not run scientific calculations. XeLaTeX can also compile the sources with the supplied BibTeX bibliographies.

## Scientific records

[Final robustness report](ROBUSTNESS_CLOSURE_REPORT.md) · [Expanded comparisons](ROBUSTNESS_RESULTS.md) · [Area-pair results](FIELD_PAIR_RESULTS.md) · [Methods](METHODS_ROBUSTNESS.md) · [Data catalogue](DATA_CATALOG.md) · [Document index](docs/INDEX.md).

The original source snapshots, configurations and results retain their provenance. Earlier notes describe the chronology and are not instructions to restart experiments or upload the superseded 51 GB package.

Own code: [MIT](LICENSE). Own results and documents: [CC BY 4.0](LICENSING.md). OpenAlex metadata: CC0. Third-party rights remain with their owners.
