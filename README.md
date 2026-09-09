# Cockpit Benchmark — independent suites

[suites.json](suites.json) is the unified index. Each suite has its own scoring
contract, source manifest, standard answers and reproducible evidence.

| Suite | Repositories / leaves | Score | Contract |
|---|---|---|---|
| [Android APP / Framework](SCORECARD.md) | 18 / 171 | 258 / 828 | [v3.5](SCORE_RULES.md) |
| [MATLAB / Simulink](suites/matlab-simulink/README.md) | 9 / 117 | 338 / 549 | [Effective contract](suites/matlab-simulink/EFFECTIVE_CONTRACT.md) |

Version v0.9.3 resolves [three horizontal SOLID severity boundaries](docs/HORIZONTAL_ARBITRATION_V093.md) and two wording/baseline defects. Three scores change; FW-15 LSP keeps its score with narrower wording. All 27 source HEADs/refs, contracts and MATLAB scores/evidence remain unchanged; expansion is separate.

## Restore

```powershell
./restore.ps1 -Destination C:/bench/android
./restore.ps1 -Suite matlab-simulink -Destination C:/bench/matlab
./restore.ps1 -Suite all -Destination C:/bench/all
```

The default remains Android. `all` restores to separate `android-validation18`
and `matlab-simulink` subdirectories. `-Resume` rechecks existing sources;
`-IncludeSubmodules` applies to Android. MATLAB has no declared submodules.
The additional suite dispatcher requires Python 3.11+ and Git; Android retains
its PowerShell/Git requirements. Restoration verifies frozen HEADs, all refs,
complete history and clean remote-free repositories. It does not execute models.

## Verify

```sh
python verification/suites.py validate --wrapper . --require-publishable
python verification/matlab_evidence.py --wrapper . --archive matlab-verification-data-v0.9.0.zip --sources C:/bench/matlab
```

The first command checks the published registry and complete evidence index;
it does not by itself replay the attachment. Download the MATLAB attachment
from [v0.9.0](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.0)
for the second command. Its hash is frozen in
[EVIDENCE_INDEX.json](suites/matlab-simulink/EVIDENCE_INDEX.json).

Android’s [verifier](verification/README.md), [API governance](docs/API_GOVERNANCE.md),
[evidence protocol](docs/EVIDENCE_PROTOCOL.md) and
[v0.9.3 evidence attachment](https://github.com/cockpit-bench/cockpit-benchmark/releases/tag/v0.9.3)
remain the reference for that suite. Give an evaluation agent only its selected
source repository and explicitly allowed raw inputs, never the wrapper answers.

For candidate evaluation use the [fixed batch entry](docs/EVALUATION_BATCH.md). Source-only and frozen-external are separate modes; score accuracy and sampled semantic evidence validity are separate metrics.

See [review follow-up scope and remaining work](docs/REVIEW_FOLLOWUP.md).
