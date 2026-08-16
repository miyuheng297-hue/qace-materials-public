#!/usr/bin/env python3
"""Validate aggregate schemas, relationships, and the Table 4 subsets."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CONFIGS = [
    "UPSTREAM_TOP10", "UPSTREAM_ORDER_FIXED7", "BGE_RANK_FIXED7", "SHARED_SELECTOR_FULL",
    "BGE_FLOOR_FIXED6", "BGE_FLOOR_FIXED7", "ABLATE_NO_PATTERN_BLEND",
    "ABLATE_NO_REDUNDANCY_PENALTY", "ABLATE_NO_SELECTION_FLOOR", "ABLATE_NO_MIN_RECALL_REFILL",
    "ABLATE_NO_BGE_RESCORING", "SENSITIVITY_MIN_RECALL_LOWER", "SENSITIVITY_MIN_RECALL_HIGHER",
]
METRICS = ["sp_precision", "sp_recall", "sp_f1", "average_evidence_count"]
PANEL_A = CONFIGS[:6] + ["ABLATE_NO_BGE_RESCORING"]
PANEL_B = ["ABLATE_NO_PATTERN_BLEND", "ABLATE_NO_REDUNDANCY_PENALTY", "ABLATE_NO_SELECTION_FLOOR", "ABLATE_NO_MIN_RECALL_REFILL", "ABLATE_NO_BGE_RESCORING"]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def close(a: str, b: float, tol: float = 1e-12) -> bool:
    return math.isclose(float(a), b, rel_tol=tol, abs_tol=tol)


def main() -> int:
    aggregate_rows = rows(DATA / "strict_sp_ablation_results.csv")
    if [r["configuration_id"] for r in aggregate_rows] != CONFIGS:
        raise SystemExit("aggregate_configuration_order_mismatch")
    if list(aggregate_rows[0]) != ["configuration_id", *METRICS]:
        raise SystemExit("aggregate_header_mismatch")
    aggregate = {r["configuration_id"]: r for r in aggregate_rows}
    for row in aggregate_rows:
        for metric in METRICS:
            value = float(row[metric])
            if not math.isfinite(value) or (metric != "average_evidence_count" and not 0 <= value <= 1):
                raise SystemExit(f"invalid_aggregate_value:{row['configuration_id']}:{metric}")

    comparison_rows = rows(DATA / "primary_comparisons_40.csv")
    if len(comparison_rows) != 40:
        raise SystemExit(f"comparison_row_count:{len(comparison_rows)}")
    family_counts = {family: sum(r["family"] == family for r in comparison_rows) for family in {r["family"] for r in comparison_rows}}
    if family_counts != {"configuration_level": 12, "component_level_ablation": 20, "sensitivity_analysis": 8}:
        raise SystemExit(f"holm_family_counts:{family_counts}")
    if any(r["bootstrap_replicates"] != "20000" for r in comparison_rows):
        raise SystemExit("bootstrap_replicates_mismatch")
    for r in comparison_rows:
        if r["metric"] not in METRICS:
            raise SystemExit(f"unknown_metric:{r['metric']}")
        expected = float(aggregate[r["target"]][r["metric"]]) - float(aggregate[r["reference"]][r["metric"]])
        if not close(r["observed_mean_difference"], expected):
            raise SystemExit(f"difference_mismatch:{r['target']}:{r['reference']}:{r['metric']}")

    panel_a = rows(DATA / "table4_panel_a.csv")
    if len(panel_a) != 7 or [r["configuration_id"] for r in panel_a] != PANEL_A:
        raise SystemExit("table4_panel_a_scope_mismatch")
    for r in panel_a:
        source = aggregate[r["configuration_id"]]
        for metric in METRICS:
            if r[metric] != source[metric]:
                raise SystemExit(f"table4_panel_a_value_mismatch:{r['configuration_id']}:{metric}")

    panel_b = rows(DATA / "table4_panel_b.csv")
    if len(panel_b) != 5 or [r["target"] for r in panel_b] != PANEL_B:
        raise SystemExit("table4_panel_b_scope_mismatch")
    for r in panel_b:
        matches = [x for x in comparison_rows if x["family"] == "component_level_ablation" and x["target"] == r["target"] and x["reference"] == "SHARED_SELECTOR_FULL" and x["metric"] == "sp_f1"]
        if len(matches) != 1:
            raise SystemExit(f"table4_panel_b_source_missing:{r['target']}")
        source = matches[0]
        for field in ("observed_mean_difference", "ci_lower", "ci_upper", "p_value", "holm_adjusted_p_value", "holm_reject_0_05", "bootstrap_replicates", "bootstrap_seed"):
            if r[field] != source[field]:
                raise SystemExit(f"table4_panel_b_value_mismatch:{r['target']}:{field}")
    details = rows(DATA / "table4_panel_b_metric_details.csv")
    if len(details) != 20:
        raise SystemExit(f"table4_panel_b_detail_count:{len(details)}")
    print("aggregate_validation=ok configurations=13 comparisons=40 table4_panel_a=7 table4_panel_b=5 table4_panel_b_metric_rows=20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
