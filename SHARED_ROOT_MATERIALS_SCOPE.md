# Shared Root Materials Scope

This table records the current public-release treatment of every root-level or shared asset included in this public candidate that is not exclusively covered by a direct HotpotQA, MuSiQue, or strict supporting-fact package path. It implements the authors' 2026 decisions: author-original Python scripts are MIT; author-original documentation and figures are CC BY 4.0; scoped HotpotQA aggregate material is CC BY-SA 4.0; and scoped MuSiQue aggregate material is CC BY 4.0. The formal path-specific scope documents remain controlling where they apply.

No category grants rights in a third-party dataset, model, publication, trademark, or software component. A row marked `PUBLIC-EXCLUDED / AUTHOR-CONFIRMATION-REQUIRED` must be removed from, separately cleared for, or otherwise handled before a public repository release; it is not silently licensed by this table.

| Tracked path | Classification | Basis and release treatment |
|---|---|---|
| `.gitignore` | CC BY 4.0 | Author-original repository configuration/documentation. |
| `.gitattributes` | CC BY 4.0 | Author-original portability configuration. |
| `README.md` | CC BY 4.0 | Author-original repository documentation. |
| `RELEASE_SCOPE.md` | CC BY 4.0 | Author-original scope documentation. |
| `SOURCE_PROVENANCE.md` | CC BY 4.0 | Author-original provenance documentation; does not grant third-party rights named within it. |
| `FIGURE_REPRODUCTION.md` | CC BY 4.0 | Author-original reproduction documentation. |
| `BENCHMARK_CONTENT_EXCLUSION_AUDIT.md` | CC BY 4.0 | Author-original exclusion audit. |
| `LICENSE_DECISION_REQUIRED.md` | CC BY 4.0 | Author-original licence-status documentation; the filename is retained for traceability. |
| `COPYRIGHT_NOTICE.md` | CC BY 4.0 | Author-original copyright and scope notice. |
| `HOT_POTQA_DATASET_ATTRIBUTION.md` | CC BY 4.0 | Author-original attribution documentation. |
| `HOT_POTQA_LICENSE_SCOPE.md` | CC BY 4.0 | Author-original scope documentation; it controls the listed HotpotQA paths. |
| `HOT_POTQA_THIRD_PARTY_NOTICES.md` | CC BY 4.0 | Author-original notice documentation. |
| `MUSIQUE_DATASET_ATTRIBUTION.md` | CC BY 4.0 | Author-original attribution documentation. |
| `MUSIQUE_LICENSE_SCOPE.md` | CC BY 4.0 | Author-original scope documentation; it controls the five listed MuSiQue paths. |
| `MUSIQUE_THIRD_PARTY_NOTICES.md` | CC BY 4.0 | Author-original notice documentation. |
| `SHARED_ROOT_MATERIALS_SCOPE.md` | CC BY 4.0 | This author-original scope table. |
| `audit/EXECUTION_INTEGRITY_CAVEAT.md` | CC BY 4.0 | Explicitly scoped author-original HotpotQA documentation. |
| `audit/STATISTICAL_METHODS.md` | CC BY 4.0 | Author-original shared methods documentation; it does not license named third-party material. |
| `audit/SANITIZATION_REPORT.md` | CC BY 4.0 | Author-original sanitation documentation. |
| `environment/ENVIRONMENT.md` | CC BY 4.0 | Author-original environment documentation; runtime dependencies are not distributed. |
| `figures/FIGURE_CAPTIONS.md` | CC BY 4.0 | Author-original captions/documentation. |
| `figures/figure1_v106_docx_submission_equivalent.png` | CC BY 4.0 | Author-produced conceptual figure; third-party rights are not asserted. |
| `figures/source_metadata/figure_asset_provenance.json` | CC BY 4.0 | Author-original provenance metadata. |
| `scripts/audit_release_content.py` | MIT | Explicitly scoped author-original release-validation script. |
| `scripts/validate_portable_manifest.py` | MIT | Explicitly scoped author-original manifest-validation script. |
| `scripts/validate_aggregate_results.py` | MIT | Author-original shared aggregate validator; it does not redistribute benchmark records. |
| `scripts/validate_final_figure_assets.py` | MIT | Author-original shared figure validator. |
| `PORTABLE_SHA256_MANIFEST.txt` | CC BY 4.0 | Author-original integrity record; it is regenerated for the public release set and does not self-hash. |
| `LICENSES/MIT.txt` | MIT | Official MIT licence text retained as the notice for the scoped author-original scripts; no authorship in the legal text is asserted. |
| `LICENSES/CC-BY-4.0.txt` | CC BY 4.0 | Official CC BY 4.0 legal text retained as the notice for the scoped author-original documents, figures, and MuSiQue direct assets; no authorship in the legal text is asserted. |
| `LICENSES/CC-BY-SA-4.0.txt` | HotpotQA CC BY-SA 4.0 aggregate material | Official CC BY-SA 4.0 legal text retained as the notice for the scoped HotpotQA aggregate material; no authorship in the legal text is asserted. |

## Directly scoped paths outside this table

- `data/table1_hotpotqa.csv`, `data/figure2_hotpotqa_differences.csv`, `config/hotpotqa_formal_config.json`, and `figures/figure2_v106_docx_submission_equivalent.png` are governed by `HOT_POTQA_LICENSE_SCOPE.md`.
- `config/musique_fixed_pool_config.json`, `data/table2_musique.csv`, `data/figure3_musique_metrics.csv`, `data/musique_inferential_summary.csv`, and `figures/figure3_v106_docx_submission_equivalent.png` are governed by `MUSIQUE_LICENSE_SCOPE.md`.
- `releases/strict-sp-ablation-materials/` is governed by its explicit HotpotQA path entries in `HOT_POTQA_LICENSE_SCOPE.md`; its scripts, aggregate CSVs/metadata, and documentation retain their respective scoped licences.

## Candidate-release consequence

This public candidate intentionally omits the following private-workspace historical records because their release-state wording is time-bound: `HOT_POTQA_RELEASE_FINALIZATION_AUDIT.md`, `MUSIQUE_RELEASE_FINALIZATION_AUDIT.md`, and `README_EDIT_AUDIT.md`. They are not part of this candidate, are not referenced by its manifest, and do not alter the scientific content of the included aggregate materials.

The official licence texts in `LICENSES/` are retained only as the legal notices referenced by the path-specific scope records; they are not claimed as author-original works. No unlisted source or third-party material is granted a licence merely because it is present in this candidate.
