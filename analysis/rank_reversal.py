#!/usr/bin/env python3
"""Rank-reversal experiment.

Compares several evidence selectors under two reporting conventions:

  natural     each selector runs at the budget it would use on its own
  controlled  every selector is forced to the same per-question count,
              namely the archived QACE selection count for that question

If the ranking of selectors changes between the two conventions, then a
literature comparison that ignores selection count is not interpretable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from qace_count_analysis import (
    FLOOR,
    MIN_RECALL,
    bge_rank,
    fact,
    load_gold,
    load_questions,
    one_metrics,
    upstream_rank_order,
    _norm,
)

SIGMA = 0.5
MMR_LAMBDA = 0.7


# ------------------------------------------------------------------ helpers


def _tokens(text: str) -> set[str]:
    import re

    return set(re.findall(r"[A-Za-z0-9]+", text.lower()))


def _similarity_matrix(cands: list[dict]) -> np.ndarray:
    """Gaussian kernel on Jaccard distance -> positive semi-definite."""
    toks = [_tokens(c["text"]) for c in cands]
    n = len(cands)
    sim = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = toks[i], toks[j]
            union = len(a | b)
            jac = (len(a & b) / union) if union else 0.0
            d = 1.0 - jac
            s = float(np.exp(-(d * d) / (2 * SIGMA * SIGMA)))
            sim[i, j] = sim[j, i] = s
    return sim


def _relevance(cands: list[dict]) -> np.ndarray:
    values = np.array([_norm(c) for c in cands], dtype=float)
    values[~np.isfinite(values)] = 0.0
    lo = values.min()
    if lo < 0:
        values = values - lo
    total = values.sum()
    if total <= 0:
        values = np.ones_like(values)
        total = values.sum()
    return values / total


def select_mmr(cands: list[dict], k: int, lam: float = MMR_LAMBDA) -> list[dict]:
    if not cands:
        return []
    rel = _relevance(cands)
    sim = _similarity_matrix(cands)
    chosen = [int(np.argmax(rel))]
    while len(chosen) < min(k, len(cands)):
        best, best_score = None, None
        for i in range(len(cands)):
            if i in chosen:
                continue
            redundancy = max(sim[i, j] for j in chosen)
            score = lam * rel[i] - (1.0 - lam) * redundancy
            if best_score is None or score > best_score:
                best, best_score = i, score
        if best is None:
            break
        chosen.append(best)
    return [cands[i] for i in chosen]


def select_dpp(cands: list[dict], k: int) -> list[dict]:
    if not cands:
        return []
    rel = _relevance(cands)
    sim = _similarity_matrix(cands)
    kernel = np.outer(rel, rel) * sim
    diag = np.diag(kernel).copy()
    chosen: list[int] = []
    while len(chosen) < min(k, len(cands)):
        if not chosen:
            best = int(np.argmax(diag))
        else:
            sub = kernel[np.ix_(chosen, chosen)]
            cross = kernel[:, chosen]
            try:
                proj = cross @ np.linalg.solve(sub, cross.T)
            except np.linalg.LinAlgError:
                proj = cross @ np.linalg.pinv(sub) @ cross.T
            residual = diag - np.diag(proj)
            residual[chosen] = -np.inf
            best = int(np.argmax(residual))
        if not np.isfinite(diag[best]):
            break
        chosen.append(best)
    return [cands[i] for i in chosen]


def select_random(cands: list[dict], k: int, seed: int, sample_id: str) -> list[dict]:
    if not cands:
        return []
    digest = hashlib.sha256(f"{seed}:{sample_id}".encode()).digest()
    rng = np.random.default_rng(int.from_bytes(digest[:8], "big"))
    order = rng.permutation(len(cands))
    return [cands[i] for i in order[: min(k, len(cands))]]


def select_floor_rule(cands: list[dict], cap: int) -> list[dict]:
    ranked = bge_rank(cands)
    selected, chosen = [], set()
    for cand in ranked[:3]:
        if _norm(cand) >= FLOOR:
            selected.append(cand)
            chosen.add(fact(cand))
    for cand in ranked:
        if len(selected) >= cap:
            break
        if fact(cand) not in chosen and _norm(cand) >= FLOOR:
            selected.append(cand)
            chosen.add(fact(cand))
    for cand in ranked:
        if len(selected) >= min(MIN_RECALL, cap):
            break
        if fact(cand) not in chosen:
            selected.append(cand)
            chosen.add(fact(cand))
    return selected[:cap]


def ranked_selection(cands: list[dict], order: str, k: int, seed: int, sample_id: str) -> list[dict]:
    if order == "upstream":
        return upstream_rank_order(cands)[:k]
    if order == "bge":
        return bge_rank(cands)[:k]
    if order == "mmr":
        return select_mmr(cands, k)
    if order == "dpp":
        return select_dpp(cands, k)
    if order == "random":
        return select_random(cands, k, seed, sample_id)
    raise ValueError(order)


# ------------------------------------------------------------------ driver


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--qace", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--seed", type=int, default=20261022)
    args = ap.parse_args()

    rows = load_questions(Path(args.questions))
    gold = load_gold(Path(args.gold))
    by_id = {r["sample_id"]: r for r in rows}

    payload = json.loads(Path(args.qace).read_text(encoding="utf-8"))
    raw_sp = payload["sp"] if isinstance(payload, dict) and "sp" in payload else payload
    qace_sp = {str(sid): [(str(t), int(i)) for t, i in f] for sid, f in raw_sp.items()}

    ids = [sid for sid in (r["sample_id"] for r in rows) if sid in gold and sid in qace_sp]

    # selector id -> (natural order, natural k, callable)
    natural_specs = {
        "UPSTREAM_TOP10": ("upstream", 10),
        "BGE_TOP7": ("bge", 7),
        "BGE_FLOOR_TOP6": ("floor", 6),
        "MMR_TOP5": ("mmr", 5),
        "DPP_TOP5": ("dpp", 5),
        "RANDOM_TOP5": ("random", 5),
    }

    results: dict[str, dict] = {}
    natural_sel: dict[str, dict[str, list]] = {name: {} for name in natural_specs}
    natural_sel["QACE_FULL"] = {}
    controlled_sel: dict[str, dict[str, list]] = {name: {} for name in natural_specs}
    controlled_sel["QACE_FULL"] = {}

    for sid in ids:
        cands = by_id[sid]["candidates"]
        target = len(qace_sp[sid])
        natural_sel["QACE_FULL"][sid] = qace_sp[sid]
        controlled_sel["QACE_FULL"][sid] = qace_sp[sid]
        for name, (order, k) in natural_specs.items():
            if order == "floor":
                sel = select_floor_rule(cands, k)
            else:
                sel = ranked_selection(cands, order, k, args.seed, sid)
            natural_sel[name][sid] = [fact(c) for c in sel]
            if order == "floor":
                ctl = select_floor_rule(cands, target)
            else:
                ctl = ranked_selection(cands, order, target, args.seed, sid)
            controlled_sel[name][sid] = [fact(c) for c in ctl]

    def aggregate(store: dict[str, dict[str, list]]) -> dict[str, dict]:
        out = {}
        for name, sel in store.items():
            f1s, ps, rs, ks = [], [], [], []
            for sid in ids:
                pred = sel[sid]
                p, r, f = one_metrics(pred, gold[sid])
                ps.append(p)
                rs.append(r)
                f1s.append(f)
                ks.append(len(pred))
            out[name] = {
                "selector": name,
                "sp_precision": float(np.mean(ps)),
                "sp_recall": float(np.mean(rs)),
                "sp_f1": float(np.mean(f1s)),
                "avg_count": float(np.mean(ks)),
            }
        return out

    nat = aggregate(natural_sel)
    ctl = aggregate(controlled_sel)

    def ranker(table):
        return {name: i + 1 for i, name in enumerate(sorted(table, key=lambda n: -table[n]["sp_f1"]))}

    nat_rank, ctl_rank = ranker(nat), ranker(ctl)

    rows_out = []
    for name in nat:
        rows_out.append(
            {
                "selector": name,
                "natural_count": round(nat[name]["avg_count"], 4),
                "natural_sp_f1": round(nat[name]["sp_f1"], 6),
                "natural_rank": nat_rank[name],
                "controlled_count": round(ctl[name]["avg_count"], 4),
                "controlled_sp_f1": round(ctl[name]["sp_f1"], 6),
                "controlled_rank": ctl_rank[name],
                "rank_shift": nat_rank[name] - ctl_rank[name],
            }
        )
    rows_out.sort(key=lambda r: r["natural_rank"])

    names = list(nat)
    flips = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            before = np.sign(nat[a]["sp_f1"] - nat[b]["sp_f1"])
            after = np.sign(ctl[a]["sp_f1"] - ctl[b]["sp_f1"])
            if before != after and before != 0 and after != 0:
                flips.append(
                    {
                        "pair": [a, b],
                        "natural_margin": round(nat[a]["sp_f1"] - nat[b]["sp_f1"], 6),
                        "controlled_margin": round(ctl[a]["sp_f1"] - ctl[b]["sp_f1"], 6),
                    }
                )

    pairs = len(names) * (len(names) - 1) // 2
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    report = {
        "label": args.label,
        "sample_count": len(ids),
        "natural": nat,
        "controlled": ctl,
        "natural_ranking": [n for n in sorted(nat, key=lambda x: -nat[x]["sp_f1"])],
        "controlled_ranking": [n for n in sorted(ctl, key=lambda x: -ctl[x]["sp_f1"])],
        "pair_count": pairs,
        "reversal_count": len(flips),
        "reversals": flips,
        "rows": rows_out,
    }
    (outdir / "rank_reversal.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["selector,natural_count,natural_sp_f1,natural_rank,controlled_count,controlled_sp_f1,controlled_rank,rank_shift"]
    for row in rows_out:
        lines.append(
            ",".join(
                str(row[key])
                for key in (
                    "selector",
                    "natural_count",
                    "natural_sp_f1",
                    "natural_rank",
                    "controlled_count",
                    "controlled_sp_f1",
                    "controlled_rank",
                    "rank_shift",
                )
            )
        )
    (outdir / "rank_reversal.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(rows_out, indent=1))
    print(f"reversals: {len(flips)}/{pairs}")
    print(json.dumps(flips, indent=1))


if __name__ == "__main__":
    main()
