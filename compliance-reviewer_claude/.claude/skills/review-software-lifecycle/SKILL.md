---
name: review-software-lifecycle
description: 'Reviews CI/CD, branching, versioning, release process, supply-chain practices (NIST SSDF / SLSA) and documentation. Use when the compliance-reviewer orchestrator delegates the Software Lifecycle subject.'
user-invocable: false
---

# Review: Software Lifecycle

Assesses the project's CI/CD pipeline, branching model, versioning scheme, release process, supply-chain security posture and lifecycle documentation.

## Inputs

`.github/workflows/*`, other CI/CD config, `CHANGELOG*`, version files, `SECURITY.md`, contribution/branching docs.

## Procedure

1. Load `references/checklist.md` and `references/sources.md`.
2. Check whether CI runs build + tests on every change, and whether a release pipeline exists.
3. Check the versioning scheme against SemVer (`MAJOR.MINOR.PATCH`, meaningful bumps).
4. Check for supply-chain practices: build provenance/signing (SLSA), a documented secure development process (NIST SSDF), dependency update automation.
5. Check that lifecycle documentation (contributing guide, branching model, release notes) exists and is current.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
