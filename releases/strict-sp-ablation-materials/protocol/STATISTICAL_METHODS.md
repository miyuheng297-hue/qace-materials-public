# Statistical methods (portable summary)

For configuration `c`, the aggregate files report macro means over 7,405 items:

- SP precision = mean of selected supporting-fact precision;
- SP recall = mean of selected supporting-fact recall;
- SP F1 = mean of the item-level SP F1 values;
- average evidence count = mean number of selected evidence units.

For every predefined target/reference pair, the difference is target minus reference on the same item ordering. The confidence interval is the 2.5th and 97.5th percentile of 20,000 paired bootstrap means. The two-sided p-value is the deterministic paired-bootstrap tail probability used by the finalized Stage 03. Holm adjustment is applied independently within the three declared families and across all four metrics.

The public CSVs are aggregate-only. No raw item vectors, item identifiers, gold records, selected evidence, predictions, responses, or intermediate bootstrap draws are included.
