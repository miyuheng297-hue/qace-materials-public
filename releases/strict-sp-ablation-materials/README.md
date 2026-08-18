# Strict Supporting-Fact Ablation Materials

This directory is the strict SP-only aggregate subpackage in public release `public-materials-2026-08-17` (https://github.com/miyuheng297-hue/qace-materials-public/releases/tag/public-materials-2026-08-17). It summarizes 13 allowlisted configurations over one audited frozen candidate pool for 7,405 HotpotQA distractor-development items.

It contains SP precision, recall, F1, average selected-evidence count, 10 predefined contrasts, paired-bootstrap 95% intervals, and three Holm families. It does not contain raw benchmark text, answers, paragraphs, supporting facts, sample IDs, candidate snapshots, selected-evidence records, predictions, responses, logs, caches, checkpoints, or model weights.

This package supports SP-only evidence-selection claims under the frozen pool. It does not support Answer EM/F1, Official Joint, answer generation, end-to-end QA, latency, token, memory, cost, resource, or cross-dataset claims. See `CODE_AVAILABILITY.md`, `DATA_AVAILABILITY.md`, and `PUBLIC_RELEASE_AUDIT.md`.
