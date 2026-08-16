# HotpotQA Licence Scope

## Scope and precedence

This document defines the limited scope of the licences in `LICENSES/`. The listed licences apply only to author-owned contributions at the paths below. They do not grant rights in HotpotQA, KG²RAG, FlagEmbedding/BGE, Meta Llama 3, or any other third-party material. They do not replace the original terms or attribution requirements of any dataset, model, method, software, or publication.

`COPYRIGHT_NOTICE.md` identifies the rights holders for the scoped author-owned contributions. If a path is not listed below, it is **not** automatically licensed by this document.

## Author-original scripts — MIT

The following author-original, local aggregate-validation scripts are licensed under [`LICENSES/MIT.txt`](LICENSES/MIT.txt):

- `releases/strict-sp-ablation-materials/scripts/audit_release_content.py`
- `releases/strict-sp-ablation-materials/scripts/generate_table4.py`
- `releases/strict-sp-ablation-materials/scripts/statistical_methods.py`
- `releases/strict-sp-ablation-materials/scripts/validate_aggregate_results.py`
- `releases/strict-sp-ablation-materials/scripts/validate_portable_manifest.py`
- `scripts/audit_release_content.py`
- `scripts/validate_portable_manifest.py`

The shared root scripts `scripts/validate_aggregate_results.py` and `scripts/validate_final_figure_assets.py` are not included in this HotpotQA-only scope because they also cover non-HotpotQA material. They remain pending separate rights and scope review.

## Author-original documents and HotpotQA figure asset — CC BY 4.0

The following author-original documents and HotpotQA-specific figure asset are licensed under [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt):

- `audit/EXECUTION_INTEGRITY_CAVEAT.md`
- `data/table1_hotpotqa.csv` **only as documentation of its aggregate table schema and labels; the aggregate values themselves are additionally covered by the CC BY-SA scope below**
- `figures/figure2_v106_docx_submission_equivalent.png`
- `releases/strict-sp-ablation-materials/*.md`
- `releases/strict-sp-ablation-materials/protocol/*.md`

This document/figure licence does not license benchmark-derived aggregate values beyond the separate CC BY-SA scope, and does not license any third-party logos, data, or material that may be named in a document.

## Sanitized HotpotQA aggregate results and metadata — CC BY-SA 4.0

The following HotpotQA-related sanitized aggregate results and metadata are licensed under [`LICENSES/CC-BY-SA-4.0.txt`](LICENSES/CC-BY-SA-4.0.txt):

- `data/table1_hotpotqa.csv`
- `data/figure2_hotpotqa_differences.csv`
- `config/hotpotqa_formal_config.json`
- `releases/strict-sp-ablation-materials/PORTABLE_SHA256_MANIFEST.txt`
- `releases/strict-sp-ablation-materials/data/*.csv`
- `releases/strict-sp-ablation-materials/metadata/*.csv`
- `releases/strict-sp-ablation-materials/audit/*.csv`
- `releases/strict-sp-ablation-materials/RELEASE_REPAIR_AUDIT.json`

The listed aggregate and metadata files do not contain redistributed HotpotQA questions, answers, titles, paragraphs, IDs, candidate records, selected-evidence records, predictions, responses, or per-example records.

## Explicit exclusions

The following material is excluded from this HotpotQA scope and remains **pending** separate rights/attribution review:

- every MuSiQue-related file, including `config/musique_fixed_pool_config.json`, `data/table2_musique.csv`, `data/figure3_musique_metrics.csv`, `data/musique_inferential_summary.csv`, and `figures/figure3_v106_docx_submission_equivalent.png`;
- shared/mixed root documents and assets that contain MuSiQue or other non-HotpotQA material, including `README.md`, `RELEASE_SCOPE.md`, `SOURCE_PROVENANCE.md`, `FIGURE_REPRODUCTION.md`, `figures/FIGURE_CAPTIONS.md`, `audit/STATISTICAL_METHODS.md`, `environment/ENVIRONMENT.md`, `PORTABLE_SHA256_MANIFEST.txt`, and `figures/source_metadata/figure_asset_provenance.json`;
- shared/mixed root scripts `scripts/validate_aggregate_results.py` and `scripts/validate_final_figure_assets.py`;
- `CITATION.cff`, existing draft files, prior rights-review records, any unlisted historical material, and any file whose origin has not been confirmed.

No licence is granted by this scope document for excluded material merely because it sits in the same repository.
