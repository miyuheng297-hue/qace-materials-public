# QACE Research Materials

This repository contains the public materials associated with the QACE manuscript. It has two
layers: an aggregate-only audit package (release `public-materials-2026-08-17`, unchanged) and,
added on 2026-10-23, a reproducibility package for the PLOS ONE submission.

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

The aggregate package does not contain raw benchmark text, questions, answers, titles, paragraphs, supporting-fact records, candidate or selection records, predictions, responses, logs, caches, checkpoints, credentials, private paths, or model/software payloads. The strict package is SP-only and does not support Answer EM/F1, Joint, end-to-end QA, latency, token, memory, cost, or resource claims.

## Reproducibility package (added 2026-10-23)

The PLOS ONE submission requires that the code and the data underlying every reported number be
publicly available without restriction at the time of publication. A reproducibility layer is
therefore added at the repository root:

```
analysis/    analysis scripts (Python 3.12)
data/        machine-readable data for every table and figure in the manuscript
docs/        REPRODUCTION.md and DATA_DICTIONARY.md
requirements.txt
```

**Scope change.** Unlike the aggregate package above, this layer contains per-question records:
sample identifiers, candidate scores, selected-fact identifiers, per-question metrics and
generated answers. It deliberately contains **no benchmark sentence text, no titles, no
questions and no gold answers**. Every candidate fact is identified by

```
fact_id = sha256("title##sentence_index")[:16]
```

which is recomputed locally from the public HotpotQA and 2WikiMultiHopQA distributions. This
keeps the no-text policy of the aggregate package while still allowing every number in the
manuscript to be recomputed.

What the layer supports:

| item | supported |
|---|---|
| count-matched comparison (Table 2, Table 3, Fig 2) | yes |
| ranking under two conventions (Table 4, Fig 1) | yes |
| equivalence testing (TOST) | yes |
| selection-floor sensitivity (Fig 3) | yes |
| mechanism attribution (Table 5) | yes |
| answer-layer means (Section 4.9) | yes |
| knowledge-graph expansion condition (Section 4.6) | yes, via `data/kg_expansion/` |
| 2WikiMultiHopQA (Section 4.5) | yes, via `data/2wiki_candidate_snapshot_scores.jsonl` |

See `docs/REPRODUCTION.md` for the run order, `docs/DATA_DICTIONARY.md` for every field, and
`docs/ZENODO_STEPS.md` for archiving the release and obtaining a DOI.

## Licensing

Licensing is path-scoped. Author-produced documentation and figure displays are covered by CC BY 4.0 where listed; author-original validation scripts are covered by MIT where listed; sanitized HotpotQA aggregate material is covered by the stated CC BY-SA 4.0 scope; and direct MuSiQue aggregate material is covered by its CC BY 4.0 scope. The scope files and notices are controlling and do not grant rights in third-party datasets, models, software, or publications.

The repository is released under the **MIT licence** (`LICENSE`), which covers the scripts under
`analysis/` and `scripts/`, the documentation under `docs/`, and the derived data under `data/`.
It grants no rights in third-party datasets, models, software or publications; HotpotQA and
2WikiMultiHopQA keep their own licences (see the attribution and third-party notice files).
`LICENSE_DECISION_REQUIRED.md` is kept for historical traceability only.

Editable SVG files and plotting scripts of the earlier release are intentionally not included in
that release because their item-level public-release authorization was not established by the
local audit. The immutable older tag `public-materials-2026-08` retains the previous package
unchanged.
