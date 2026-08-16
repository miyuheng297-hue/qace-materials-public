#!/usr/bin/env python3
"""Generate/check the aggregate-only Table 4 display subsets."""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
META = ROOT / "metadata"

PANEL_A = [
    "UPSTREAM_TOP10",
    "UPSTREAM_ORDER_FIXED7",
    "BGE_RANK_FIXED7",
    "SHARED_SELECTOR_FULL",
    "BGE_FLOOR_FIXED6",
    "BGE_FLOOR_FIXED7",
    "ABLATE_NO_BGE_RESCORING",
]
PANEL_B = [
    "ABLATE_NO_PATTERN_BLEND",
    "ABLATE_NO_REDUNDANCY_PENALTY",
    "ABLATE_NO_SELECTION_FLOOR",
    "ABLATE_NO_MIN_RECALL_REFILL",
    "ABLATE_NO_BGE_RESCORING",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render(rows: list[dict[str, str]], fieldnames: list[str]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def build() -> tuple[str, str, str]:
    aggregate = {r["configuration_id"]: r for r in read_csv(DATA / "strict_sp_ablation_results.csv")}
    comparisons = read_csv(DATA / "primary_comparisons_40.csv")
    labels = {r["configuration_id"]: r for r in read_csv(META / "configuration_display_names.csv")}
    registry = {r["configuration_id"]: r for r in read_csv(META / "configuration_registry_summary.csv")}

    panel_a_rows = []
    for order, cid in enumerate(PANEL_A, start=1):
        row = aggregate[cid]
        panel_a_rows.append({
            "panel": "A",
            "row_order": str(order),
            "configuration_id": cid,
            "display_name": labels[cid]["display_name"],
            "family": registry[cid]["family"],
            "sp_precision": row["sp_precision"],
            "sp_recall": row["sp_recall"],
            "sp_f1": row["sp_f1"],
            "average_evidence_count": row["average_evidence_count"],
        })

    panel_b_rows = []
    for order, cid in enumerate(PANEL_B, start=1):
        matches = [r for r in comparisons if r["family"] == "component_level_ablation" and r["target"] == cid and r["reference"] == "SHARED_SELECTOR_FULL" and r["metric"] == "sp_f1"]
        if len(matches) != 1:
            raise ValueError(f"expected one SP F1 comparison for {cid}, got {len(matches)}")
        r = matches[0]
        panel_b_rows.append({
            "panel": "B",
            "row_order": str(order),
            "target": r["target"],
            "target_display_name": labels[r["target"]]["display_name"],
            "reference": r["reference"],
            "reference_display_name": labels[r["reference"]]["display_name"],
            "family": r["family"],
            "metric": r["metric"],
            "observed_mean_difference": r["observed_mean_difference"],
            "ci_lower": r["ci_lower"],
            "ci_upper": r["ci_upper"],
            "p_value": r["p_value"],
            "holm_adjusted_p_value": r["holm_adjusted_p_value"],
            "holm_reject_0_05": r["holm_reject_0_05"],
            "bootstrap_replicates": r["bootstrap_replicates"],
            "bootstrap_seed": r["bootstrap_seed"],
        })

    detail_rows = []
    for order, cid in enumerate(PANEL_B, start=1):
        for r in comparisons:
            if r["family"] == "component_level_ablation" and r["target"] == cid and r["reference"] == "SHARED_SELECTOR_FULL":
                detail_rows.append({"comparison_order": str(order), **r})

    a = render(panel_a_rows, list(panel_a_rows[0]))
    b = render(panel_b_rows, list(panel_b_rows[0]))
    d = render(detail_rows, ["comparison_order", *[k for k in detail_rows[0] if k != "comparison_order"]])
    return a, b, d


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {
        DATA / "table4_panel_a.csv": build()[0],
        DATA / "table4_panel_b.csv": build()[1],
        DATA / "table4_panel_b_metric_details.csv": build()[2],
    }
    if args.check:
        mismatches = [str(path.name) for path, expected in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != expected]
        if mismatches:
            raise SystemExit("table4_outputs_mismatch:" + ",".join(mismatches))
        print("table4_generation_check=ok panel_a_rows=7 panel_b_comparisons=5 panel_b_metric_rows=20")
        return 0
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print("table4_outputs_written panel_a_rows=7 panel_b_comparisons=5 panel_b_metric_rows=20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
