import csv
import json
from collections import defaultdict
from pathlib import Path

SRC = Path(r"E:\KG2RAG_PAPER\qace_2wiki_replication_20261022\source_data")
OUT = Path(r"E:\QACE_PLOS_ONE\supplementary")
OUT.mkdir(parents=True, exist_ok=True)

gold_raw = json.loads((SRC / "hotpot_gold_by_id.json").read_text(encoding="utf-8"))
sample = next(iter(gold_raw.items()))
print("gold keys:", list(sample[1].keys()) if isinstance(sample[1], dict) else type(sample[1]))

# normalise gold: id -> (set of (title, idx), type)
gold = {}
qtype = {}
for sid, v in gold_raw.items():
    if isinstance(v, dict):
        facts = v.get("sp") or v.get("facts") or v.get("supporting_facts")
        gold[sid] = {(str(t), int(i)) for t, i in facts}
        qtype[sid] = v.get("type") or v.get("question_type") or "unknown"
    else:
        gold[sid] = {(str(t), int(i)) for t, i in v}
        qtype[sid] = "unknown"

DEV = Path(r"D:\Users\Administrator\Documents\deepseek-harness\default-workspace\qace_2wiki\hotpot_dev.json")
if DEV.exists():
    for r in json.loads(DEV.read_text(encoding="utf-8")):
        qtype[str(r["_id"])] = r.get("type", "unknown")

sel_raw = json.loads((SRC / "hotpot_SHARED_SELECTOR_FULL.json").read_text(encoding="utf-8"))
sp = sel_raw["sp"] if isinstance(sel_raw, dict) and "sp" in sel_raw else sel_raw
qace = {str(k): [(str(t), int(i)) for t, i in v] for k, v in sp.items()}

# candidates per question with scores, preserving order
cands = defaultdict(list)
with (SRC / "hotpot_scored_shared_snapshot.jsonl").open(encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        sid = str(r["sample_id"])
        for c in r["candidates"]:
            cands[sid].append((str(c["title"]), int(c["sentence_index"]), float(c["raw_bge_score"])))


def f1(pred, g):
    p, gg = set(pred), set(g)
    hit = len(p & gg)
    if not p and not gg:
        return 1.0
    prec = hit / len(p) if p else 0.0
    rec = hit / len(gg) if gg else 0.0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


rows = []
by_type_q = defaultdict(list)
by_type_b = defaultdict(list)
sel_rows = []
for sid in sorted(set(qace) & set(gold) & set(cands)):
    q = qace[sid]
    k = len(q)
    ranked = sorted(cands[sid], key=lambda x: -x[2])[:k]
    b = [(t, i) for t, i, _ in ranked]
    fq, fb = f1(q, gold[sid]), f1(b, gold[sid])
    rows.append([sid, k, f"{fq:.6f}", f"{fb:.6f}", f"{fq-fb:+.6f}"])
    t = qtype.get(sid, "unknown")
    by_type_q[t].append(fq)
    by_type_b[t].append(fb)
    for sel, name in ((q, "composite"), (b, "reranker")):
        for (tt, ii) in sel:
            sel_rows.append([sid, name, tt, ii])

with (OUT / "S1_Table_per_question_f1.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sample_id", "selected_count", "composite_f1", "matched_reranker_f1", "difference"])
    w.writerows(rows)

with (OUT / "S2_Table_selected_sentences.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["sample_id", "selector", "title", "sentence_index"])
    w.writerows(sel_rows)

n = len(rows)
mean_q = sum(float(r[2]) for r in rows) / n
mean_b = sum(float(r[3]) for r in rows) / n
print(f"n={n}  composite={mean_q:.6f}  reranker={mean_b:.6f}  diff={mean_q-mean_b:+.6f}")

print("\nper question type:")
for t in sorted(by_type_q):
    a, b = by_type_q[t], by_type_b[t]
    print(f"  {t:12s} n={len(a):5d}  composite={sum(a)/len(a):.4f}  reranker={sum(b)/len(b):.4f}  diff={sum(a)/len(a)-sum(b)/len(b):+.5f}")

with (OUT / "per_type_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["question_type", "n", "composite_f1", "matched_reranker_f1", "difference"])
    for t in sorted(by_type_q):
        a, b = by_type_q[t], by_type_b[t]
        w.writerow([t, len(a), f"{sum(a)/len(a):.6f}", f"{sum(b)/len(b):.6f}", f"{sum(a)/len(a)-sum(b)/len(b):+.6f}"])

print("\nwritten to", OUT)
