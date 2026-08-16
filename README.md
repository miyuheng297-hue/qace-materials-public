# QACE Research Materials

This public-release candidate directory holds auditable research materials associated with the QACE paper. It is not a general-purpose implementation repository or an end-to-end reproducibility release.

## Material sets

- Historical aggregate audit materials document the earlier aggregate evidence chain and its own stated boundaries.
- `releases/strict-sp-ablation-materials/` contains the current strict supporting-fact ablation materials that underlie Table 4 in the current manuscript. Its scope is distinct from the historical materials and must not be merged with them when interpreting results.

The strict supporting-fact materials contain sanitized aggregate evidence only. They are not an end-to-end KG²RAG or question-answering reproduction package and do not contain raw benchmark text, predictions, per-example candidate data, or selected-evidence records.

## Repository status

Licensing is path-scoped for confirmed author-owned contributions: author-original Python scripts use MIT; author-original documents and figures use CC BY 4.0; scoped HotpotQA sanitized aggregate results and configuration metadata use CC BY-SA 4.0; and the five directly scoped MuSiQue aggregate/configuration/figure assets use CC BY 4.0. See `COPYRIGHT_NOTICE.md`, `HOT_POTQA_LICENSE_SCOPE.md`, `MUSIQUE_LICENSE_SCOPE.md`, and `SHARED_ROOT_MATERIALS_SCOPE.md`.

No repository URL, release tag, DOI, or Data/Code Availability destination is invented here. The three time-bound historical records listed in `SHARED_ROOT_MATERIALS_SCOPE.md` were intentionally omitted from this candidate.

## Reading the materials

Read the scope, provenance, claim-boundary, rights, and availability documents in each material directory before relying on an aggregate result. The material directories preserve their own integrity and rights records; readers should not treat one directory as substituting for another evidence chain.
