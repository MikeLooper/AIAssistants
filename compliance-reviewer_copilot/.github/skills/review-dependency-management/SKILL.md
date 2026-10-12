---
name: review-dependency-management
description: 'Reviews dependency version pinning, lock files, known vulnerabilities, end-of-life versions, licenses and SBOM presence. Use when the compliance-reviewer orchestrator delegates the Implementation / Dependency Management subject.'
user-invocable: false
---

# Review: Dependency Management

Assesses how third-party dependencies are declared, pinned, scanned for vulnerabilities, and tracked for licensing/SBOM purposes.

## Inputs

Dependency manifests, lock files, and `02-analyzers.json` (if present), per `compliance-inventory`.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check dependencies are version-pinned (exact or narrow ranges) and a lock file exists where the ecosystem supports one.
3. If `02-analyzers.json` has vulnerability scan results, turn each reported vulnerability into a finding with the reported severity mapped via the fallback rubric (data loss/exploit risk → Error).
4. Flag dependencies on end-of-life runtime/framework versions (e.g. .NET/Java/Python versions past their support window) using the file's declared target version.
5. Check for a license inventory or SBOM (`sbom.json`, `*.cdx.json`, `*.spdx.json`) and flag its absence as Information (not a hard requirement).

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
