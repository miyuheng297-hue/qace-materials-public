# Execution Integrity Caveat

## v10.6 Table 1 Note (Verbatim)

"Results are from the corrected two-round formal evaluation on 7,405 HotpotQA distractor-dev instances. The corrected JSON-structured protocol was post-hoc and not preregistered; final response JSONL files are complete, and four unsaved non-string initial attempts remain an execution-integrity caveat. G is a frozen selected-evidence trace replay with exact parity to the frozen trace used by the corrected formal protocol, not a fresh online execution."

## Formal Audit Statement (Verbatim)

"Launcher logs contain 4 unrecorded non-string answer runtime failures, so strict clean-run validity is NO even though final records are complete."

## Retention Boundary

Both statements are retained because they describe distinct but consistent boundaries: the manuscript states the four unsaved non-string initial attempts and the formal audit states that strict clean-run validity is NO. The final records being complete does not remove either caveat. This package contains neither the logs nor any failed response, identifier, sample, or benchmark content.
