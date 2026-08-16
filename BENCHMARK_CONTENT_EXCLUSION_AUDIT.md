# Benchmark Content Exclusion Audit

## Audit Objective

The candidate must contain no benchmark source text, gold annotations, or model-produced answers. It was rebuilt from an allowlist of aggregate values and final figure assets rather than copied wholesale from the staging package.

## Exclusion Evidence

| Prohibited content | Evidence of exclusion |
|---|---|
| Question text or aliases | No JSONL files are present; CSV schemas contain only configuration, metric, run, contrast, interval, and p-value fields. |
| Gold answers | No answer strings or aliases are present. `answer_em` and `answer_f1` are metric labels only. |
| Gold supporting facts | No supporting-fact titles, sentence indices, paragraph identifiers, or gold annotation structures are present. |
| Titles and paragraph text | No title, paragraph, context, evidence-text, or document-text fields are present. |
| Predictions or model responses | No prediction, response, raw HTTP, terminal-response, checkpoint, or log file is present. |
| Sample-level material | No sample IDs, per-sample metrics, selections, candidate positions, text hashes, or failure samples are present. |
| Server and secret material | No absolute server paths, IP addresses, URLs, hostnames, endpoints, tokens, passwords, API keys, or credential files are present. |

## Mechanical Checks

`scripts/audit_release_content.py` enforces:

- an extension allowlist;
- rejection of JSONL, logs, archives, database files, checkpoints, and common secret-file names;
- rejection of absolute server paths, URLs, IP addresses, and credential-like assignments;
- rejection of exact sensitive JSON keys and CSV headers;
- rejection of benchmark-shaped identifiers and common response-record field names;
- inspection of text and metadata files as ordinary text, while permitting only the three hash-anchored final PNG figure assets.

The script is run again after the portable manifest is generated. Its result is recorded in `audit/SANITIZATION_REPORT.md`.

## Human Review Boundary

The audit demonstrates that the candidate contains no known benchmark or model-answer content. The rights holder must still review the aggregate values, figure captions, names, and licensing position before publication.
