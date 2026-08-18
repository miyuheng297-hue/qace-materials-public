# QACE Research Materials

This repository contains the public aggregate-materials package associated with the QACE manuscript. It is an audit and inspection package, not an end-to-end implementation or rerun release.

## Current release

- Tag: `public-materials-2026-08-17`
- Repository: https://github.com/miyuheng297-hue/qace-materials-public
- Release page: https://github.com/miyuheng297-hue/qace-materials-public/releases/tag/public-materials-2026-08-17
- Manuscript source, manuscript PDF, author metadata, benchmark records, model weights, and runtime logs are not distributed.

## Included material

- Sanitized aggregate HotpotQA and MuSiQue tables, configuration metadata, and inferential summaries.
- Strict supporting-fact-only aggregate material for the 13-configuration ablation and 10 predefined contrasts under one frozen candidate pool in `releases/strict-sp-ablation-materials/`.
- The latest four author-produced figure displays as PNG and vector PDF files in `figures/`.
- Scope, attribution, third-party notices, provenance, integrity manifests, and validation scripts.

The package does not contain raw benchmark text, questions, answers, titles, paragraphs, supporting-fact records, sample IDs, candidate or selection records, predictions, responses, logs, caches, checkpoints, credentials, private paths, or model/software payloads. The strict package is SP-only and does not support Answer EM/F1, Joint, end-to-end QA, latency, token, memory, cost, or resource claims.

## Licensing

Licensing is path-scoped. Author-produced documentation and figure displays are covered by CC BY 4.0 where listed; author-original validation scripts are covered by MIT where listed; sanitized HotpotQA aggregate material is covered by the stated CC BY-SA 4.0 scope; and direct MuSiQue aggregate material is covered by its CC BY 4.0 scope. The scope files and notices are controlling and do not grant rights in third-party datasets, models, software, or publications.

Editable SVG files and plotting scripts are intentionally not included in this release because their item-level public-release authorization was not established by the local audit. The immutable older tag `public-materials-2026-08` retains the previous package unchanged.
