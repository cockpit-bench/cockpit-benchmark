# MATLAB / Simulink — reviewed, not finalized

The independent contract contains 13 leaves / 61 points per repository: nine
repositories, 117 leaves / 549 points. The six non-LLM dimensions are excluded.
Read [SCORING_OVERRIDES.md](SCORING_OVERRIDES.md) before the unchanged
[original contract](SCORING_CONTRACT.md); user overrides have precedence.

[Current reviewed scores](review/STANDARD_SCORES.json) total 338 / 549. They are
**not canonical final scores**. The old 339-point suite is not an input here.
[Source manifest](manifest.json) records the current exact HEADs/trees/refs and
proposed public target names; those repositories are not yet published.

Eight of nine default repositories have complete repeated facts. Ten of twelve
default/VCU-B configurations have fresh native replay. ML-05 and ML-05-B lack
valid fresh execution. ML-05's executable returned WinError 5 and disappeared;
the exact reason is unconfirmed. No rename, ACL change, protection disabling or
repeated compilation is an approved workaround.

The coordinator must resolve that environmental cause, run both configurations
and resource checks, and pass the existing strict finalizer before exporting a
canonical suite. Current readiness is bound in [VALIDATION_STATUS.json](VALIDATION_STATUS.json).
This preparation's validator rejects the MATLAB published state unconditionally;
the final evidence export and its validation must be implemented before enabling it.
Local review snapshots retain original evidence paths for traceability; they
are not a portable public evidence pack or candidate input. Portable evidence
export and final public restoration remain required before release.

[Dataset limitations](review/DATASET_LIMITS.md): 34 / 52 tier cells, in-sample modal
count 65 / 117, a common generation family. These are not prediction accuracies.
Prior same-HEAD local restoration and MATLAB MIL do not replace the missing native
replays. Host generated-C replay is not SIL/PIL/HIL or real-vehicle validation.
