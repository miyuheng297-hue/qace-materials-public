# Release audit — QACE v11.3 strict SP-ablation materials

## Release identity

Sanitized aggregate audit and reproducibility package for the strict SP-only Table 4 evidence in QACE manuscript v11.3.

`V11_3_PRIVATE_STAGING_READY: YES`

Technical packaging, numerical reconciliation, and sanitization pass. This status means the package is suitable for authorised **private staging only**. It is not public-release approval.

## Included scope

- Finalized 13-configuration aggregate SP precision/recall/F1/average-evidence-count CSV.
- Finalized 40-record aggregate paired-comparison CSV, using 20,000 paired-bootstrap replicates and three declared Holm families.
- Table 4 Panel A (7 rows), Panel B (5 SP-F1 contrasts), and Panel B metric detail (20 records).
- Path-free configuration/provenance metadata, sanitized protocol/statistical methods, and local-only aggregate validation scripts.

## Excluded scope

No benchmark questions, answers, paragraphs, titles, supporting-fact text, sample identifiers, gold records, candidate snapshots, selected-evidence records, route/selection logs, per-item metrics/differences, predictions, responses, HTTP records, caches, checkpoints, model files, absolute server paths, IP addresses, hostnames, usernames, credentials, legacy experiment materials, or Stage 4D material are included.

## Claim boundary

The package supports strict SP-only evidence-selection claims under the common frozen scored-candidate snapshot. It does not support Answer EM/F1, Official HotpotQA Joint, answer generation, end-to-end QA, retrieval, latency, token, memory, or resource claims; nor does it replace the separate Table 1/Figure 2 or Table 2/Figure 3 evidence chains.

## Public-release blockers

Authors/rights holders must choose and document the licence, confirm aggregate redistribution and HotpotQA terms, complete third-party notices, and complete repository/citation metadata. No URL, release tag, DOI, or licence is fabricated here.
