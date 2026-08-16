# Sanitized strict SP-only experiment protocol

## Scope

The package describes supporting-fact selection only over 7,405 ordered evaluation items. It reports SP precision, SP recall, SP F1, and average selected-evidence count. No answer text, answer generation, Answer EM/F1, Joint EM/F1, or Official Joint metric is part of this package.

All 13 configurations use one audited frozen upstream candidate pool. A requested evidence budget is capped by the number of available candidates for that item; no padding, duplicates, fabricated candidates, or cross-pool supplementation are allowed. The upstream pool capacity is at most 10.

## Configuration families

The 13 configuration identifiers and their portable rules are recorded in `metadata/configuration_registry_summary.csv`. They comprise three upstream references, one full shared selector, two fixed-budget controls, five one-at-a-time component ablations, and two local min-recall sensitivity settings.

The full selector and each intervention operate only on the common frozen pool. The score-source ablation uses the immutable upstream score instead of sentence-level BGE rescoring; a missing or non-finite score is a hard failure. Sensitivity settings change only the min-recall budget relative to the full selector.

## Statistical contract

There are 10 predefined configuration/component/sensitivity contrasts. For each contrast and each of four metrics, the reported values are paired differences, a percentile 95% confidence interval, a two-sided paired-bootstrap p-value, and a Holm-adjusted p-value. The bootstrap uses 20,000 deterministic replicates, base seed 20260814, and comparison-specific seeds. Holm correction is separate for the 12 configuration-level, 20 component-ablation, and 8 sensitivity-analysis tests.

The finalized acceptance audit independently recomputed point estimates, per-item differences, bootstrap records, and Holm values from the canonical scoring inputs. This release exposes only the resulting aggregates and metadata, not those inputs.

## Boundary

The package supports SP-only evidence-selection claims under the shared frozen pool. It does not support claims about retrieval quality in isolation, universal model quality, answer generation, Answer EM/F1, Official Joint, latency, or end-to-end QA accuracy.
