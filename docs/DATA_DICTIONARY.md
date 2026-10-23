# Data dictionary

All files are UTF-8. TSV files are tab-separated with a header row. JSONL files contain one
JSON object per line. No benchmark sentence text is included anywhere.

---

## `data/candidate_snapshot_scores.jsonl`

One line per question. 7,405 lines (HotpotQA distractor development split).

| field | type | description |
|---|---|---|
| `sample_id` | string | HotpotQA question id (`_id`) |
| `candidates` | array | up to 10 candidate sentences, in retrieval order |
| `candidates[].fact_id` | string | `sha256("title##sentence_index")[:16]` |
| `candidates[].position` | int | 0-based position in the frozen retrieval order |
| `candidates[].raw_bge_score` | float | cross-encoder score, 6 decimals |
| `candidates[].normalized_bge_score` | float or null | min-max normalised within the question |

The candidate pool is frozen: every selector in the study scores exactly these candidates with
exactly these scores.

---

## `data/selections/*.tsv`

One row per selected fact.

| field | type | description |
|---|---|---|
| `sample_id` | string | question id |
| `rank` | int | 1-based position in the selector's output order |
| `fact_id` | string | identifier of the selected fact |

Files:

| file | selector |
|---|---|
| `hotpotqa_composite_full.tsv` | the composite selector studied in the manuscript (7,405 questions) |
| `hotpotqa_bge_top7.tsv` | plain semantic reranking, top 7 |
| `hotpotqa_bge_floor_fixed6.tsv` | reranking with a score floor, cap 6 |
| `hotpotqa_upstream_top10.tsv` | original retrieval order, top 10 |
| `hotpotqa_upstream_fixed7.tsv` | original retrieval order, top 7 |
| `2wiki_composite_full.tsv` | the composite selector on 2WikiMultiHopQA (3,000 questions) |

The count-matched reranker is not stored separately: for each question it is the top `k`
candidates by `raw_bge_score`, where `k` is the number of rows for that question in
`hotpotqa_composite_full.tsv`, breaking ties by `position`.

---

## `data/per_question_f1.csv`

One row per question (7,405 rows).

| column | description |
|---|---|
| `sample_id` | question id |
| `selected_count` | number of facts selected by the composite selector (= matched count) |
| `composite_f1` | support-fact F1 of the composite selector |
| `matched_reranker_f1` | support-fact F1 of the count-matched reranker |
| `difference` | composite minus reranker |

Aggregating the last two columns reproduces 0.484894 and 0.485540, and their mean difference
reproduces -0.000646, the values reported in the manuscript.

---

## `data/answer_generations.jsonl`

One line per generated answer. 14,810 lines (2 conditions x 7,405 questions).

| field | type | description |
|---|---|---|
| `sample_id` | string | question id |
| `condition` | string | `composite` or `reranker` (the count-matched reranker) |
| `answer` | string | raw model output, not post-processed |

Generation settings: llama3:8b via Ollama, temperature 0, top-k 1, top-p 1, max 32 new tokens,
context window 3,900, fixed seed, identical prompt for both conditions.

Gold answers are not redistributed; they are recomputed from the public HotpotQA file.

---

## Reproducibility checks

| check | expected value |
|---|---|
| mean of `composite_f1` | 0.484894 |
| mean of `matched_reranker_f1` | 0.485540 |
| mean of `difference` | -0.000646 |
| questions with non-zero difference | 72 |
| win / tie / loss | 24 / 7,333 / 48 |
| lines in `candidate_snapshot_scores.jsonl` | 7,405 |
| lines in `answer_generations.jsonl` | 14,810 |
