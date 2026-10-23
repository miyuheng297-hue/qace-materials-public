#!/usr/bin/env python3
"""Mechanism analysis: where does the composite rule lose, and why.

Not a causal identification. For every question where QACE and the count-matched
BGE baseline select different sentences, this attributes the difference to one of
four observable mechanisms, and then checks whether the corresponding archived
ablation actually recovers the lost gold sentence.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

WS = Path(r"D:\Users\Administrator\Documents\deepseek-harness\default-workspace\qace_2wiki")
SNAP = WS.parent / ".." / "qace_2wiki" / "x"  # placeholder, replaced below
DATA = Path(r"E:\KG2RAG_PAPER\qace_2wiki_replication_20261022\source_data")
SEL = WS / "sel13"
DEV = WS / "hotpot_dev.json"
OUT = WS / "mechanism"
OUT.mkdir(parents=True, exist_ok=True)

SNAPSHOT = DATA / "hotpot_scored_shared_snapshot.jsonl"
GOLD = DATA / "hotpot_gold_by_id.json"
QACE = SEL / "SHARED_SELECTOR_FULL.json"


def load_snapshot(path):
    gaps = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            cands = []
            for c in rec["candidates"]:
                cands.append(
                    {
                        "title": c["title"],
                        "idx": int(c["sentence_index"]),
                        "raw": float(c["raw_bge_score"]),
                        "norm": float(c["normalized_bge_score"]),
                        "up": int(c["upstream_rank"]),
                    }
                )
            gaps[str(rec["sample_id"])] = cands
    return gaps


def load_sp(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload["sp"] if isinstance(payload, dict) and "sp" in payload else payload
    return {str(k): [(t, int(i)) for t, i in v] for k, v in raw.items()}


def f1(pred, gold):
    p, g = set(pred), set(gold)
    hit = len(p & g)
    if not p and not g:
        return 1.0
    prec = hit / len(p) if p else 0.0
    rec = hit / len(g) if g else 0.0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


def main():
    cands = load_snapshot(SNAPSHOT)
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    gold = {str(k): [(t, int(i)) for t, i in v] for k, v in gold.items()}
    qace = load_sp(QACE)

    dev = json.loads(DEV.read_text(encoding="utf-8"))
    meta = {str(r["_id"]): {"type": r.get("type"), "level": r.get("level")} for r in dev}

    abl = {
        "no_redundancy": load_sp(SEL / "ABLATE_NO_REDUNDANCY_PENALTY.json"),
        "no_floor": load_sp(SEL / "ABLATE_NO_SELECTION_FLOOR.json"),
        "no_pattern": load_sp(SEL / "ABLATE_NO_PATTERN_BLEND.json"),
        "no_refill": load_sp(SEL / "ABLATE_NO_MIN_RECALL_REFILL.json"),
    }

    ids = [s for s in cands if s in gold and s in qace]

    rows = []
    for sid in ids:
        pool = cands[sid]
        rank = sorted(pool, key=lambda c: (-c["raw"], c["up"]))
        sel_q = qace[sid]
        k = len(sel_q)
        sel_b = [(c["title"], c["idx"]) for c in rank[:k]]
        fq, fb = f1(sel_q, gold[sid]), f1(sel_b, gold[sid])
        rows.append(
            {
                "sid": sid,
                "k": k,
                "f1_qace": fq,
                "f1_bge": fb,
                "delta": fq - fb,
                "set_q": set(sel_q),
                "set_b": set(sel_b),
                "gold": set(gold[sid]),
                "pool": pool,
            }
        )

    diff = [r for r in rows if r["set_q"] != r["set_b"]]
    loss = [r for r in rows if r["delta"] < -1e-12]
    win = [r for r in rows if r["delta"] > 1e-12]
    print(f"differing sets: {len(diff)} | f1 loss {len(loss)} | win {len(win)} | tie {len(rows)-len(loss)-len(win)}")

    # ---- attribute each lost gold sentence
    reasons = Counter()
    per_question = []
    for r in loss:
        lost = list((r["set_b"] & r["gold"]) - r["set_q"])
        gained = list((r["set_q"] & r["gold"]) - r["set_b"])
        norm = {(c["title"], c["idx"]): c["norm"] for c in r["pool"]}
        rankmap = {(c["title"], c["idx"]): i + 1 for i, c in enumerate(sorted(r["pool"], key=lambda c: (-c["raw"], c["up"])))}
        titles_q = {t for t, _ in r["set_q"]}
        item_reasons = []
        for item in lost:
            if norm.get(item, 1.0) < 0.15:
                item_reasons.append("floor")
            elif item[0] in titles_q:
                item_reasons.append("redundancy")
            elif len(r["set_q"]) >= r["k"]:
                item_reasons.append("budget")
            else:
                item_reasons.append("ordering")
        reasons.update(item_reasons)
        dominant = Counter(item_reasons).most_common(1)[0][0] if item_reasons else "none"
        per_question.append(
            {
                "sid": r["sid"],
                "dominant": dominant,
                "lost": len(lost),
                "gained": len(gained),
                "type": meta.get(r["sid"], {}).get("type"),
                "level": meta.get(r["sid"], {}).get("level"),
                "lost_items": lost,
            }
        )

    gain_sum = sum(r["delta"] for r in win)
    loss_sum = sum(r["delta"] for r in loss)
    print(f"sum of positive deltas {gain_sum:+.6f} over {len(win)} | negative {loss_sum:+.6f} over {len(loss)}")

    win_reasons = Counter()
    for r in win:
        gained = list((r["set_q"] & r["gold"]) - r["set_b"])
        norm = {(c["title"], c["idx"]): c["norm"] for c in r["pool"]}
        rankmap = {(c["title"], c["idx"]): i + 1 for i, c in enumerate(sorted(r["pool"], key=lambda c: (-c["raw"], c["up"])))}
        for item in gained:
            if rankmap.get(item, 0) > r["k"]:
                win_reasons["beyond_bge_cut"] += 1
            elif norm.get(item, 0) >= 0.15:
                win_reasons["reordered_within_topk"] += 1
            else:
                win_reasons["other"] += 1
    print("win-side gained-item reasons:", dict(win_reasons))
    print("lost-item reasons:", dict(reasons))
    print("dominant reason per loss question:", dict(Counter(p["dominant"] for p in per_question)))

    # ---- does the matching ablation recover the lost gold?
    recovery = defaultdict(lambda: {"recovered_questions": 0, "total": 0})
    for p in per_question:
        lost = set(p["lost_items"])
        if not lost:
            continue
        for name, sp in abl.items():
            got = set(sp.get(p["sid"], []))
            recovery[name]["total"] += 1
            if lost & got:
                recovery[name]["recovered_questions"] += 1
    print("ablation recovery (questions where at least one lost gold reappears):")
    for name, v in recovery.items():
        print(f"  {name}: {v['recovered_questions']}/{v['total']}")

    # ---- stratification by type / level
    strat = defaultdict(lambda: {"n": 0, "delta_sum": 0.0, "loss": 0, "win": 0})
    for r in rows:
        key = (meta.get(r["sid"], {}).get("type"), meta.get(r["sid"], {}).get("level"))
        strat[key]["n"] += 1
        strat[key]["delta_sum"] += r["delta"]
        strat[key]["loss"] += 1 if r["delta"] < -1e-12 else 0
        strat[key]["win"] += 1 if r["delta"] > 1e-12 else 0
    print("\nby (type, level):")
    for key, v in sorted(strat.items(), key=lambda x: str(x[0])):
        print(f"  {key}: n={v['n']:5d} mean_delta={v['delta_sum']/v['n']:+.6f} loss={v['loss']:3d} win={v['win']:3d}")

    payload = {
        "counts": {
            "questions": len(rows),
            "differing_sets": len(diff),
            "f1_loss": len(loss),
            "f1_win": len(win),
            "f1_tie": len(rows) - len(loss) - len(win),
        },
        "lost_item_reasons": dict(reasons),
        "dominant_reason": dict(Counter(p["dominant"] for p in per_question)),
        "ablation_recovery": {k: dict(v) for k, v in recovery.items()},
        "stratification": {str(k): {"n": v["n"], "mean_delta": v["delta_sum"] / v["n"], "loss": v["loss"], "win": v["win"]} for k, v in strat.items()},
    }
    (OUT / "mechanism.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nwritten:", OUT / "mechanism.json")


if __name__ == "__main__":
    main()
