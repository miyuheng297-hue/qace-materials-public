# MuSiQue Third-Party Notices

## Scope

This notice covers only third-party sources with direct evidence in the scoped MuSiQue configuration or aggregate material. It distinguishes use from distribution and does not treat an unverified component as a MuSiQue-specific dependency.

| Component | Evidence-supported role | Distributed in this repository? | Official source | Citation or notice |
|---|---|---|---|---|
| MuSiQue | Dataset underlying the paragraph-native fixed-pool aggregate validation. | No original dataset, question, paragraph, title, answer, identifier, candidate pool, selected-paragraph record, prediction, response, log, or per-example record is distributed. | [MuSiQue official repository](https://github.com/StonyBrookNLP/musique); [formal TACL 2022 record](https://aclanthology.org/2022.tacl-1.31/) | Cite Trivedi *et al.* (TACL 2022) and retain appropriate source-terms and attribution information. |
| FlagEmbedding/BGE | `config/musique_fixed_pool_config.json` names `BAAI/bge-reranker-large` as the reranker family. | No FlagEmbedding code, BGE model weight, or other model material is distributed. | [FlagEmbedding official repository](https://github.com/FlagOpen/FlagEmbedding) | Retain an appropriate citation/notice only after verifying the actual BGE model provenance. A library licence does not automatically govern model weights. |
| Meta Llama 3 | `config/musique_fixed_pool_config.json` identifies the answer-generator family as `llama3:8b`. | No Llama model, weight, tokenizer, prompt, output, runtime, or Meta source code is distributed. | [Meta Llama 3 official repository](https://github.com/meta-llama/llama3); [official licence location](https://github.com/meta-llama/llama3/blob/main/LICENSE) | Verify actual model provenance and applicable terms before making model-specific distribution or notice claims. |

No other component is represented here as a MuSiQue-specific dependency. In particular, this notice does not assert that HotpotQA, KG²RAG, LlamaIndex, Ollama, or mixedbread mxbai is distributed with, or uniquely used by, the scoped MuSiQue assets.
