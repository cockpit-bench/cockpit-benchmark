# v0.8.5 discrimination and evidence fixes

The canonical 18 sources, refs, contract v3.4.1 and all 171 leaf objects remain unchanged: 277/828, 42/81 observed bands and a 130/171 in-sample modal baseline. This release adds a separate eight-case source-adjudicated boundary regression, an explicit evidence-availability protocol and two verifier fixes.

The C++ counter now handles numeric separators and raw string delimiters, including C++ header language labels. All frozen production paths were recounted. Six files had comment-only lines overcounted: APP-01 253080 → 253031 (−49); FW-14 231183 → 231159 (−24). Both remain large. No source selection, code, refs or quality labels changed. The three reported lexical fixtures also passed g++ 13.3.0 -std=c++14 -fsyntax-only. This is a focused lexer repair, not a full C++ preprocessor.

Integration 2/3 claims now require a HEAD-bound report, command, runtime/environment, objectives/outcomes, passed/failed/skipped counts, complete/covered interaction edge lists and recomputed ratios. Report/artifact bytes must match package hashes; remote CI also binds provider, run, job and actual workflow Git blob/SHA. The existing contract permits real JUnit/Robolectric/native component tests: host_jvm/host_native are distinguished from device/emulator execution, and device fields are conditional. Synthetic verifier test reports are not actual integration executions. All nine FW leaves remain 1.

APP-02 CI remains 2 in the historical canonical reference. Its time-bound HTTP/OCI summaries are incomplete raw inputs and are excluded from source-only/frozen-raw comparisons. Live observations require a new common capture batch and separate reference. Neither a prompt-specific Debian hint nor the maintainer facts/oracle is provided to candidates. See EVIDENCE_PROTOCOL.md and EVIDENCE_AVAILABILITY.md.

FW-03 API 3 and FW-18 LSP 0 are retained. The user chose to leave API full-coverage scope and any revised 2-point definition for a future contract version. No new API denominator is silently imposed.

No complete 18-repository Android build or device integration run is claimed. Restore executable behavior and source refs are unchanged, so prior v0.8.1 main/submodule restoration evidence remains the applicable 18/25 record. Pending 22 and MATLAB are outside this change.
