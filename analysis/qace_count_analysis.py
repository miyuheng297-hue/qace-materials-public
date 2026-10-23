#!/usr/bin/env python3
"""Count-controlled support-fact evaluation and budget-conditioned loss decomposition.

Reads a frozen candidate-pool snapshot (one JSON object per question) plus a gold
supporting-fact file, materialises several selection conditions, and reports
macro-averaged SP-P/SP-R/SP-F1 together with the recall/F1 loss decomposition.

The selector semantics mirror KG2RAG/code/controlled_full_sp_only.py:
  * floor 0.15, fallback prefix 3, redundancy penalty 0.05, min-recall refill 5, hard cap 7
  * BGE order = raw score desc, upstream rank asc on exact ties
A `--pattern-blend` of 0 is used whenever the snapshot carries no pattern score.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

import numpy as np

FLOOR = 0.15
FALLBACK = 3
PENALTY = 0.05
MIN_RECALL = 5
CAP_HARD = 7


# ---------------------------------------------------------------- loading


def _candidate_field(cand: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in cand and cand[name] is not None:
            return cand[name]
    return default


def load_questions(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            cands = []
            raw_scores = rec.get("raw_bge_scores") or []
            norm_scores = rec.get("normalized_bge_scores") or []
            for pos, cand in enumerate(rec["candidates"]):
                raw = _candidate_field(cand, "raw_bge_score")
                if raw is None and pos < len(raw_scores):
                    raw = raw_scores[pos]
                norm = _candidate_field(cand, "normalized_bge_score")
                if norm is None and pos < len(norm_scores):
                    norm = norm_scores[pos]
                cands.append(
                    {
                        "candidate_id": _candidate_field(cand, "candidate_id", default=f"p{pos}"),
                        "title": cand["title"],
                        "sentence_index": int(cand["sentence_index"]),
                        "text": _candidate_field(cand, "text", "sentence_text", "node_text", default=""),
                        "raw": None if raw is None else float(raw),
                        "norm": None if norm is None else float(norm),
                        "upstream_rank": int(_candidate_field(cand, "upstream_rank", "parent_order", "candidate_position", default=pos)),
                        "upstream_score": _candidate_field(cand, "upstream_score", "parent_score", default=None),
                    }
                )
            rows.append({"sample_id": str(rec["sample_id"]), "question": rec.get("question", ""), "candidates": cands})
    return rows


def load_gold(path: Path) -> dict[str, list[tuple[str, int]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    gold: dict[str, list[tuple[str, int]]] = {}
    if isinstance(payload, dict):
        items = payload.items()
    else:
        items = ((row["sample_id"], row["supporting_facts"]) for row in payload)
    for sample_id, facts in items:
        gold[str(sample_id)] = [(str(t), int(i)) for t, i in facts]
    return gold


# ---------------------------------------------------------------- selector


def fact(cand: dict[str, Any]) -> tuple[str, int]:
    return (cand["title"], cand["sentence_index"])


def _raw(cand: dict[str, Any]) -> float:
    return float("-inf") if cand["raw"] is None else cand["raw"]


def _norm(cand: dict[str, Any]) -> float:
    return float("-inf") if cand["norm"] is None else cand["norm"]


def unique(cands: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen, out = set(), []
    for cand in cands:
        key = fact(cand)
        if key not in seen:
            seen.add(key)
            out.append(cand)
    return out


def bge_rank(cands: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return unique(sorted(cands, key=lambda c: (-_raw(c), c["upstream_rank"])))


def upstream_rank_order(cands: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return unique(sorted(cands, key=lambda c: c["upstream_rank"]))


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def _tokens(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(text.lower()))


def redundant(cand: dict[str, Any], selected: list[dict[str, Any]]) -> bool:
    cand_tokens = _tokens(cand["text"])
    for chosen in selected:
        if cand["title"] == chosen["title"]:
            return True
        chosen_tokens = _tokens(chosen["text"])
        if cand_tokens and chosen_tokens:
            union = len(cand_tokens | chosen_tokens)
            if union and len(cand_tokens & chosen_tokens) / union >= 0.80:
                return True
    return False


def select_qace(
    cands: list[dict[str, Any]],
    *,
    target: int,
    pattern_blend: float = 0.0,
    redundancy_penalty: float = PENALTY,
    selection_floor: float | None = FLOOR,
    min_recall_budget: int = MIN_RECALL,
) -> list[dict[str, Any]]:
    if not cands:
        return []
    ranked = bge_rank(cands)
    scored = []
    for cand in cands:
        blend = pattern_blend if pattern_blend and cand.get("pattern") is not None else 0.0
        score = (1.0 - blend) * _norm(cand)
        scored.append((score, _raw(cand), cand["upstream_rank"], cand))
    scored.sort(key=lambda r: (-r[0], -r[1], r[2]))

    selected: list[dict[str, Any]] = []
    chosen = set()
    for cand in ranked[:FALLBACK]:
        if selection_floor is not None and _norm(cand) < selection_floor:
            continue
        selected.append(cand)
        chosen.add(fact(cand))

    remaining = [r for r in scored if fact(r[3]) not in chosen]
    while remaining and len(selected) < target:
        eligible = [r for r in remaining if selection_floor is None or _norm(r[3]) >= selection_floor]
        if not eligible:
            break
        best = max(
            eligible,
            key=lambda r: (
                r[0] - (redundancy_penalty if redundancy_penalty > 0 and selected and redundant(r[3], selected) else 0.0),
                r[1],
                -r[2],
            ),
        )
        selected.append(best[3])
        chosen.add(fact(best[3]))
        remaining.remove(best)

    selected = selected[: min(target, CAP_HARD)]
    if min_recall_budget > 0:
        for cand in ranked:
            if len(selected) >= min(min_recall_budget, 10, CAP_HARD):
                break
            if fact(cand) not in chosen:
                selected.append(cand)
                chosen.add(fact(cand))
    return selected[:CAP_HARD]


# ---------------------------------------------------------------- metrics


def one_metrics(pred: list[tuple[str, int]], gold: list[tuple[str, int]]) -> tuple[float, float, float]:
    p_set, g_set = set(pred), set(gold)
    hit = len(p_set & g_set)
    if not p_set and not g_set:
        return 1.0, 1.0, 1.0
    precision = hit / len(p_set) if p_set else 0.0
    recall = hit / len(g_set) if g_set else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1


def decompose(sel: list[tuple[str, int]], pool: set[tuple[str, int]], gold: list[tuple[str, int]]) -> dict[str, float]:
    g = len(set(gold))
    h = len(set(gold) & pool)
    k = len(sel)
    t = len(set(sel) & set(gold))
    denom = g + k
    return {
        "g": g,
        "h": h,
        "k": k,
        "t": t,
        "pool_size": len(pool),
        "recall_pool_absent_loss": (g - h) / g if g else 0.0,
        "recall_capacity_loss": (h - min(k, h)) / g if g else 0.0,
        "recall_selection_loss": (min(k, h) - t) / g if g else 0.0,
        "f1_count_mismatch_loss": abs(g - k) / denom if denom else 0.0,
        "f1_supply_loss": (2 * (min(k, g) - min(k, h)) / denom) if denom else 0.0,
        "f1_selection_loss": (2 * (min(k, h) - t) / denom) if denom else 0.0,
        "fixed_count_oracle_f1": (2 * min(k, h) / denom) if denom else 0.0,
    }


# ---------------------------------------------------------------- statistics


def paired_bootstrap(diffs: np.ndarray, replicates: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = diffs.shape[0]
    idx = rng.integers(0, n, size=(replicates, n), dtype=np.int64)
    means = diffs[idx].mean(axis=1)
    return float(np.quantile(means, 0.025, method="linear")), float(np.quantile(means, 0.975, method="linear"))


def sign_flip_p(diffs: np.ndarray, replicates: int, seed: int) -> tuple[float, int, int]:
    nonzero = diffs[diffs != 0]
    if nonzero.size == 0:
        return 1.0, 0, 0
    observed = abs(float(nonzero.sum()))
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(replicates):
        signs = rng.integers(0, 2, size=nonzero.size) * 2 - 1
        if abs(float((nonzero * signs).sum())) >= observed - 1e-12:
            extreme += 1
    return (extreme + 1) / (replicates + 1), extreme, int(nonzero.size)


# ---------------------------------------------------------------- driver


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--qace", default=None, help="archived QACE selection JSON (with an 'sp' mapping)")
    ap.add_argument("--bootstrap", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261022)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = load_questions(Path(args.questions))
    gold = load_gold(Path(args.gold))
    ids = [r["sample_id"] for r in rows if r["sample_id"] in gold]
    by_id = {r["sample_id"]: r for r in rows}
    missing_gold = len(rows) - len(ids)

    qace_sp: dict[str, list[tuple[str, int]]] = {}
    if args.qace:
        payload = json.loads(Path(args.qace).read_text(encoding="utf-8"))
        raw_sp = payload["sp"] if isinstance(payload, dict) and "sp" in payload else payload
        for sid, facts in raw_sp.items():
            qace_sp[str(sid)] = [(str(t), int(i)) for t, i in facts]
        ids = [sid for sid in ids if sid in qace_sp]
        print(f"[qace] {args.qace}: {len(qace_sp)} selections, {len(ids)} matched to gold")

    conditions: dict[str, dict[str, list[tuple[str, int]]]] = {}
    for k in range(5, 11):
        conditions[f"UPSTREAM_K{k}"] = {}
        conditions[f"BGE_K{k}"] = {}
    if qace_sp:
        conditions["QACE_FULL_REPLAY"] = {}
        conditions["BGE_MATCH_QACE_COUNT"] = {}
    else:
        for target in (5, 6, 7):
            conditions[f"QACE_ORDER_K{target}"] = {}
        conditions["BGE_MATCH_QACE7"] = {}

    per_question = {}
    for sid in ids:
        cands = by_id[sid]["candidates"]
        gold_f = gold[sid]
        pool = {fact(c) for c in cands}
        up = upstream_rank_order(cands)
        bg = bge_rank(cands)
        for k in range(5, 11):
            conditions[f"UPSTREAM_K{k}"][sid] = [fact(c) for c in up[:k]]
            conditions[f"BGE_K{k}"][sid] = [fact(c) for c in bg[:k]]
        if qace_sp:
            archived = qace_sp[sid]
            conditions["QACE_FULL_REPLAY"][sid] = archived
            conditions["BGE_MATCH_QACE_COUNT"][sid] = [fact(c) for c in bg[: len(archived)]]
        else:
            qace7 = select_qace(cands, target=7)
            conditions["QACE_ORDER_K7"][sid] = [fact(c) for c in qace7]
            conditions["BGE_MATCH_QACE7"][sid] = [fact(c) for c in bg[: len(qace7)]]
            for target in (5, 6):
                conditions[f"QACE_ORDER_K{target}"][sid] = [fact(c) for c in select_qace(cands, target=target)]
        per_question[sid] = {"gold": gold_f, "pool": pool}

    aggregate = {}
    per_sample_f1: dict[str, list[float]] = {}
    for name, sel in conditions.items():
        p_vals, r_vals, f_vals, counts = [], [], [], []
        dec_rows = []
        for sid in ids:
            pred = sel[sid]
            p, r, f = one_metrics(pred, gold[sid])
            p_vals.append(p)
            r_vals.append(r)
            f_vals.append(f)
            counts.append(len(pred))
            dec_rows.append(decompose(pred, per_question[sid]["pool"], gold[sid]))
        per_sample_f1[name] = f_vals
        agg = {
            "condition": name,
            "sample_count": len(ids),
            "sp_precision": float(np.mean(p_vals)),
            "sp_recall": float(np.mean(r_vals)),
            "sp_f1": float(np.mean(f_vals)),
            "avg_selected": float(np.mean(counts)),
        }
        for key in dec_rows[0]:
            agg[key] = float(np.mean([row[key] for row in dec_rows]))
        aggregate[name] = agg

    # paired comparisons against the matched-count baseline
    comparisons = []
    if qace_sp:
        pairs = [("QACE_FULL_REPLAY", "BGE_MATCH_QACE_COUNT")]
    else:
        pairs = [("QACE_ORDER_K7", "BGE_MATCH_QACE7")]
    for name, base_name in pairs:
        base = np.array(per_sample_f1[base_name])
        cur = np.array(per_sample_f1[name])
        diff = cur - base
        lo, hi = paired_bootstrap(diff, args.bootstrap, args.seed)
        p_value, extreme, nonzero = sign_flip_p(diff, args.bootstrap, args.seed + 1)
        comparisons.append(
            {
                "contrast": f"{name} minus {base_name}",
                "metric": "sp_f1",
                "mean_difference": float(diff.mean()),
                "ci95_low": lo,
                "ci95_high": hi,
                "p_value": p_value,
                "extreme_count": extreme,
                "nonzero_question_count": nonzero,
                "n_questions": int(diff.shape[0]),
                "win": int((diff > 1e-12).sum()),
                "tie": int((np.abs(diff) <= 1e-12).sum()),
                "loss": int((diff < -1e-12).sum()),
            }
        )

    payload = {
        "label": args.label,
        "questions_file": str(args.questions),
        "gold_file": str(args.gold),
        "sample_count": len(ids),
        "rows_without_gold": missing_gold,
        "protocol": {
            "floor": FLOOR,
            "fallback_prefix": FALLBACK,
            "redundancy_penalty": PENALTY,
            "min_recall_refill": MIN_RECALL,
            "hard_cap": CAP_HARD,
            "pattern_blend": 0.0,
            "pattern_blend_note": "snapshot carries no query-pattern score; blend forced to 0",
            "bootstrap_replicates": args.bootstrap,
            "bootstrap_seed": args.seed,
            "signflip_seed": args.seed + 1,
        },
        "aggregate": aggregate,
        "comparisons": comparisons,
    }
    (outdir / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["condition,sample_count,sp_precision,sp_recall,sp_f1,avg_selected,recall_pool_absent_loss,recall_capacity_loss,recall_selection_loss,f1_count_mismatch_loss,f1_supply_loss,f1_selection_loss,fixed_count_oracle_f1"]
    for name, agg in aggregate.items():
        lines.append(
            ",".join(
                [
                    name,
                    str(agg["sample_count"]),
                    f"{agg['sp_precision']:.10f}",
                    f"{agg['sp_recall']:.10f}",
                    f"{agg['sp_f1']:.10f}",
                    f"{agg['avg_selected']:.10f}",
                    f"{agg['recall_pool_absent_loss']:.10f}",
                    f"{agg['recall_capacity_loss']:.10f}",
                    f"{agg['recall_selection_loss']:.10f}",
                    f"{agg['f1_count_mismatch_loss']:.10f}",
                    f"{agg['f1_supply_loss']:.10f}",
                    f"{agg['f1_selection_loss']:.10f}",
                    f"{agg['fixed_count_oracle_f1']:.10f}",
                ]
            )
        )
    (outdir / "aggregate.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({k: {kk: round(vv, 6) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in aggregate.items()}, indent=2))
    print("COMPARISONS:", json.dumps(comparisons, indent=2))


if __name__ == "__main__":
    main()
