# Figure Reproduction and Final-Asset Status

The files in `figures/` are the v10.6 final submission-equivalent figures. They are PNG files copied byte-for-byte from the actual embedded DOCX media, not regenerated from a replacement script. The DOCX uses only raster media for Figure 1--3. A restricted local search found no same-version editable SVG, PDF, EPS, or final-figure-generation script; therefore the package does not claim an editable vector source and does not substitute an approximate drawing.

| Figure | Final package file | DOCX media member | v10.6 same-version status | Editable vector source |
|---|---|---|---|---|
| Figure 1 | `figures/figure1_v106_docx_submission_equivalent.png` | `word/media/image1.png` | Yes; exact embedded-media copy | No same-version source found |
| Figure 2 | `figures/figure2_v106_docx_submission_equivalent.png` | `word/media/image2.png` | Yes; exact embedded-media copy | No same-version source found |
| Figure 3 | `figures/figure3_v106_docx_submission_equivalent.png` | `word/media/image3.png` | Yes; exact embedded-media copy; this is the v10.6 three-panel result figure | No same-version source found |

## Figure 2 and Figure 3 Data Boundary

Only the source CSV files that agree with the v10.6 final figures are retained:

- `data/figure2_hotpotqa_differences.csv`, checked against `data/table1_hotpotqa.csv` as percentage-point transformations.
- `data/figure3_musique_metrics.csv`, checked against `data/table2_musique.csv` as separate run-by-configuration metric values.

The previously supplied SVG generator is deliberately absent: its layout is not the v10.6 submission layout. No other final-figure plotting script was found, so no plotting script is retained or represented as a source for these PNGs.

## Verification Commands

```text
python3 scripts/validate_aggregate_results.py
python3 scripts/validate_portable_manifest.py
python3 scripts/validate_final_figure_assets.py --docx /path/to/QACE_manuscript_v10_6_format_ready.docx --pdf /path/to/QACE_manuscript_v10_6_format_ready.pdf
```

The final command verifies DOCX relationship mapping, embedded-media hashes and dimensions, Figure 1--3 caption anchors, PDF image-object hashes and dimensions, and a scale-normalized visual comparison using Pillow. Its expected manuscript hashes and object correspondence are stored in `figures/source_metadata/figure_asset_provenance.json`.
