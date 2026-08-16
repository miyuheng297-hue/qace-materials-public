#!/usr/bin/env python3
"""Portable statement of the finalized aggregate statistical contract.

This module intentionally consumes no benchmark or item-level data. It exposes
the constants used to interpret the aggregate CSVs and can be imported by
downstream audit code.
"""
BOOTSTRAP_REPLICATES = 20_000
BOOTSTRAP_BASE_SEED = 20_260_814
METRICS = ("sp_precision", "sp_recall", "sp_f1", "average_evidence_count")
HOLM_FAMILY_TESTS = {
    "configuration_level": 12,
    "component_level_ablation": 20,
    "sensitivity_analysis": 8,
}


def paired_difference(target_mean: float, reference_mean: float) -> float:
    """Return the target-minus-reference aggregate contrast."""
    return target_mean - reference_mean


def percentile_ci_label() -> str:
    """Describe the interval convention without exposing bootstrap draws."""
    return "paired bootstrap percentile interval [2.5%, 97.5%]"


if __name__ == "__main__":
    print({"metrics": METRICS, "bootstrap_replicates": BOOTSTRAP_REPLICATES, "base_seed": BOOTSTRAP_BASE_SEED, "holm_family_tests": HOLM_FAMILY_TESTS, "ci": percentile_ci_label()})
