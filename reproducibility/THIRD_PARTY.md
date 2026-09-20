# Third-party provenance

Exact model repositories/revisions are in `config/embeddings_v1.json` and the archived manifests. Model weights are not redistributed. The readme/license observations below were checked against the pinned local model cards or the official project sources on 20 September 2026; they are provenance, not a transfer of rights in training or input text.

| Model | Stated model/project terms |
| --- | --- |
| SPECTER, SPECTER2 base and adapter | Apache 2.0, pinned model cards. |
| SciNCL | MIT, pinned model card. |
| SciBERT | Apache 2.0, [official project](https://github.com/allenai/scibert). The pinned model card itself has no license field. |
| BERT, MPNet, MiniLM | Apache 2.0, pinned model cards. |
| PubMedBERT/BiomedBERT | MIT, pinned model card. |
| BioBERT | [Official project license](https://github.com/dmis-lab/biobert/blob/master/LICENSE); the [model repository](https://huggingface.co/dmis-lab/biobert-v1.1) has no model card. Do not infer an explicit model-output license from absent metadata. |
| SimCSE | [Official project MIT license](https://github.com/princeton-nlp/SimCSE/blob/main/LICENSE); also retain the pinned model source. |

OpenAlex describes its metadata as CC0 in its [data documentation](https://help.openalex.org/data/how-its-built/). Its [abstract attribute documentation](https://help.openalex.org/data/works/attributes/#abstract_inverted_index) distinguishes the supplied inverted index from plaintext abstracts. This release excludes the historical plaintext inputs and retains their identities/hashes. The CC0 metadata terms and permissive model licenses do not establish copyright ownership of the underlying articles.

Numerical arrays, own code and documentation have the scopes set out in `LICENSING.md`. Third-party libraries retain their licenses. Full copies of cited papers, downloaded model assets, secrets and personal environments are absent.
