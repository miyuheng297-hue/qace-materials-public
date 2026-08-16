# v11.3 Release Repair Audit

## Scope

This repair copied the locally accepted strict SP-only aggregate package and changed only public metadata/documentation, the inventory, the portable manifest, and availability drafts. No experiment, model, BGE, selector, retrieval, generation, evaluation, bootstrap, or plotting activity was run.

## Changes

- Updated manuscript/Table 4 identifiers to **QACE v11.3 strict SP-ablation materials**.
- Rebuilt the content inventory so it includes every package file, including `PUBLIC_FILE_INVENTORY.csv` and the non-self-hashed portable manifest.
- Clarified that the inventory is a content directory and the manifest is the hash-integrity record.
- Transferred only publicly suitable author names, affiliation, and confirmed ORCID from the v11.3 author manuscript into `CITATION.cff`; no email was copied.
- Kept repository URL, release tag/version, DOI, and licence as author-confirmation fields.
- Retained strict SP-only and non-end-to-end boundaries.

## Verification

- Numerical reconciliation: Panel A 7/7, Panel B 5/5, and detail 20/20 exact; 13 aggregate configurations and 40 aggregate comparisons remain byte-identical to the finalized acceptance source.
- Sensitive scan: PASS — no raw benchmark/item/candidate/selection/prediction material, absolute paths, IPs, credentials, endpoints, or legacy experiment payloads added.
- Portable manifest: regenerated after all metadata changes and verified separately.

`V11_3_PRIVATE_STAGING_READY: YES`

This is not public-release approval. Rights-holder confirmations are still required before any public GitHub release.
