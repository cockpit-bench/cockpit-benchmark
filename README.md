# Benchmark — APP, FW and New Energy MATLAB

[suites.json](suites.json) is the current registry. APP and FW are independent repository types; New Energy MATLAB identifies the business domain. MATLAB/Simulink is technology metadata, not a generic business type. Future MATLAB repositories from other centers require their own business classification.

| Repository type | Published repositories / leaves | Score | Published sources |
|---|---:|---:|---:|
| [APP](suites/app/SCORECARD.md) | 11 / 88 | 141 / 440 | 11 |
| [FW](suites/fw/SCORECARD.md) | 11 / 121 | 194 / 572 | 11 |
| [New Energy MATLAB](suites/new-energy-matlab/SCORECARD.md) | 11 / 143 | 429 / 671 | 11 |

Version **v0.10.1** fixes scoped semantic evidence and adds current three-type evaluation over the 33 sources published in v0.10.0. APP-21 decoupling changes from 2 to 3; all other 351 scores remain. All 33 source HEADs/refs and existing 27 complete reference objects remain frozen. The old 22 pending slots are untouched. Scores remain separate; there is no combined raw score. See the [scoped decisions and limits](docs/REVIEW_V0101.md).

See [the six business profiles, evidence and limits](docs/EXPANSION_20260909.md). The approved contracts are unchanged: [APP/FW v3.5.1](SCORE_RULES.md) and [the independent MATLAB effective contract](suites/matlab-simulink/EFFECTIVE_CONTRACT.md). New scores are observed outcomes, not construction targets. This is a development/regression collection, not an independent holdout or measured model accuracy.

## Restore published sources

Python 3.11+, Git and PowerShell are required. Public restoration needs no GitHub credentials or local source map. An optional source map substitutes existing local source directories; unpublished inputs without a map are rejected before cloning or network access. All commands verify full history, exact HEAD/tree/refs, clean state and zero remotes. They do not run source code.

```powershell
# All three types from the public repositories.
./restore.ps1 -Suite all -Destination C:/bench/restored
# Select only the two new APP repositories, without restoring FW or MATLAB.
./restore.ps1 -Suite app -RepositoryIds APP-21,APP-22 -Destination C:/bench/new-app
```

`all` is the default and creates `app`, `fw`, and `new-energy-matlab` folders. A single-type request places repositories directly in its destination. `-Resume` rechecks existing inputs; `-IncludeSubmodules` checks out pinned recursive gitlinks and removes child remotes. Restore never turns a local source into a published one.

## Verify current additions

```sh
python verification/repository_types.py validate --wrapper . --require-publishable
python verification/expansion.py --wrapper . --source-map C:/bench/source-map.json --records-root C:/bench/native-records --output C:/bench/expansion-replay.json
```

The second command checks source inventories twice, code/model anchors, all 64 new leaf calculations, and retained native artifact hashes. Semantic judgments are explicit reviewed inputs; deterministic replay is not a fresh blind semantic review. Omitting `--records-root` verifies sources and rules only. `--require-publishable` validates all 33 published source entries. The source map used for evidence replay maps the six IDs to your restored directories; it contains paths only. The small [native-record attachment](docs/EXPANSION_20260909.md#published-native-records) supplies the optional records root without adding binaries to the wrapper.

Give an evaluation agent only one selected source repository and explicitly allowed raw inputs. Never provide these manifests, standards or evidence judgments as candidate inputs. Use the [current three-type fixed evaluation](docs/CURRENT_EVALUATION.md): source-only eligible APP 81/88, FW 111/121, New Energy MATLAB 134/143; frozen raw inputs give 81/88, 113/121 and 143/143. The preserved [fixed Android evaluation batch](docs/EVALUATION_BATCH.md) remains the original 171-leaf Validation-18 compatibility entry.

## Preserved release compatibility

The root `manifest.json`, `STANDARD_SCORES.json`, `SCORECARD.*`, original Android verification attachment and `suites/matlab-simulink` remain the frozen legacy evidence payloads. [legacy-v094.json](suites/legacy-v094.json) binds them. They are not the primary current type registry.

Historical selector aliases `android-validation18` (APP plus FW) and `matlab-simulink` (New Energy MATLAB) remain accepted for compatibility; on this mainline they select the corresponding **current** type populations. Use the immutable [v0.9.4 release](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.4) for the exact original 18/9 restoration and its original behavior. Old refs and tags are not moved.
