This release provides compact data and code to reproduce the statistical comparisons in *How much does the map of science depend on the embedding model?*

Download `code-and-guides.zip`, all nine `data-*.zip` archives and `release-manifest.json`; extract the ZIPs together into a new directory. The payload is approximately 492 MB, compared with the superseded 51 GB full-cache distribution. The manuscript and supplements are excluded.

Verified from extracted archives locally and in a clean Linux environment: 25 regenerated tables (106,445 rows), 17,550 neighbour score checks from integer intersection counts, and the four-figure aggregation check. SHA-256 fingerprints and selection provenance are supplied. See README.md and COVERAGE.md for commands and limits.

The release starts from frozen model-derived measurements. It does not regenerate embeddings from historical text, reconstruct nearest-neighbour lists, or certify a complete rerun of every historical supplementary analysis. Embedding caches, model weights and plaintext input tables are excluded.

Scientific code is unchanged from source commit cc61517; new reproduction and distribution utilities are identified separately. Code: MIT. Own results and documentation: CC BY 4.0. OpenAlex metadata: CC0.

Permanent archive: [10.5281/zenodo.22876602](https://doi.org/10.5281/zenodo.22876602). All 15 deposited files were verified against the release sizes and checksums. [Public Linux reproduction run](https://github.com/aleetreny/Shape-of-Science-Reproducibility/actions/runs/35610529164).
