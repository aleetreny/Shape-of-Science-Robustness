# Current public reproduction route

The compact version 1.1.0 is available from [GitHub Releases](https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0). Download `code-and-guides.zip` and all nine `data-*.zip` archives, extract together, and follow that distribution's README. Its DOI archive is public at [10.5281/zenodo.22876602](https://doi.org/10.5281/zenodo.22876602). The superseded 51 GB caches remain local and are not required by the compact commands.

Verified from the extracted distribution: 25 regenerated result tables (106,445 rows), 17,550 local neighbour scores, balanced local/global averages, and the four-main-figure aggregation checks. Every downloaded public GitHub asset was verified against its SHA-256 hash. The route starts from frozen model-derived measurements; it does not re-run inference from historical texts or certify every supplementary analysis. The package contains exact identities/selections, configurations and upstream code, with this boundary explicitly stated.

The existing `reproduce_summaries.py` in this research checkout still works without dependencies. `check_vectors.py` and `verify_archives.py` refer to the superseded full-cache archive layout and are historical utilities, not the public compact route. Prior documentation is preserved in `research/compact_release_2026-09-21/superseded/reproducibility/README.md`.
