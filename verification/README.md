Current v0.9.1: fixed candidate evaluation uses docs/EVALUATION_BATCH.md; Android canonical is 269/828 after the scoped SOLID corrections in docs/SOLID_CALIBRATION.md. Replay uses the matching v0.9.1 data attachment in docs/VERIFICATION_INPUTS.md. MATLAB remains the independent v0.9.0 evidence/score snapshot. Earlier commands below describe historical attachment versions.

Current v0.8.6: API scope B under SCORE_RULES.md v3.5 supersedes earlier API-scope statements below; see [API governance schema and limits](../docs/API_GOVERNANCE.md). Other leaf contracts remain unchanged.

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

## v0.8.3 consistency and family checks

The same replay also compares complete canonical leaf objects, facts and scorecards. It detects stale reasons/evidence even when scores agree.

Run the portable regressions with `python -m unittest discover -s verification -p "test_*.py" -v`.

Provide an explicit JSON object such as `{"APP-14":"development","FW-16":"development","APP-03":"validation"}` to `python verification/check_split.py --wrapper . --assignments /path/to/split.json`. Add `--require-complete` for all 18. Recorded same-family repositories cannot cross sets; this is not an independent holdout certificate.

v0.8.5 adds the separate eight-case boundary regression, evidence mode gating and execution/C++ checks. Read docs/DISCRIMINATION_FIXES.md, docs/BOUNDARY_REGRESSION.md and docs/EVIDENCE_PROTOCOL.md from the wrapper root. Portable tests include synthetic records only; no Android execution is implied.

Integration execution schema: [INTEGRATION_EXECUTION.md](../docs/INTEGRATION_EXECUTION.md). For source-binding regression tests, set BOUNDARY_SOURCE_ROOT to the generated examples source directory; otherwise these checks are explicitly skipped while metric tests still run.
