# Figure Reproduction and Asset Status

The package distributes the exact current standalone figure displays used in the latest LaTeX manuscript:

| Figure | PNG | vector PDF | manuscript page | numeric source |
|---|---|---|---:|---|
| 1 | `figures/Fig1.png` | `figures/Fig1.pdf` | 6 | conceptual schematic |
| 2 | `figures/Fig2.png` | `figures/Fig2.pdf` | 12 | `data/figure2_hotpotqa_differences.csv` |
| 3 | `figures/Fig3.png` | `figures/Fig3.pdf` | 14 | `data/figure3_musique_metrics.csv` |
| 4 | `figures/Fig4.png` | `figures/Fig4.pdf` | 16 | strict SP-only CSVs in the nested package |

PNG and PDF hashes, dimensions, labels, and manuscript embedding checks are recorded in `figures/source_metadata/figure_asset_provenance.json`. The numerical displays were reconciled against the retained aggregate CSVs and the audited Table 1--4 sources; no new model run, retrieval, generation, bootstrap, or evaluation was performed for this release.

The PDFs contain embedded font subsets needed for selectable labels. No font files are redistributed and no font ownership is asserted.

The release does not claim an editable plotting source. SVG files and plotting scripts remain excluded pending explicit item-level public-release authorization. The standalone vector PDFs are provided for inspection and typesetting, not as a claim that the public package can recreate the manuscript from raw benchmark inputs.
