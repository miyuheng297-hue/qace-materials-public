# Statistical Methods Boundary

HotpotQA values in this candidate are descriptive aggregate metrics only. No HotpotQA inferential claim is released because the direct inferential source required by the manuscript boundary is not included.

For MuSiQue, each generation round has an independent six-test family: two contrasts multiplied by Answer F1, Derived Joint, and Answer EM.

- Answer F1 and Derived Joint used 20,000 paired bootstrap resamples with seed 20260730.
- Answer EM used the exact two-sided McNemar binomial test.
- Holm adjustment was applied within each round only.
- The decision rule is Holm-adjusted p below 0.05; equality is not rejection.
- Derived Joint is the mean per-example product of Answer F1 and paragraph-support F1, not Official HotpotQA Joint.

`data/musique_inferential_summary.csv` contains only aggregate deltas, intervals, p-values, and decisions. Per-sample inputs are deliberately excluded, so the original bootstrap and McNemar tests cannot be independently recomputed from this public candidate.
