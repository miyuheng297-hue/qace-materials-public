# HotpotQA Third-Party Notices

## Scope

This notice records third-party sources named by the scoped HotpotQA materials. It does not state that those components are distributed, and it does not replace their original terms or required notices.

| Component | Use in scoped material | Distributed here? | Official source | Citation or notice to retain |
|---|---|---|---|---|
| HotpotQA | Evaluation benchmark underlying sanitized aggregate supporting-fact material | No. The repository does not distribute raw questions, answers, titles, paragraphs, IDs, candidates, selected-evidence records, predictions, responses, or per-example records. | [Project page](https://hotpotqa.github.io/); [official repository](https://github.com/hotpotqa/hotpot); [ACL Anthology paper](https://aclanthology.org/D18-1259/) | Cite Yang *et al.* (EMNLP 2018) and retain appropriate reference to the official source terms, including [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). |
| KG²RAG | Upstream method context referenced by the materials | No KG²RAG source tree, graph asset, or candidate snapshot is distributed. | [Official NAACL 2025 record, ACL Anthology](https://aclanthology.org/2025.naacl-long.449/) | Retain the formal NAACL 2025 citation when KG²RAG is referenced. Verify the source and licence separately before adding upstream code or assets. |
| FlagEmbedding/BGE | Reranker family/model name in aggregate configuration material | No FlagEmbedding source code or BGE model weights are distributed. | [FlagEmbedding official repository](https://github.com/FlagOpen/FlagEmbedding) | Cite or acknowledge the verified FlagEmbedding/BGE source used. Do not assume a library licence governs model weights. |
| Meta Llama 3 | `llama3:8b` is mentioned only in historical root-level aggregate configuration/environment material. The current `releases/strict-sp-ablation-materials/` package is SP-only and does not generate answers. | No Llama model weights, tokenizer, prompt set, outputs, runtime, or Meta source code are distributed. | [Meta Llama 3 official repository](https://github.com/meta-llama/llama3); [official licence location](https://github.com/meta-llama/llama3/blob/main/LICENSE) | Confirm actual model provenance and applicable terms before making model-specific distribution or notice claims. This repository must not state that it redistributes Llama material. |

## Non-distributed components

LlamaIndex, Ollama, and mixedbread mxbai are not represented as distributed dependencies. They are not included in this notice as distributed components. No statement of their actual use is made here.
