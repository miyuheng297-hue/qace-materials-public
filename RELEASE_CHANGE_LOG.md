# Release Change Log

Release tag: `public-materials-2026-08-17`

## Initial repository state

- Local `HEAD`: `e6f68b9b650189c011846408aef5b20e5bf82047`.
- Fetched `origin/main`: `e6f68b9b650189c011846408aef5b20e5bf82047`.
- Local and remote tracked trees: 72 files, identical paths and contents.
- Initial worktree: clean.
- Existing tag `public-materials-2026-08`: present locally and remotely at the initial commit.
- Existing GitHub Release `QACE Sanitized Research Materials`: published, non-draft, non-prerelease, and linked to the old tag. It remains immutable.

## Added

- Latest manuscript-matched `figures/Fig1.png` and `figures/Fig1.pdf` through `figures/Fig4.png` and `figures/Fig4.pdf`.
- Final strict-subpackage `CODE_AVAILABILITY.md`, `DATA_AVAILABILITY.md`, `PUBLIC_RELEASE_AUDIT.md`, and `THIRD_PARTY_NOTICES.md`.
- This release change log.

Editable SVG files and plotting scripts were not added. The prior read-only audit marked them for inclusion only after item-level authorship, dependency, and public-release authorization. That authorization was not established in the local evidence, so the public update remains limited to the exact PNG/PDF display assets.

## Removed from the new branch state

- Three obsolete v10.6 raster filenames.
- Strict-subpackage private staging instructions, draft availability statements, confirmation-required licence file, repair audits, and third-party notice template.

These files remain available in the immutable old tag and Release; no Git history or old tag was rewritten.

## Replaced or refreshed

- Repository README, release scope, source provenance, figure reproduction/captions/provenance, path-scoped copyright/licence records, sanitization report, and benchmark-exclusion audit.
- Root and strict manifest validators. The root validator excludes `.git`, excludes only the root manifest being checked, and retains the nested strict manifest in root coverage.
- Root aggregate/figure/sensitive-content validators for the current four-figure package; the sensitive-content scan now ignores Git internals when run from a checked-out repository.
- Strict README, citation metadata, inventory, source-hash normalization record, sensitive-scan summary, manifest, and validators.

## Preserved byte-for-byte

- Table 1 and Table 2 aggregate CSVs and their Figure 2/3 source CSVs.
- MuSiQue inferential summary and both root configurations.
- Strict SP-only result, comparison, Table 4 display, configuration, provenance, protocol, and statistical-method source files, except the two validators updated for current manifest/sensitive-scan behavior.
- Official MIT, CC BY 4.0, and CC BY-SA 4.0 notice texts and dataset attribution/third-party notice files.

## Audit results before repository synchronization

- Root manifest: 73 entries, complete relative-path coverage, zero mismatches.
- Strict manifest: 27 entries, complete relative-path coverage, zero mismatches.
- PowerShell SHA-256: zero mismatches for both manifests.
- GNU `sha256sum -c`: all root and strict entries passed.
- Sensitive-content scans: passed at root and strict levels.
- Aggregate validation: HotpotQA, MuSiQue, and strict SP-only data passed.
- Table 4 generation/check: 13 configurations, 40 comparison rows, Panel A and Panel B subsets passed.
- Figure assets: eight current PNG/PDF files present; all hashes match the latest manuscript asset directory.
- Figure PNGs: 600 dpi metadata and expected dimensions present.
- Strict inventory: 28 actual files, 28 rows, zero missing/extra paths and zero byte-size mismatches.
- `git diff --check` equivalent on the independent candidate: no whitespace errors after repair.
- No experiment, model, BGE, Ollama, retrieval, generation, bootstrap, or evaluation was run.

## Scientific and rights boundaries

The update changes publication packaging, figures, documentation, and validators only. It does not change any aggregate data value, statistical result, figure value, table value, manuscript claim, or evidence-chain boundary. The package remains aggregate-only and does not support end-to-end, efficiency, global-optimality, or isolated component-causal claims.

Licensing remains path-scoped. The package contains no raw benchmark records, sample identifiers, candidates, selections, predictions, responses, logs, credentials, private paths, or third-party payloads. SVG and plotting-source publication remains an author decision outside this release.
