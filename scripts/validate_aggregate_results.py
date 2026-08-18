#!/usr/bin/env python3
"""Validate sanitized aggregate tables and current figure-source relationships."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPECTED_HOTPOTQA = {
    "B_parent_order_fixed7": {"answer_em":"0.500473","answer_f1":"0.629148","support_precision":"0.284713","support_recall":"0.827481","support_f1":"0.417716","official_joint_f1":"0.286584"},
    "D_bge_floor_fixed6": {"answer_em":"0.527346","answer_f1":"0.660107","support_precision":"0.353410","support_recall":"0.842048","support_f1":"0.490140","official_joint_f1":"0.347954"},
    "G_frozen_trace_replay": {"answer_em":"0.526131","answer_f1":"0.659146","support_precision":"0.346031","support_recall":"0.843842","support_f1":"0.482708","official_joint_f1":"0.341981"},
}
EXPECTED_MUSIQUE = {
    ("run_1","P5"): {"answer_em":"0.059164","answer_f1":"0.113512","paragraph_support_precision":"0.128506","paragraph_support_recall":"0.240381","paragraph_support_f1":"0.164565","derived_joint":"0.028979"},
    ("run_1","R5_F5"): {"answer_em":"0.196525","answer_f1":"0.285781","paragraph_support_precision":"0.396773","paragraph_support_recall":"0.773135","paragraph_support_f1":"0.516083","derived_joint":"0.161982"},
    ("run_1","D6"): {"answer_em":"0.185767","answer_f1":"0.277185","paragraph_support_precision":"0.347952","paragraph_support_recall":"0.811061","paragraph_support_f1":"0.479619","derived_joint":"0.142570"},
    ("run_2","P5"): {"answer_em":"0.057923","answer_f1":"0.112623","paragraph_support_precision":"0.128506","paragraph_support_recall":"0.240381","paragraph_support_f1":"0.164565","derived_joint":"0.028677"},
    ("run_2","R5_F5"): {"answer_em":"0.195283","answer_f1":"0.286837","paragraph_support_precision":"0.396773","paragraph_support_recall":"0.773135","paragraph_support_f1":"0.516083","derived_joint":"0.162961"},
    ("run_2","D6"): {"answer_em":"0.185767","answer_f1":"0.277185","paragraph_support_precision":"0.347952","paragraph_support_recall":"0.811061","paragraph_support_f1":"0.479619","derived_joint":"0.142570"},
}


def rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def close(actual: Decimal, expected: Decimal, tolerance: Decimal) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"aggregate mismatch: {actual} != {expected}")


def validate_hotpotqa() -> None:
    table = {row["configuration"]: row for row in rows("table1_hotpotqa.csv")}
    if set(table) != {"B_parent_order_fixed7", "D_bge_floor_fixed6", "G_frozen_trace_replay"}:
        raise AssertionError("unexpected HotpotQA configuration set")
    metric_map = {
        "Answer EM": "answer_em",
        "Answer F1": "answer_f1",
        "Support Precision": "support_precision",
        "Support Recall": "support_recall",
        "Support F1": "support_f1",
        "Official Joint F1": "official_joint_f1",
    }
    comparisons = {"D_minus_B": "D_bge_floor_fixed6", "G_minus_B": "G_frozen_trace_replay"}
    for config, expected_row in EXPECTED_HOTPOTQA.items():
        actual_row = {key: value for key, value in table[config].items() if key != "configuration"}
        if actual_row != expected_row:
            raise AssertionError(f"HotpotQA values do not match v10.6 manuscript: {config}")
    reference = table["B_parent_order_fixed7"]
    for row in rows("figure2_hotpotqa_differences.csv"):
        key = metric_map[row["metric"]]
        expected = (Decimal(table[comparisons[row["comparison"]]][key]) - Decimal(reference[key])) * Decimal(100)
        close(Decimal(row["difference_percentage_points"]), expected, Decimal("0.00011"))


def validate_musique() -> None:
    table_rows = rows("table2_musique.csv")
    if len(table_rows) != 6:
        raise AssertionError("Table 2 must have six aggregate rows")
    table = {(row["run"], row["configuration"]): row for row in table_rows}
    if set(table) != {(run, cfg) for run in ("run_1", "run_2") for cfg in ("P5", "R5_F5", "D6")}:
        raise AssertionError("unexpected MuSiQue run/configuration set")
    for key, expected_row in EXPECTED_MUSIQUE.items():
        actual_row = {field: value for field, value in table[key].items() if field not in {"run", "configuration"}}
        if actual_row != expected_row:
            raise AssertionError(f"MuSiQue values do not match v10.6 manuscript: {key}")
    metric_map = {"Answer F1": "answer_f1", "Paragraph Support F1": "paragraph_support_f1", "Derived Joint": "derived_joint"}
    for row in rows("figure3_musique_metrics.csv"):
        expected = Decimal(table[(row["run"], row["configuration"])][metric_map[row["metric"]]]) * Decimal(100)
        close(Decimal(row["value_percent"]), expected, Decimal("0.00001"))
    inferential = rows("musique_inferential_summary.csv")
    if len(inferential) != 12:
        raise AssertionError("inferential summary must have twelve aggregate tests")
    for row in inferential:
        expected = Decimal(row["holm_p"]) < Decimal("0.05")
        if (row["holm_significant"] == "true") != expected:
            raise AssertionError("Holm decision mismatch")


def main() -> int:
    validate_hotpotqa()
    validate_musique()
    strict_script = ROOT / "releases/strict-sp-ablation-materials/scripts/validate_aggregate_results.py"
    if not strict_script.is_file():
        raise AssertionError("strict aggregate validator is missing")
    print("aggregate_validation=ok hotpotqa_rows=3 musique_rows=6 figure2_rows=12 figure3_rows=18 strict_validator=present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
