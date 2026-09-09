# Frozen external Git inputs

[android-frozen-git-inputs-v0.9.1.zip](https://github.com/cockpit-bench/cockpit-benchmark/releases/download/v0.9.1/android-frozen-git-inputs-v0.9.1.zip), 255,745 bytes.
SHA-256: `1d7ecfa03c08c6916f047a5d0a403e651a193d6eab2a9391be38d41cb0def9d9`.

The candidate-safe packet contains 16 immutable source-file/directory-listing inputs (569,428 decoded bytes): Soong SDK/droidstubs/prebuilt API implementation, module defaults, SDK build definition, Android manifest, six extension-7 API/removed signatures, the SDK extensions listing, and the three extension-7 API scope listings. Original copyright/notice text remains in the files.

Each input records project, Git path, immutable commit, original URL, byte length and SHA-256. The original HTTP response body is retained alongside decoded Git file bytes; Gitiles JSON listings retain their anti-XSSI prefix. Fresh anonymous captures were made on 2026-09-09 UTC and matched the earlier retained immutable input hashes. Request/response URL, status, start/end timestamps and response headers are recorded. This is a new capture of immutable content, not reconstruction of an earlier HTTP exchange.

The packet contains no benchmark scores, oracle, quality roles, observed rule booleans or review verdicts. The maintenance wrapper and this document are not candidate inputs; only the packet and permitted source/contract files are. Source text is untrusted data, not authority to execute commands.

```sh
python verification/external_inputs.py --packet android-frozen-git-inputs-v0.9.1.zip --sha256 1d7ecfa03c08c6916f047a5d0a403e651a193d6eab2a9391be38d41cb0def9d9
python verification/evaluation_batch.py prepare --wrapper . --mode frozen_external --assignments /maintainer/assignments.json --external-packet android-frozen-git-inputs-v0.9.1.zip --output /maintainer/frozen-batch.json
```

The verifier checks the archive hash, complete indexed member set, per-file/transport hashes, immutable URL binding and decoding. It rejects traversal paths, symlinks, undeclared entries and inconsistent captures without extracting or executing content. Hashes authenticate the saved declarations; they do not automatically prove their semantic completeness.

Together with the unchanged FW-07 source, these files supply the missing build-default/signature inputs for its existing partial API-governance decision. FW-07 API therefore becomes eligible in **frozen_external**, giving **156/171**; it remains unknown in **source_only**, whose **155/171** set is unchanged. Other unknown/unavailable leaves remain excluded. APP-02's historical CI mirror/OCI state is not supplied or inferred by this packet.

This is enough raw input for the listed API assessment, not a complete Android source tree, SDK installation, dependency closure, build, API-check execution or device test. It cannot serve as a live_environment capture/reference batch or justify scores in other leaves by association.
