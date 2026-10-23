#!/usr/bin/env python3
"""Threshold sensitivity with an independent split, rebuilt from the frozen trace.

Step 1 validates the re-implementation against the archived SHARED_SELECTOR_FULL
selection at floor = 0.15 (must match exactly).
Step 2 sweeps selection_floor, reporting count, SP-F1, and the count-matched BGE
baseline for every floor.
Step 3 does the honest version of the advisor's request: pick the floor on one
half of the questions and evaluate it on the other half.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

AUDIT = Path("/root/KG2RAG_upload2/KG2RAG/output/strict_sp_ablation_shared_snapshot_20260814/selection/candidate_audit.jsonl")
GOLD = Path("/root/rivermind-data/qace_paper_upgrade_20261022/work/hotpot_gold.json")
OUT = Path("/root/rivermind-data/qace_paper_upgrade_20261022/work/threshold")

CFG = "SHARED_SELECTOR_FULL"
BUDGET = {"simple": 5, "bridge": 6, "comparison": 7, "uncertain": 7}
PENALTY = 0.05
BLEND = 0.05
FALLBACK = 3
MIN_RECALL = 5
CAP = 7

TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def toks(text: str) -> frozenset:
    return frozenset(TOKEN_RE.findall((text or "").lower()))


def group_candidates() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    with AUDIT.open() as handle:
        for line in handle:
            rec = json.loads(line)
            state = rec["configuration_states"][CFG]
            sid = rec["sample_id"]
            groups.setdefault(sid, []).append(
                {
                    "title": rec["title"],
                    "idx": int(rec["sentence_index"]),
                    "raw": float(state["raw_bge_score"]),
                    "norm": float(state["normalized_bge_score"]),
                    "pattern": float(state["pattern_score"] or 0.0),
                    "up": int(state["upstream_rank"]),
                    "route": state["route"],
                    "details": state.get("route_details") or {},
                    "toks": toks(rec.get("text", "")),
                    "archived": bool(rec["final_selected_by_configuration"].get(CFG)),
                }
            )
    return groups


def fact(c):
    return (c["title"], c["idx"])


def redundant(cand, chosen) -> bool:
    for c in chosen:
        if cand["title"] == c["title"]:
            return True
        a, b = cand["toks"], c["toks"]
        union = len(a | b)
        if a and b and union and len(a & b) / union >= 0.80:
            return True
    return False


def bge_rank(cands):
    seen, out = set(), []
    for c in sorted(cands, key=lambda x: (-x["raw"], x["up"])):
        k = fact(c)
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out


def select(cands, floor):
    if not cands:
        return []
    route = cands[0]["route"]
    target = BUDGET.get(route, 7)
    details = cands[0]["details"]
    uncertain = bool(details.get("uncertain")) or float(details.get("confidence", 0.0)) < 0.45
    ranked = bge_rank(cands)

    scored = []
    for c in cands:
        score = c["norm"] if uncertain else (1 - BLEND) * c["norm"] + BLEND * c["pattern"]
        scored.append((score, c["raw"], c["up"], c))
    scored.sort(key=lambda r: (-r[0], -r[1], r[2]))

    chosen, picked = [], set()
    for c in ranked[:FALLBACK]:
        if floor is not None and c["norm"] < floor:
            continue
        chosen.append(c)
        picked.add(fact(c))

    remaining = [r for r in scored if fact(r[3]) not in picked]
    while remaining and len(chosen) < target:
        eligible = [r for r in remaining if floor is None or r[3]["norm"] >= floor]
        if not eligible:
            break
        best = max(
            eligible,
            key=lambda r: (
                r[0] - (PENALTY if (PENALTY > 0 and chosen and redundant(r[3], chosen)) else 0.0),
                r[1],
                -r[2],
            ),
        )
        chosen.append(best[3])
        picked.add(fact(best[3]))
        remaining.remove(best)

    chosen = chosen[: min(target, CAP)]
    if MIN_RECALL > 0:
        for c in ranked:
            if len(chosen) >= min(MIN_RECALL, 10, CAP):
                break
            if fact(c) not in picked:
                chosen.append(c)
                picked.add(fact(c))
    return chosen[:CAP]


def metrics(pred, gold):
    p, g = set(pred), set(gold)
    hit = len(p & g)
    if not p and not g:
        return 1.0, 1.0, 1.0
    prec = hit / len(p) if p else 0.0
    rec = hit / len(g) if g else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    groups = group_candidates()
    gold_raw = json.loads(GOLD.read_text())
    gold = {k: [(t, int(i)) for t, i in v] for k, v in gold_raw.items()}
    ids = [sid for sid in groups if sid in gold]
    print(f"questions: {len(ids)}", flush=True)

    # step 1: reproduce archived selection at 0.15
    mismatch = 0
    archived_total = 0
    for sid in ids:
        got = {fact(c) for c in select(groups[sid], 0.15)}
        want = {fact(c) for c in groups[sid] if c["archived"]}
        archived_total += len(want)
        mismatch += len(got ^ want)
    print(f"VALIDATION floor=0.15: symmetric difference {mismatch} / archived {archived_total}", flush=True)

    floors = [0.00, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.20, 0.25, 0.30]
    cache, rows = {}, []
    for floor in floors:
        sel = {sid: select(groups[sid], floor) for sid in ids}
        cache[floor] = sel
        counts, f1s, fb = [], [], []
        for sid in ids:
            chosen = [fact(c) for c in sel[sid]]
            matched = [fact(c) for c in bge_rank(groups[sid])][: len(chosen)]
            counts.append(len(chosen))
            f1s.append(metrics(chosen, gold[sid])[2])
            fb.append(metrics(matched, gold[sid])[2])
        rows.append(
            {
                "floor": floor,
                "avg_count": sum(counts) / len(ids),
                "sp_f1": sum(f1s) / len(ids),
                "matched_bge_f1": sum(fb) / len(ids),
                "delta_vs_matched": sum(f1s) / len(ids) - sum(fb) / len(ids),
            }
        )
        print(json.dumps(rows[-1]), flush=True)

    def half(sid):
        return int(hashlib.md5(sid.encode()).hexdigest(), 16) % 2

    A = [s for s in ids if half(s) == 0]
    B = [s for s in ids if half(s) == 1]

    def score_on(floor, subset):
        return sum(metrics([fact(c) for c in cache[floor][sid]], gold[sid])[2] for sid in subset) / len(subset)

    best = max(floors, key=lambda f: score_on(f, A))
    result = {
        "split_sizes": {"A": len(A), "B": len(B)},
        "chosen_on_A": best,
        "score_A_of_chosen": score_on(best, A),
        "score_B_of_chosen": score_on(best, B),
        "score_B_of_default_0_15": score_on(0.15, B),
        "gap_B_chosen_minus_default": score_on(best, B) - score_on(0.15, B),
        "validation_symmetric_difference": mismatch,
        "sweep": rows,
    }
    (OUT / "threshold_sensitivity.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    lines = ["floor,avg_count,sp_f1,matched_bge_f1,delta_vs_matched"]
    for r in rows:
        lines.append(f"{r['floor']},{r['avg_count']:.4f},{r['sp_f1']:.6f},{r['matched_bge_f1']:.6f},{r['delta_vs_matched']:+.6f}")
    (OUT / "threshold_sensitivity.csv").write_text("\n".join(lines) + "\n")
    print("BEST on A:", best, "| B chosen", round(result["score_B_of_chosen"], 6),
          "| B default", round(result["score_B_of_default_0_15"], 6), flush=True)


if __name__ == "__main__":
    main()
