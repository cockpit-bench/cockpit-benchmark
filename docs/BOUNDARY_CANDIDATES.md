# Reproducible boundary candidates

These eight small repositories are generated locally by the [public generator](../verification/examples/build_boundary_prototypes.py). Their recorded refs, artifact hashes and behavior checks are in [boundary-candidates.json](boundary-candidates.json). They are candidates, not independently adjudicated gold or members of Validation-18/pending 22.

| Case | Target leaf | Rule mapping | Checked heads |
|---|---|---:|---:|
| channel-a | platform_reuse.release_branch_strategy | 0 | 1 |
| channel-b | platform_reuse.release_branch_strategy | 3 | 5 |
| channel-c | platform_reuse.release_branch_strategy | 8 | 3 |
| channel-d | platform_reuse.release_branch_strategy | 10 | 2 |
| channel-e | platform_reuse.release_branch_strategy | 10 | 1 |
| device-a | platform_reuse.platform_upgrade | 3 | 1 |
| device-b | platform_reuse.platform_upgrade | 8 | 1 |
| device-c | platform_reuse.platform_upgrade | 10 | 1 |

This run compiled 15 actual heads against Android SDK 31 and 35 (30 javac compilations), built a production-only JAR for each head, and passed 106 JVM behavior checks using those JARs and their packaged fleet assets. No APK build or Android device execution is claimed.

`channel-e` has only main and an annotated v1.0.0 tag. The tagged source builds one JAR whose fleet profile serves a1/a2 on 8155 and b1/b2 on 8295; the same artifact passes all four acceptance checks plus rejection checks. `channel-a` has no declared release policy/tag. `channel-b` has vehicle-specific release channels, `channel-c` shares a channel per platform, and `channel-d` uses a shared release branch. The three device variants put the same risk directly in business code, behind an interface with fallback, or behind an interface using public Build.MODEL.

All eight share `cabin-manual-shared-origin-1` and must remain in one evaluation split. They do not fill the canonical 42/81 coverage table. Source generation uses fixed Git dates; artifact bytes also depend on the recorded JDK/toolchain.

Prerequisites: Python, Git, JDK 17 and Android SDK platforms 31 and 35. Run outside the wrapper and give the generator a new output directory:

```sh
python verification/examples/build_boundary_prototypes.py --sdk /path/to/Android/Sdk --output /path/to/new-boundary-candidates
```

The generator creates real local Git histories and tags and compiles/runs only the included example code. Gradle/APK dependencies are not downloaded by this check. Maintainer observations and scores are written outside the generated source repositories.
