# v0.8.2 rule corrections

Contract v3.4.1, all 18 source revisions and score bands are unchanged. These corrections align mappings with the existing contract; v0.8.1 remains immutable.

## Release strategy

`main`, `master` and `trunk` have no score shortcut. The existing field `ref_tree_differences_verify_release_policy` describes verified policy evidence: it can include same-version fleet configurations, qualified artifacts and tags on a single trunk, not just differences between branches. An explicit false value means reviewed absence; missing/null is unresolved and raises `Missing`. Positive facts are classified from the finest actual channel: vehicle (3), platform (8), unified across platforms (10). Merely adding a development branch cannot change the result.

FW-07 previously supplied only refs to the shortcut. Its complete 17 tags all peel to upstream `82d2b854425b2e8731f4902bbba175c653b54d60`; its current HEAD changes Wi-Fi connection scorers/tests and provenance, not release policy. The generic WiFi APEX is not, by itself, a qualified same-version multi-vehicle release. The reviewed absent-policy observations now have source/build/provenance anchors. This conclusion concerns the frozen repository, not an assertion that the upstream organization has no release process.

## LSP execution proof

Test declarations/counts cannot promote a score. Without recorded passing execution the previously reviewed implementation facts still support their own baseline: one conforming implementation can score 2; two conforming implementations can score 3 without executing tests. Existing violation/contract gates still apply first.

The test-dependent path requires `evaluation_revision` and a `substitution_execution` object. A positive record contains:

- `status: "passed"`, the same `revision` and `parent_symbol` as the evaluated source;
- the executed `command`, positive `tests_passed`, and `tests_failed: 0`;
- `tested_implementations` and `passed_implementations`, naming reviewed production child symbols;
- `coverage` booleans for exception, boundary, precondition and postcondition;
- `report_path` and `report_sha256` referencing a JSON execution artifact in the verification data pack's `files_sha256` map.

The JSON artifact must contain the same revision, parent, command, status, counts, implementations and coverage. `verify.py` checks its digest and binding against the actual source HEAD. One passed production implementation enables the test path to 3. A 4 requires at least two production implementations, all of them passed, and all four systematic coverage facts. A test count or an old coverage boolean is insufficient.

Missing proof and `not_run`/`failed` do not enable a test upgrade. A contradictory or stale positive record fails verification. A failed test is not automatically labelled an LSP violation: semantic failure analysis still belongs to reviewed observations. The verifier does not re-execute the command or prove the authenticity of a supplied execution report; maintainers must retain actual runner evidence. Current Validation-18 uses no test-dependent LSP promotion added by this release.

## Coverage and regressions

Coverage prose derives recorded/absent/unclassified counts from the current observations. Regression tests include mixed execution states, trunk-name invariance, unknown policy evidence, declaration-only tests, stale revisions and report tampering.

Run `python verification/test_rule_boundaries.py`. Its constructed execution records test mapping and validation boundaries; they are not production execution claims or canonical examples. For actual compiled behavioral candidates, see [BOUNDARY_CANDIDATES.md](BOUNDARY_CANDIDATES.md).
