# Cockpit Benchmark v0.8.4

Public Dev/Regression benchmark with 18 independently browsable source repositories. It is not a lineage-isolated final holdout. Source provenance and exact HEADs/heads/tags are recorded in [manifest.json](manifest.json).

See [SCORECARD.md](SCORECARD.md), [SCORE_RULES.md](SCORE_RULES.md), and [manifest.md](manifest.md). Facts are under facts/ and canonical answers under oracle/. Give an evaluator one source repository only.

This release preserves all 18 v0.8.0 source HEADs. A complete 171-leaf review corrected 22 evidence/fact records; APP-02 CI changes from 3 to 2, giving 277/828. Contract v3.4.1 clarifies production scanning paths without changing score bands. Production LOC excludes tests, resources, build tooling, generated code and vendored dependencies; file counts are descriptive.

Restore with PowerShell: `./restore.ps1 -Destination C:/bench/source-cases`. The destination must be empty and outside this wrapper. Use `-Resume` to revalidate an existing restoration. Add `-IncludeSubmodules` to fetch recursively pinned HTTPS gitlinks; new dependency clones use shallow history while still checking out the exact gitlink commit, never branch latest. Main source repositories retain full history. Main source remotes are removed; `-IncludeSubmodules` also removes submodule remotes after successful pinned restoration. 22 pending entries are never cloned.

`restore-state.json` separately reports main source-review readiness and pinned submodule readiness. Neither implies complete SDK/Maven/platform dependencies or a successful build. Full Android builds and integration execution must be read per leaf; targeted host checks are not Android integration coverage.

Maintainer review: [coverage and modal baseline](docs/COVERAGE.md) · [downloadable reproduction inputs](docs/VERIFICATION_INPUTS.md) · [runnable verifier](verification/README.md) · [accepted execution specification](docs/EXECUTION_SPEC.md) · [web review instructions](docs/WEB_REVIEW.md) · [original guidance archive](docs/REAL_REPOSITORY_GUIDANCE.md).

Public replay validates counts, hashes, evidence coordinates and rule mappings from disclosed reviewed inputs. It does not independently establish the completeness or truth of semantic judgments. Old tags, including v0.8.0, remain unchanged.

Rule corrections: [release/LSP boundaries and execution inputs](docs/RULE_FIXES.md). [Reproducible small candidates](docs/BOUNDARY_CANDIDATES.md) remain separate from Validation-18.

Evidence corrections: [complete leaf review repairs](docs/REVIEW_FIXES.md). The 18 sources have 17 recorded families; APP-14 and FW-16 share the same SystemUI production files. Validate grouping with `verification/check_split.py`.

v0.8.4 preserves quoted multiline CSV reasons exactly. v0.8.3 is superseded because a final global line-ending conversion made one CSV reason differ from its canonical text; scores and source evidence did not change.
