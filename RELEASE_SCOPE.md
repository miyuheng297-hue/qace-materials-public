# Release Scope

This candidate is an aggregate-results, v10.6 final-figure, and audit-materials package. It is not an end-to-end rerun package.

Included:

- aggregate HotpotQA Table 1 metrics for B, D, and the frozen G trace replay;
- aggregate MuSiQue Table 2 metrics for the two separately recorded rounds;
- aggregate MuSiQue inferential summaries already reported by the accepted analysis;
- configuration definitions that contain no machine paths or secrets;
- exact PNG copies of the three final figures actually embedded in the v10.6 DOCX, with DOCX/PDF correspondence metadata;
- Figure 2/3 aggregate CSV sources that match the v10.6 displayed values;
- validation scripts. No figure-generation script is included because no same-version v10.6 script was found locally;
- reproducibility, sanitization, and rights-review documentation.

Excluded:

- benchmark questions, answers, aliases, titles, paragraphs, supporting facts, and gold annotations;
- sample identifiers, per-sample scores, selected evidence, predictions, model responses, raw HTTP, and logs;
- datasets, candidate snapshots, knowledge-graph assets, model weights, caches, credentials, hosts, endpoints, and server paths;
- historical QACE v3, top-k, holdout, and failed or diagnostic result artifacts;
- manuscript source files and unpublished author information;
- any non-v10.6 figure redraw or approximate replacement;
- prior SVG figures and their generator, because they do not reproduce the v10.6 submission layout.

The released aggregates support inspection of the reported tables and figures. They do not permit reconstruction of benchmark records, replay of historical model calls, or independent recomputation of paired tests without separately authorized private inputs.

## Execution-Integrity Boundary Retained From v10.6

The following Table 1 note is retained verbatim from the v10.6 manuscript: "Results are from the corrected two-round formal evaluation on 7,405 HotpotQA distractor-dev instances. The corrected JSON-structured protocol was post-hoc and not preregistered; final response JSONL files are complete, and four unsaved non-string initial attempts remain an execution-integrity caveat. G is a frozen selected-evidence trace replay with exact parity to the frozen trace used by the corrected formal protocol, not a fresh online execution."

`audit/EXECUTION_INTEGRITY_CAVEAT.md` retains the corresponding formal-audit statement. These qualifications are not relaxed by the final-figure repair.
