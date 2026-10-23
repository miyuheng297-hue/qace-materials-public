# Reproduction guide

This directory contains the code and the machine-readable data needed to reproduce every
number and figure in the manuscript *"Count-matched evaluation shows no incremental benefit of
composite evidence selection over semantic reranking in multi-hop question answering"*.

No benchmark text is redistributed. Every candidate fact is identified by
`fact_id = sha256(f"{title}##{sentence_index}")[:16]`, which can be recomputed from the public
HotpotQA and 2WikiMultiHopQA files.

## Directory layout

```
analysis/            analysis scripts (Python 3.12)
data/
  candidate_snapshot_scores.jsonl   7,405 questions x 10 candidates, scores only
  selections/                       per-question selected facts, 6 selectors
  per_question_f1.csv               per-question F1, composite vs matched reranker
  answer_generations.jsonl          14,810 generated answers (2 conditions x 7,405)
docs/DATA_DICTIONARY.md             field-by-field description of every file
requirements.txt                    pinned dependencies
```

## Environment

```
python 3.12
numpy     (see requirements.txt)
```

Install with `pip install -r requirements.txt`.

## Step 0 - rebuild fact_id

Download `hotpot_dev_distractor_v1.json` from the HotpotQA distribution and compute, for every
`(title, sentence_index)` pair in the supporting facts and in the candidate paragraphs,

```python
import hashlib
fact_id = hashlib.sha256(f"{title}##{int(sentence_index)}".encode("utf-8")).hexdigest()[:16]
```

This is the only join key used by the released files.

## Step 1 - count-matched comparison (Table 2, Table 3, Fig 2)

```
python analysis/qace_count_analysis.py \
  --questions data/candidate_snapshot_scores.jsonl \
  --qace data/selections/hotpotqa_composite_full.tsv \
  --outdir results/matched
```

Produces the composite and count-matched-reranker SP-F1, the paired bootstrap interval, the
sign-flip p-value, the win/tie/loss counts and the budget-conditioned decomposition.

## Step 2 - ranking under two conventions (Table 4, Fig 1)

```
python analysis/rank_reversal.py \
  --questions data/candidate_snapshot_scores.jsonl \
  --qace data/selections/hotpotqa_composite_full.tsv \
  --outdir results/reversal
```

## Step 3 - equivalence testing (TOST)

```
python analysis/tost_equivalence.py \
  --questions data/candidate_snapshot_scores.jsonl \
  --qace data/selections/hotpotqa_composite_full.tsv \
  --outdir results/tost
```

## Step 4 - selection-floor sensitivity (Fig 3)

```
python analysis/threshold_sensitivity.py \
  --questions data/candidate_snapshot_scores.jsonl \
  --gold <gold file> \
  --outdir results/threshold
```

## Step 5 - where the composite rule loses (Table 5)

```
python analysis/mechanism_analysis.py --outdir results/mechanism
```

## Step 6 - answer layer (Section 4.9)

The generated answers are released as `data/answer_generations.jsonl`; scoring uses the same
normalisation as the manuscript (lower-case, strip punctuation and articles):

```
python analysis/score_replay.py --answers data/answer_generations.jsonl
```

## Notes on scope

- The frozen candidate pools were produced by the upstream KG2RAG pipeline, which is third-party
  software and is not redistributed here; it is described in the manuscript and cited.
- The knowledge-graph expansion condition (Section 4.6) requires the extracted subgraph data,
  which is derived from HotpotQA and is therefore not redistributed; the script that builds the
  expansion-on snapshot is included for reference (`analysis/build_snapshot_on.py`).
- MuSiQue results reported in the earlier release are not part of this manuscript.
