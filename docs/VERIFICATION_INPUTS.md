# v0.8.4 verification inputs

Download [validation18-verification-data-v0.8.4.zip](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.8.4/validation18-verification-data-v0.8.4.zip) (4880863 bytes).

SHA-256: `949a30c30101d0d2da60cffb4af8e3ba1300948aaf406a536efac2b4aac5f2b6`

Extract outside wrapper and source repositories; follow [the verifier](../verification/README.md). Use the matching v0.8.4 tools: the archive binds all five public helper hashes. It contains complete reviewed path partitions, counts, source/ownership anchors, corrected rule observations and SOLID adjudications; no source repositories or dependencies.

Source HEADs and contract v3.4.1 are unchanged. The dated APP-02 external CI observation changes CI 3 to 2; all other scores are unchanged. Reproduction yields 171 leaves and 277/828. See [the corrections](REVIEW_FIXES.md). Replay checks the disclosed observations and bindings; it performs neither a new semantic review nor Android execution.

The archive contents and SHA-256 are byte-identical to v0.8.3 and retain review_revision v0.8.3. v0.8.4 corrects wrapper CSV serialization only; use the current wrapper, whose strict consistency check passes.
