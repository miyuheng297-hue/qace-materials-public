# Benchmark Content Exclusion Audit

The next-release candidate was scanned before repository synchronization. It contains aggregate CSVs, configuration metadata, documentation, validators, and four standalone figure displays only.

Excluded from the package are benchmark questions, answers, aliases, titles, paragraphs, supporting facts, annotations, sample identifiers, candidate/selection records, predictions, responses, raw HTTP, logs, checkpoints, caches, model weights, private paths, IP addresses, credentials, and server endpoints. Public repository, DOI, licence, and dataset-attribution URLs are documentation and are not private endpoints.

The root and strict validators exclude `.git` metadata and exclude only the manifest currently being checked. The final scan results and file inventory are recorded in the release audit and manifests.
