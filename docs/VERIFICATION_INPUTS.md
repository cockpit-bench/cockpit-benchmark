# v0.8.1 verification inputs

Download [validation18-verification-data-v0.8.1.zip](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.8.1/validation18-verification-data-v0.8.1.zip) (4988350 bytes).

SHA-256: `dc6a2f469812a515cffdcf7009bd5ed08207a8db53d6acb6ff3f4ebe6eb941c2`

The archive holds complete tracked-path partitions and reviewed observations for the unchanged 18 source HEADs. It contains no source code payloads, Git objects or dependencies. Extract it outside the wrapper and source cases. Follow [the runnable verification instructions](../verification/README.md).

Verify the downloaded archive before extraction, for example `Get-FileHash ./validation18-verification-data-v0.8.1.zip -Algorithm SHA256`. Internal entries and verifier source versions are hash-checked by `verify.py`.

v0.8.0's source and semantic review remain the baseline. v3.4.1 clarifies real production paths (including Soong/custom sourceSets), without changing leaves, bands, module-name rules or execution gates. v0.8.1 discloses reviewed path/semantic selections and replays their counts and rule mappings. This does not independently infer all ownership or semantic truth.

See [coverage](COVERAGE.md) for all 81 legal type/leaf/band cells, including empty cells and evidence-state counts. The 130/171 modal result is a post-hoc in-sample baseline, not cross-validation accuracy.
