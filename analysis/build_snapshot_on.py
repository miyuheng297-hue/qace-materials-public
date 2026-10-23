import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/root/rivermind-data/qace_paper_upgrade_20261022")
KG_ON = BASE / "kg_on"
OUT = BASE / "work"
OUT.mkdir(parents=True, exist_ok=True)

groups = defaultdict(list)
for p in sorted(KG_ON.glob("trace_*.jsonl")):
    with p.open() as f:
        for line in f:
            r = json.loads(line)
            groups[r["sample_id"]].append(r)

print("questions:", len(groups))

snap_path = OUT / "kg_on_snapshot.jsonl"
sel_path = OUT / "kg_on_selections.json"
sel = {}
with snap_path.open("w") as out:
    for sid in sorted(groups):
        rows = groups[sid]
        cands = []
        for r in rows:
            cands.append(
                {
                    "candidate_id": f'{r["title"]}##{r["sentence_index"]}',
                    "title": r["title"],
                    "sentence_index": int(r["sentence_index"]),
                    "text": r.get("sentence_text") or r.get("node_text") or "",
                    "raw_bge_score": r["raw_qace_bge_score"],
                    "normalized_bge_score": r.get("normalized_score"),
                    "upstream_rank": int(r.get("parent_order", r["candidate_position"])),
                    "upstream_score": r.get("parent_score"),
                }
            )
        rec = {
            "sample_id": sid,
            "question": rows[0].get("question", ""),
            "candidate_pool_capacity": rows[0].get("candidate_pool_size", len(cands)),
            "candidates": cands,
            "raw_bge_scores": [c["raw_bge_score"] for c in cands],
            "normalized_bge_scores": [c["normalized_bge_score"] for c in cands],
        }
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        sel[sid] = [[r["title"], int(r["sentence_index"])] for r in rows if r.get("final_selected")]

sel_path.write_text(json.dumps({"sp": sel}, ensure_ascii=False))
print("snapshot rows:", len(groups), "->", snap_path)
print("selections ->", sel_path)

counts = [len(v) for v in sel.values()]
print("mean selected:", sum(counts) / len(counts))
