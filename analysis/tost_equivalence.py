#!/usr/bin/env python3
"""Two one-sided tests (TOST) of equivalence for paired SP-F1 differences.

The paper's existing convention treats differences below roughly 0.0050 SP-F1
as not interpretable. This script turns that convention into a formal
equivalence test: the two selectors are declared equivalent at margin delta
when the 90% paired-bootstrap interval of the mean difference is contained in
(-delta, +delta), which is the standard TOST decision rule at alpha = 0.05.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from qace_count_analysis import (
    bge_rank,
    fact,
    load_gold,
    load_questions,
    one_metrics,
)


def paired_bootstrap_means(diffs: np.ndarray, replicates: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = diffs.shape[0]
    means = np.empty(replicates)
    batch = 128
    for start in range(0, replicates, batch):
        stop = min(start + batch, replicates)
        idx = rng.integers(0, n, size=(stop - start, n), dtype=np.int64)
        means[start:stop] = diffs[idx].mean(axis=1)
    return means


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--qace", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--replicates", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261022)
    args = ap.parse_args()

    rows = load_questions(Path(args.questions))
    gold = load_gold(Path(args.gold))
    by_id = {r["sample_id"]: r for r in rows}
    payload = json.loads(Path(args.qace).read_text(encoding="utf-8"))
    raw_sp = payload["sp"] if isinstance(payload, dict) and "sp" in payload else payload
    qace_sp = {str(sid): [(str(t), int(i)) for t, i in f] for sid, f in raw_sp.items()}

    ids = [sid for sid in (r["sample_id"] for r in rows) if sid in gold and sid in qace_sp]

    qace_f1, bge_f1 = [], []
    for sid in ids:
        cands = by_id[sid]["candidates"]
        g = gold[sid]
        q = qace_sp[sid]
        b = [fact(c) for c in bge_rank(cands)[: len(q)]]
        qace_f1.append(one_metrics(q, g)[2])
        bge_f1.append(one_metrics(b, g)[2])

    diffs = np.array(qace_f1) - np.array(bge_f1)
    boot = paired_bootstrap_means(diffs, args.replicates, args.seed)

    lo95, hi95 = float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))
    lo90, hi90 = float(np.quantile(boot, 0.05)), float(np.quantile(boot, 0.95))

    margins = [0.0025, 0.005, 0.010]
    table = []
    for delta in margins:
        equivalent = (lo90 > -delta) and (hi90 < delta)
        table.append(
            {
                "margin": delta,
                "ci90": [lo90, hi90],
                "equivalent": bool(equivalent),
                "n_beyond_margin": int((np.abs(diffs) > delta).sum()),
                "share_beyond_margin": float((np.abs(diffs) > delta).mean()),
            }
        )

    out = {
        "label": args.label,
        "sample_count": len(ids),
        "mean_difference": float(diffs.mean()),
        "sd_difference": float(diffs.std(ddof=1)),
        "ci95": [lo95, hi95],
        "ci90": [lo90, hi90],
        "win": int((diffs > 1e-12).sum()),
        "tie": int((np.abs(diffs) <= 1e-12).sum()),
        "loss": int((diffs < -1e-12).sum()),
        "max_abs_difference": float(np.abs(diffs).max()),
        "tost": table,
        "bootstrap_replicates": args.replicates,
        "bootstrap_seed": args.seed,
    }

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "tost.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
