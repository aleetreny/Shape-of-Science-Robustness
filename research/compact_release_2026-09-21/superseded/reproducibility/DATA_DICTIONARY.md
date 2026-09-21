# Data dictionary and archive map

All identifiers and selection arrays refer to the fixed historical corpus. Do not join by title or by the row number of a newly downloaded table.

| Field or object | Meaning |
| --- | --- |
| `row_index` | Zero-based row in the 500,000-paper corpus. Subset tables preserve this identifier even when stored consecutively. |
| `work_id` | OpenAlex work identifier; a distinct publication in this corpus. |
| `text_sha256` and `source_text_sha256` | Historical processed-text identity, or parent text identity for an input variant. Hashes do not supply the omitted text. |
| `cohort` | General 400,000-paper collection or 100,000-paper reinforcement; not population weights. |
| `field_id`, `subfield_id` | OpenAlex broad area and narrower specialty labels. Labels are not independent thematic ground truth. |
| `publication_year`, `period_start` | Publication year and first year of its five-year analysis period. |
| quality flags, duplicate groups | Recorded source/cleaning diagnostics retained for sensitivity analyses. No manual relabelling of illustrative cases. |
| `rows.parquet` | Identity and token/truncation diagnostics for a stored vector block; no plaintext abstracts. |
| `mean.npy`, `cls.npy`, `sep.npy` | Raw float32 vectors with the pooling named by the file; row order comes from the sibling `rows.parquet`. Vectors are not pre-normalised. |
| `selection_sha256` | Hash of the exact ordered selection, usually little-endian int64 global row IDs as documented in the frozen program. |
| `query_ids`, `candidate_ids` | Starting articles and eligible search articles. The current query is excluded from its own neighbour list. |
| `repeat`, `kind`, `representation` | Repetition within the named design, its selection type, and original/centred vector processing. Different analyses use different repetition counts. |
| `mean_overlap` | Fraction shared by two neighbour lists, on a 0-1 scale. `model_change` is the replaced fraction, also 0-1. A percentage-point difference multiplies a fraction difference by 100. |
| `angle_p50` | Median-chord angular spread in degrees; not thematic diversity. |
| `pr`, `erank`, `d80` | Participation ratio, entropy effective rank, and integer number of principal directions covering 80% of variance. Definitions are in `METHODS_MORPHOLOGY.md` in the code distribution. |

`SCHEMAS.json` lists the Arrow columns/types for every distinct source schema. Some schemas describe omitted original input tables; `DATA_EXCLUSIONS.json` identifies which columns were removed from their public replacements.

| Archive | Contents |
| --- | --- |
| `analysis_ready_v1.zip` | Non-text metadata for all 500,000 papers. |
| `embeddings_<model>.zip` (10 files) | All frozen principal model vectors and available mean/CLS/SEP variants, with block identities and manifests. |
| `embeddings_source_snapshot.zip` | Source snapshots accompanying the main vector generation. |
| `analysis_v1.zip` | Initial structure/neighbor results, exact selections, common-passage 52,000-paper vectors and MiniLM-512 control. |
| `checklist_v1.zip` | The 26,000-paper input pilot and its controls, retained as historical evidence. |
| `robustness_v2.zip` | Expanded 52,000-paper input experiment, paired scope searches, time/discipline/family and stability analyses. |
| `prepaper_v1.zip` | Case-atlas numerical records and source-quality diagnostics, with local abstract excerpts excluded. |
| `morphology_pilot_v1.zip` | Geometry selections, original measurements and synthetic controls. |
| `field_pair_summary_v1.zip` | Pairwise direction/classification records and rules. |
| `robustness_closure_v1.zip` | Final centre repetitions, direct text/model contrasts, complete geometry conditions and quality checks. |

The two sets of 52,000 have different purposes. The text experiment includes the earlier 26,000-paper pilot; the common-passage control is another selection. The geometry analysis uses the text experiment's title-plus-abstract vectors. Exact memberships are retained, so these relationships can be checked without reconstructing them from seeds alone.

Scientific protocols, configuration, methods and `reports/` are in the filtered code distribution. The reproduction input manifests identify their original numerical tables and checksums. The scientific phase reports document the additional analyses and their limits. Article manuscripts, supplements and earlier editorial copies are not included. `PACKAGE_MANIFEST.json` inside the code ZIP inventories the files delivered and identifies the source Git commit and documentation updates.
