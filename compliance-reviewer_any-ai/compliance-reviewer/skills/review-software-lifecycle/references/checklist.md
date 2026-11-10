# Checklist — Software Lifecycle

Subject: Software Lifecycle

Elements are defined in `standards/` (SV in `semver.md`; SSDF in `nist-ssdf.md`; SLSA in `slsa.md`; OSC in
`openssf-scorecard.md`). Every element belongs to exactly one active check. SL-06 and SL-08 are retired: don't
evaluate them or write them to `checkResults`, and never reuse the IDs.

| id | Sub-subject | Check | Default severity | Elements | Source |
|----|-------------|-------|------------------|----------|--------|
| SL-01 | Continuous Integration | Every change is built by CI before merge, from a pipeline defined in the repository with a consistent, source-controlled build (whether tests run is judged by TST-06) | Error | SSDF-01, SSDF-02, SLSA-02, SLSA-09, OSC-06 | SSDF, SLSA, OSC |
| SL-02 | Release Automation | Releases are automated on the hosted CI platform: versioned artifacts are published to a registry and retained per release, and production deployment runs as a separate, protected stage with staged exposure and a rollback path | Warning | SSDF-09, SSDF-13, SLSA-01, OSC-20, SDP-01 | SSDF, SLSA, OSC, SDP |
| SL-03 | Versioning | Versions follow Semantic Versioning 2.0.0 (ecosystem equivalents accepted): valid form, immutable releases, meaningful and correctly reset bumps, deprecation before removal | Warning | SV-01–SV-11 | SV |
| SL-04 | Branch Protection | Protected branches are enforced, as shown by settings-as-code or CODEOWNERS: no force-push or deletion, required reviews and status checks, code-owner review, immutable release tags (N/A when settings aren't visible) | Warning | SSDF-10, SSDF-11, SSDF-15, SLSA-10–SLSA-14, OSC-01–OSC-05 | SSDF, SLSA, OSC |
| SL-05 | Provenance & Signing | Releases carry verifiable provenance and integrity: platform-signed SLSA provenance distributed with the artifacts, signed artifacts or published hashes, reproducible-build settings | Information | SSDF-03, SSDF-12, SSDF-14, SLSA-03–SLSA-07, OSC-18, OSC-19 | SSDF, SLSA, OSC |
| SL-06 | — | *(retired 2026-11-09: dependency-update automation, owned by review-dependency-management DEP-07; ID not reused)* | — | — | — |
| SL-07 | Security Policy | A security policy (`SECURITY.md`) gives a private reporting channel, the handling process and disclosure expectations, and supported versions/advisories | Information | SSDF-17, SSDF-18, SSDF-19, OSC-15, OSC-16, OSC-17 | SSDF, OSC |
| SL-08 | — | *(retired 2026-11-09: change log / release notes, owned by review-maintainability MAINT-07; ID not reused)* | — | — | — |
| SL-09 | Workflow Security | CI workflows don't run untrusted pull-request code with privileged triggers, and don't interpolate untrusted context into scripts | Error | OSC-07, OSC-08 | OSC |
| SL-10 | Pipeline Hardening | Pipelines run with least-privilege tokens and pinned build dependencies: read-only default permissions, per-job write scopes, actions/tasks pinned to commit SHAs, images pinned by digest, no download-and-execute, current and verified toolchain | Warning | SSDF-05, SLSA-08, OSC-09–OSC-13 | SSDF, SLSA, OSC |
| SL-11 | Static Analysis | Static security analysis runs in CI on every change, with defined criteria enforced as gates, retained results, and compiler/build security warnings enabled | Warning | SSDF-04, SSDF-06, SSDF-07, SSDF-08, SSDF-16, OSC-14 | SSDF, OSC |
| SL-12 | Committed Binaries | No generated executable artifacts are present in the repository files | Information | OSC-21 | OSC |
