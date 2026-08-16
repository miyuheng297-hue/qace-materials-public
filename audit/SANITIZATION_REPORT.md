# Sanitization Report

## Candidate Construction

The v2 candidate was copied from the private v10 sanitized candidate into a new directory, then repaired with an explicit final-asset allowlist. The prior SVG redraws and their generator were removed because they are not the v10.6 submission layout. The retained material is limited to aggregate CSV values, aggregate configuration summaries, sanitized documentation, final PNG figures extracted from the v10.6 DOCX, provenance metadata, and validation scripts.

## Positive Checks

- `scripts/validate_aggregate_results.py`: validates the fixed v10.6 Table 1/2 values and their retained Figure 2/3 source CSV transformations.
- `scripts/validate_portable_manifest.py`: validates only relative paths, hashes, and full file coverage.
- `scripts/validate_final_figure_assets.py`: validates the specified v10.6 DOCX/PDF against the final PNG asset metadata.
- `scripts/audit_release_content.py`: validates the allowed file types and rejects benchmark content, paths, credentials, and all image assets other than the three hash-anchored final PNGs.
- `PORTABLE_SHA256_MANIFEST.txt`: is verified with `sha256sum -c` from the candidate root.

The final run produced: `aggregate_validation=ok`; `sensitive_content_scan=ok files=27`; `relative_manifest_check=ok files=26`; `docx_pdf_figure_asset_check=ok figures=3 figure3_panel_count=3 editable_vector_source=none_found`.

## Excluded Classes

The candidate contains no benchmark text, answers, aliases, gold facts, titles, paragraph text, sample IDs, selected evidence, per-sample metrics, predictions, model responses, raw HTTP, terminal records, logs, failure samples, datasets, KG assets, models, caches, credentials, absolute server paths, hostnames, URLs, IP addresses, or historical v3/top-k/holdout/Stage 4D result artifacts. The three permitted PNGs are final manuscript figure assets; they contain no benchmark examples or sample-level output. Their hashes, dimensions, and DOCX/PDF correspondence are recorded for review.

## Residual Human Review

Automated scans cannot decide copyright ownership, benchmark redistribution rights, attribution obligations, publisher policy, or whether aggregate metrics and figure styling require third-party notices. The remaining rights-holder decisions, including retention of DOCX-extracted raster figures without an editable same-version source, are listed in `LICENSE_DECISION_REQUIRED.md`.
