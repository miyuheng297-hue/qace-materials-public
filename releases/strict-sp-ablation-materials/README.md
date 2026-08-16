# QACE Strict Supporting-Fact Ablation Materials

This directory is a sanitized aggregate audit and reproducibility package for the strict supporting-fact Table 4 evidence in the current QACE manuscript.

## Scope

The materials report strict supporting-fact selection over 7,405 HotpotQA distractor-development examples under one shared frozen candidate pool. They contain aggregate results for 13 configurations: supporting-fact precision, supporting-fact recall, supporting-fact F1, and average selected-evidence count. The package also records 10 predefined contrasts, each evaluated with 20,000-replicate paired bootstrap procedures and family-wise Holm correction.

The package contains aggregate CSVs, Table 4 display subsets, sanitized protocol and statistical-method descriptions, path-free provenance metadata, and local-only aggregate validation/check scripts. It does not contain raw benchmark text, answers, titles, paragraphs, gold supporting facts, sample identifiers, candidate snapshots, selected-evidence records, predictions, responses, logs, caches, checkpoints, or model weights.

## Evidence boundary

These materials support strict supporting-fact-only evidence-selection results. They do not support Answer EM/F1, any Joint metric, answer generation, end-to-end question-answering, efficiency, token, latency, memory, resource, or cross-dataset-generalization conclusions. They do not substitute for the separate evidence chains reported elsewhere in the manuscript.

## Rights, availability, and staging status

This directory is included in a public-release candidate. It has path-scoped licences for confirmed author-owned contributions: the included author-original Python scripts are MIT; author-original documentation is CC BY 4.0; and the sanitized HotpotQA aggregate CSVs and configuration/provenance metadata are CC BY-SA 4.0. The authoritative path list is `../../HOT_POTQA_LICENSE_SCOPE.md`; `../../COPYRIGHT_NOTICE.md` identifies the authors and year.

The cleaned aggregate materials are not an end-to-end rerun package. They do not grant rights in HotpotQA or any third-party method, model, software, or publication. No repository URL, release tag, DOI, or final Data/Code Availability destination is invented here. Consult `RELEASE_AUDIT.md`, `RELEASE_REPAIR_AUDIT.md`, `LICENSE_DECISION_REQUIRED.md`, `THIRD_PARTY_NOTICES_TEMPLATE.md`, `DATA_AVAILABILITY_DRAFT.md`, and `CODE_AVAILABILITY_DRAFT.md` before any release decision.
