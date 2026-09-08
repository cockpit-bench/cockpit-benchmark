# Cockpit Benchmark — suite integration preparation

This local v0.9.0 preparation connects two independent suites. It is not a new
published benchmark release. [suites.json](suites.json) is the unified index;
the root manifest and canonical score files remain the Android compatibility entry.

| Suite | Current state | Repositories / leaves | Score |
|---|---|---|---|
| [Android APP / Framework](SCORECARD.md) | Published v0.8.6 | 18 / 171 | 271 / 828 |
| [MATLAB / Simulink](suites/matlab-simulink/README.md) | Reviewed; execution incomplete; unpublished | 9 / 117 | Reviewed 338 / 549; canonical pending |

Report each suite with its own contract, denominator and evidence mode. Do not add
raw suite totals or interpret the two scales as one health score. Android's 22
pending repositories remain excluded. Both datasets are Dev/Regression; their
source families must stay intact across evaluation splits.

## Restore

The existing command remains the default Android restoration:

```powershell
./restore.ps1 -Destination C:/bench/android
./restore.ps1 -Suite matlab-simulink -Destination C:/bench/matlab
./restore.ps1 -Suite all -Destination C:/bench/all
```

The MATLAB and all-suite commands currently **reject before creating directories
or downloading sources**, because MATLAB has not passed its final gate or been
published. They do not silently restore an older suite. `-Resume` and
`-IncludeSubmodules` retain the Android meanings; MATLAB has no declared submodules.
The additional suite dispatcher requires Python 3.11+ and Git. The default Android
path retains its existing PowerShell/Git requirements.

```sh
python verification/suites.py validate --wrapper .
python verification/suites.py validate --wrapper . --require-publishable
```

The first command validates the honest preparation state; the second currently
fails on MATLAB's unresolved execution/promotion requirements. Successful metadata
validation is not model execution or final suite validation.
This preparation deliberately disables the MATLAB published state. A complete
portable raw-evidence export protocol must be implemented and verified after the
existing finalizer passes; changing a status flag or summary cannot enable it.

Android reference documentation: [API governance](docs/API_GOVERNANCE.md),
[replay inputs](docs/VERIFICATION_INPUTS.md), [verifier](verification/README.md),
[evidence protocol](docs/EVIDENCE_PROTOCOL.md). Its source HEADs, refs, contract,
scores, production counts and evidence remain the v0.8.6 artifacts.
