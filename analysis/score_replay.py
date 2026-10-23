"""Score the full-coverage answer replay and compare the two primary conditions."""

import json
import re
import string
from pathlib import Path

import numpy as np

OUT = Path("/root/rivermind-data/qace_paper_upgrade_20261022/work/answers")


def norm(s):
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def em_f1(pred, gold):
    p, g = norm(pred), norm(gold)
    em = 1.0 if p == g else 0.0
    pt, gt = p.split(), g.split()
    common = set(pt) & set(gt)
    if not common:
        return em, 0.0
    prec, rec = len(common) / len(pt), len(common) / len(gt)
    return em, 2 * prec * rec / (prec + rec)


def load(name):
    path = OUT / f"{name}.jsonl"
    rows = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            rows[r["sample_id"]] = r
    return rows


q = load("qace")
b = load("bge")
ids = sorted(set(q) & set(b))
print(f"paired questions: {len(ids)}  (qace {len(q)}, bge {len(b)})")

qe, qf, be, bf = [], [], [], []
for sid in ids:
    e1, f1 = em_f1(q[sid]["answer"], q[sid]["gold_answer"])
    e2, f2 = em_f1(b[sid]["answer"], b[sid]["gold_answer"])
    qe.append(e1); qf.append(f1); be.append(e2); bf.append(f2)

print(f"QACE  EM={np.mean(qe):.4f}  F1={np.mean(qf):.4f}")
print(f"BGE   EM={np.mean(be):.4f}  F1={np.mean(bf):.4f}")
d = np.array(qf) - np.array(bf)
rng = np.random.default_rng(20261023)
idx = rng.integers(0, len(d), size=(20000, len(d)))
means = d[idx].mean(axis=1)
print(f"delta F1 = {d.mean():+.6f}  95% CI [{np.quantile(means,0.025):+.6f}, {np.quantile(means,0.975):+.6f}]")

# first 1000 in file order, to compare with the published 1,000-sample replay
first = ids[:1000]
sel = [i for i, s in enumerate(ids) if s in set(first)]
print(f"\nfirst-1000 subset: QACE F1={np.mean([qf[i] for i in sel]):.4f}  BGE F1={np.mean([bf[i] for i in sel]):.4f}")
