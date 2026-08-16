# Third-Party Notices and Final Checks

This strict supporting-fact package distributes no third-party source code, model weights, tokenizer, prompt, output, or benchmark record. Its aggregate CSVs contain no HotpotQA question, answer, title, paragraph, sample identifier, candidate, selected-evidence, prediction, response, or per-example record.

| Component | Role in the evidence chain | Distributed in this package? | Official source or notice location | Required treatment |
|---|---|---|---|---|
| HotpotQA | Underlying benchmark for the aggregate supporting-fact evaluation. | No | `../../HOT_POTQA_DATASET_ATTRIBUTION.md` | Retain the dataset citation, source link, and original terms/attribution. |
| KG²RAG | Upstream candidate-construction context of the manuscript. | No | `../../HOT_POTQA_THIRD_PARTY_NOTICES.md` | Retain the method citation; no KG²RAG source code or output is distributed here. |
| FlagEmbedding/BGE | Scoring terminology appears in configuration labels and protocol documentation. | No | `../../HOT_POTQA_THIRD_PARTY_NOTICES.md` | Retain the applicable source notice; no BGE library, checkpoint, or weight is distributed. |

Before public release, authors must confirm that any reused statistical, formatting, or validation logic not authored for this package has the required notice. The confirmed path-scoped licences for author-owned material are recorded in `../../HOT_POTQA_LICENSE_SCOPE.md`; this notice does not grant third-party rights.
