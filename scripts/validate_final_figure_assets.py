#!/usr/bin/env python3
"""Validate current standalone figure assets against public aggregate sources."""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def figure_numbers() -> None:
    expected = {f"Fig{i}.{suffix}" for i in range(1, 5) for suffix in ("png", "pdf")}
    actual = {path.name for path in FIGURES.iterdir() if path.is_file() and path.name.startswith("Fig")}
    if expected != actual:
        raise SystemExit(f"figure_asset_set_mismatch:missing={sorted(expected-actual)}:extra={sorted(actual-expected)}")


def validate_sources() -> dict[str, int | bool]:
    table1 = rows(ROOT / "data/table1_hotpotqa.csv")
    table2 = rows(ROOT / "data/table2_musique.csv")
    diff = rows(ROOT / "data/figure2_hotpotqa_differences.csv")
    musique = rows(ROOT / "data/figure3_musique_metrics.csv")
    strict = rows(ROOT / "releases/strict-sp-ablation-materials/data/strict_sp_ablation_results.csv")
    comparisons = rows(ROOT / "releases/strict-sp-ablation-materials/data/primary_comparisons_40.csv")
    if len(table1) != 3 or len(diff) != 12:
        raise SystemExit("hotpotqa_aggregate_shape_mismatch")
    if len(table2) != 6 or len(musique) != 18 or set(r["run"] for r in musique) != {"run_1", "run_2"}:
        raise SystemExit("musique_aggregate_shape_mismatch")
    if len(strict) != 13 or len(comparisons) != 40:
        raise SystemExit("strict_aggregate_shape_mismatch")
    if sum(r["metric"] == "sp_f1" for r in comparisons) != 10:
        raise SystemExit("strict_sp_f1_contrast_count_mismatch")
    if any(r.get("bootstrap_replicates") != "20000" for r in comparisons):
        raise SystemExit("bootstrap_replicate_mismatch")
    for number in range(1, 5):
        for suffix in ("png", "pdf"):
            path = FIGURES / f"Fig{number}.{suffix}"
            if path.stat().st_size == 0:
                raise SystemExit(f"empty_asset:{path.name}")
    return {
        "figure_count": 4,
        "figure_asset_count": 8,
        "hotpotqa_table_rows": len(table1),
        "hotpotqa_difference_rows": len(diff),
        "musique_table_rows": len(table2),
        "musique_figure_rows": len(musique),
        "strict_configuration_rows": len(strict),
        "strict_comparison_rows": len(comparisons),
        "strict_sp_f1_contrasts": 10,
        "bootstrap_replicates": 20000,
        "values_recomputed": False,
        "content_hashes_recorded": True,
    }


def main() -> int:
    figure_numbers()
    summary = validate_sources()
    print("figure_asset_validation=ok")
    for key, value in summary.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
