# Environment

Candidate inspection and final-asset verification require:

- Python 3.10 or newer;
- Pillow 12.1.1 or newer for the scale-normalized DOCX/PDF pixel comparison;
- GNU-compatible `sha256sum` for manifest verification.

No dataset, model, model service, network connection, GPU, NumPy, SciPy, plotting package, or credential is required to inspect this candidate. No final-figure regeneration is offered because the retained final figures are DOCX-extracted submission-equivalent PNGs and no same-version editable source was found.

Historical configuration identifiers are documented only at aggregate scope:

- answer generator family: `llama3:8b`;
- reranker family: `BAAI/bge-reranker-large`;
- deterministic generation settings: temperature 0, seed 20260730, top-k 1, top-p 1;
- HotpotQA generation limit: 64 tokens;
- corrected MuSiQue generation limit: 128 tokens;
- context limit: 3900 tokens.

These identifiers do not make the package an end-to-end execution environment.
