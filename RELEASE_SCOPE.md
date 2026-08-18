# Release Scope

This is the sanitized aggregate release `public-materials-2026-08-17` for the QACE materials.

## Included

- `data/table1_hotpotqa.csv`, `data/figure2_hotpotqa_differences.csv`, and `config/hotpotqa_formal_config.json` for corrected aggregate HotpotQA B/D/G reporting.
- `data/table2_musique.csv`, `data/figure3_musique_metrics.csv`, `data/musique_inferential_summary.csv`, and `config/musique_fixed_pool_config.json` for paragraph-native fixed-pool MuSiQue validation.
- `releases/strict-sp-ablation-materials/` for strict SP-only aggregate results, table subsets, protocol, statistical contract, provenance, and validators.
- `figures/Fig1.png`, `figures/Fig1.pdf` through `figures/Fig4.png`, `figures/Fig4.pdf`, with the corresponding captions and provenance metadata.
- Aggregate-only audit, rights, attribution, third-party-notice, environment, and manifest files.

## Excluded

- Benchmark questions, answers, aliases, titles, paragraphs, supporting facts, annotations, sample identifiers, candidate snapshots, selected-evidence records, predictions, responses, raw HTTP, logs, caches, checkpoints, model weights, credentials, hosts, endpoints, and private paths.
- Manuscript `.tex`, `.bib`, `.pdf`, Word files, author metadata, and unpublished correspondence.
- Editable SVG files and plotting scripts pending item-level public-release authorization.
- Historical v10.6 raster filenames and private staging, draft, confirmation-required, or release-instruction files.

The displayed values remain aggregate-only and retain the evidence-chain boundaries in the manuscript: corrected HotpotQA B/D/G, paragraph-native fixed-pool MuSiQue, and strict SP-only ablation are not interchangeable.
