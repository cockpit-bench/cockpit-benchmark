# Cockpit Benchmark v0.8.0

Public Dev/Regression benchmark with 18 independently browsable source repositories. It is not a lineage-isolated final holdout. Source provenance is recorded in manifest.json.

Scores bind the exact HEADs and full heads/tags in manifest.json. Production LOC excludes tests, resources, build tooling, generated code and vendored dependencies; file counts are descriptive.

See [SCORECARD.md](SCORECARD.md), [SCORE_RULES.md](SCORE_RULES.md), and [manifest.md](manifest.md). Full score facts are under facts/ and canonical answers under oracle/. Give an evaluator one source repository only.

Restore with PowerShell: `./restore.ps1 -Destination C:/bench/source-cases`. The destination must be empty and outside this wrapper. The script verifies frozen hashes, 18 exact HEADs and all heads/tags, and removes remotes. 22 pending entries are never cloned.

Publication and anonymous restore results are recorded in the release notes. Full Android platform builds and integration execution must be read per leaf; a targeted JVM check is not Android integration coverage.

For web review: [review instructions and current decisions](docs/WEB_REVIEW.md) · [original real-repository guidance](docs/REAL_REPOSITORY_GUIDANCE.md). These documents were added after v0.8.0 on main; the v0.8.0 tag remains unchanged.
