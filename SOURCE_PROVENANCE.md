# Source Provenance

## Authoritative Manuscript Assets

The v10.6 DOCX is the authoritative final-figure asset source for this package. The three package PNG files are byte-for-byte copies of `word/media/image1.png`, `word/media/image2.png`, and `word/media/image3.png` in that DOCX, in Figure 1, Figure 2, and Figure 3 order respectively. The files are submission-equivalent raster final assets, not reconstructed illustrations or regenerated plots.

The v10.6 PDF contains the corresponding raster image objects. `scripts/validate_final_figure_assets.py` verifies the supplied manuscript pair by their SHA-256 hashes, confirms the DOCX relationships and figure-caption anchors, verifies the PDF object stream hashes and dimensions, and compares the scaled PDF and DOCX pixels. The expected evidence is machine-readable in `figures/source_metadata/figure_asset_provenance.json`.

## Editable-Source Search Result

The restricted local search covered SVG, EPS, PDF, PNG/JPEG, and plotting-script names and figure-related text under the available KG2RAG materials. It found no same-version editable SVG, PDF, EPS, or script that generated the three v10.6 final embedded images. The older SVG files and generator present in the input candidate were a different layout and were removed from v2. No approximate vector replacement is supplied.

## Retained Numeric Sources

`data/figure2_hotpotqa_differences.csv` and `data/figure3_musique_metrics.csv` are retained because `scripts/validate_aggregate_results.py` confirms they are exact v10.6 transformations/projections of `data/table1_hotpotqa.csv` and `data/table2_musique.csv`, including all displayed values. No other figure CSV or plotting script is retained.

## Caveat Provenance

The manuscript Table 1 note and formal audit statements are transcribed exactly in `audit/EXECUTION_INTEGRITY_CAVEAT.md`. The retained qualification is about four historical unsaved non-string initial attempts and strict clean-run validity; it does not disclose or include any failure sample, log, response, identifier, or benchmark content.
