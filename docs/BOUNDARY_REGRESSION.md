# APP boundary regression set

Eight specified-leaf regression cases have been source-adjudicated. [Reference and evidence](boundary-reference.json) is maintainer-only; the evaluated Agent receives one generated source repository and SCORE_RULES.md, never this wrapper or reference. All eight share one family. This is public development/regression material, separate from Validation-18 and pending 22, not an independent holdout.

| Cases | APP leaf | Reference scores |
|---|---|---|
| channel-a/b/c/d/e | platform_reuse.release_branch_strategy | 0 / 3 / 8 / 10 / 10 |
| device-a/b/c | platform_reuse.platform_upgrade | 3 / 8 / 10 |

The adjudicator read source/refs before candidate mappings; this was not blind to the task context. Main review checked the decisive source behavior and a fresh generation reproduced all 8 HEADs, refs and 94 file hashes. There are seven observed leaf-by-band groups. Full production-scale APP suitability is not claimed for these tiny fixtures.

The in-sample modal-score baseline by leaf is 3/8 (37.5%). This is a distribution diagnostic, not a measured Prompt result or independent accuracy. Canonical 18 remains at 130/171 (76.0%); report these separately.

Generate outside the wrapper (Python, Git, JDK 17, Android SDK platforms 31 and 35):

```sh
python verification/examples/build_boundary_prototypes.py --sdk /path/to/Android/Sdk --output /path/to/new-boundary
python verification/boundary.py --sources /path/to/new-boundary/sources
python verification/boundary.py --sources /path/to/new-boundary/sources --predictions /path/to/predictions.json
```

Predictions are a JSON array of objects with `case` and `score` (0, 3, 8, 10 or null). Missing/null answers abstain and retain the fixed denominator of eight. Results include each leaf/band, confusion counts, output coverage and macro recall over the seven observed leaf-by-band groups. Do not merge this accuracy with canonical 171-leaf accuracy. A synthetic all-correct test validates the metric only; it is not Agent performance.

Fresh generation compiled 15 heads against two SDKs (30 javac runs), built production JARs and passed 106 JVM behavior checks. No APK or device/emulator execution was performed. Host reflection checks exercise absent-class fallback, not Android hidden-API enforcement or all success/null/empty paths. Configuration platform names do not prove physical chipset portability.

channel-e has a shared tagged artifact but no tag/main tree difference. New rule inputs use release_policy_evidence_verified; the legacy ref_tree_differences_verify_release_policy key remains accepted for frozen canonical records. device-a contains a catch fallback but lacks adapter isolation. Those metadata repairs do not change the eight adjudicated scores.

The reference hashes, source/refs/configuration checks and score comparison are deterministic. Evidence correctness, repeated-run variance and cost still need actual Agent runs and human evidence adjudication; this tool does not invent those results.
