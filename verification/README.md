# Public verification

Python 3.11+ and Git are required. This tool reads frozen Git blobs and does not run source build scripts.

1. Restore the source repositories outside the wrapper using `restore.ps1`.
2. Download the verification data archive linked in `../docs/VERIFICATION_INPUTS.md`, check its SHA-256, and extract it outside the wrapper and source repositories.
3. Run from this wrapper:

```sh
python verification/verify.py --wrapper . --data /path/to/verification-data --sources /path/to/source-cases --output /path/to/new-replay
python verification/coverage.py --wrapper . --data /path/to/verification-data --output /path/to/coverage
```

The output directory for replay must be new and outside all three input directories. Windows absolute paths are accepted. No Python packages are needed. On Windows, run against the unmodified Git checkout; the wrapper preserves exact file bytes through `.gitattributes`.

The data archive contains all tracked included/excluded paths, reviewed production owners, per-file blob/SHA/count records, generated-region exclusions, build anchors, actual rule inputs and semantic adjudications. It contains no source repository payloads. Expected scores and quality roles are not passed to the mapping functions.

The verifier checks exact source HEADs and heads/tags, main worktree cleanliness, complete tracked-entry partition, source and build-anchor hashes, line/symbol coordinates, per-file counts, size bands, and all 171 rule predictions. It compares predictions with the published scores after computing them. Submodule working state is reported by restore, and does not alter owned-source counts.

Reviewed ownership and semantic observations are **inputs**, not conclusions inferred anew by this tool. A valid hash or existing symbol does not establish the truth, completeness or semantic relevance of an observation. Reviewers can inspect and challenge the disclosed choices. A source ownership label without an original per-path adjudication is explicitly identified as a frozen selection, not an automatically proven build closure.

This is reproducible counting and rule mapping. It is not a new independent semantic review, Android build, device test or proof of complete dependency closure. No current build execution is implied by a previously published score.

For test-dependent LSP promotion, the verifier also checks a hashed execution report against the evaluated revision, contract and covered production implementations. See [the execution input schema](../docs/RULE_FIXES.md).
