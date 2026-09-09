# MATLAB / Simulink

Nine original control-model repositories, 13 leaves / 61 points each:
**117 leaves, 338 / 549**. [Scores](SCORECARD.md), [CSV](SCORECARD.csv),
[manifest](manifest.json), [standard answers](STANDARD_SCORES.json),
[leaf evidence](oracle/), [readiness](VALIDATION_STATUS.json).

Candidate scoring uses the composed [current effective contract](EFFECTIVE_CONTRACT.md).
Its [input/output binding](effective-contract-binding.json) is reproducible with
`python verification/effective_contract.py --suite suites/matlab-simulink --check`
from the wrapper root. [SCORING_OVERRIDES.md](SCORING_OVERRIDES.md) and the unchanged
[original contract](SCORING_CONTRACT.md) remain historical source clauses. The six excluded non-LLM dimensions are
not part of this suite. Android scores are independent and must not be added.

## Evidence and validation

Local finalization verified nine complete source snapshots and repeated facts,
117 independently recomputed leaves with zero differences, and 12 native
configurations / 26,493 samples. Host generated-C replay is distinct from
MATLAB MIL, Simulink SIL/PIL/HIL, ECU compilation or vehicle validation.
Existing same-HEAD MATLAB runs and restored SLX execution were revalidated by
binding; this integration does not claim new MATLAB execution.

The [evidence index](EVIDENCE_INDEX.json) freezes the
[release attachment](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.9.0/matlab-verification-data-v0.9.0.zip).
The attachment retains original JSON and measured binary traces in a
content-addressed layout. Original paths inside historical JSON are lookup keys;
the verifier never reads those paths from the current host. It does not contain
full source repositories, Git objects, MATLAB, compiler or native executables.
Omitted artifacts are explicitly marked as hash-only provenance, not byte-verified
by the portable replay. The 9 source repositories are restored separately.

The portable verifier checks 117 scores, all 12 native vector/result bindings,
and recomputes numerical errors and 1,351,118 property assertions from retained
MIL/native output streams for 11 configurations (25,878 native samples).
ML-01 retained measured case summaries and vectors but no native stdout; its
615 native samples are checked at the recorded-case level. Passing metadata
cannot establish independent semantic truth or reproduce missing execution.

```sh
python verification/matlab_evidence.py --wrapper . --archive matlab-verification-data-v0.9.0.zip --sources C:/bench/matlab
```

Run from the wrapper root. `--sources` additionally resolves source-line anchors
and the executed model bytes against restored Git refs. It never runs model
callbacks, build scripts or executables. The index does not authorize candidate
access to standard answers or maintainer facts.

## Sources and limits

[PUBLIC_RESTORE.json](PUBLIC_RESTORE.json) records a fresh anonymous full-history
restore of all nine public source repositories, including exact HEAD/tree,
all heads/tags and file inventory checks. Restored repositories are clean and
remote-free; this is source restoration, not execution validation.

[Dataset limitations](DATASET_LIMITS.md): 34 / 52 tier cells, in-sample modal count
65 / 117, one common generation family. These are not prediction accuracies.
All samples remain Dev/Regression; keep the source family in one evaluation
split. Independent agent review does not imply external gold or human expert
certification. Source repositories contain no standard answers.

Maintenance in wrapper v0.9.2 adds ML-09 source anchors for the numerical comparison and mismatch failure in run_tests.m. Scores and the original v0.9.0 measured evidence attachment are unchanged.
