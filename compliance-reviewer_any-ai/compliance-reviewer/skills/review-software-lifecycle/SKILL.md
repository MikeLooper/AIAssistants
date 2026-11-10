---
name: review-software-lifecycle
description: 'Reviews CI on every change, release automation, Semantic Versioning, branch-protection enforcement (from settings-as-code and CODEOWNERS), build provenance and signing, security policy, CI/CD workflow hardening, static analysis gates and committed binaries, against local, pinned summaries of SemVer 2.0.0, NIST SSDF 1.1, SLSA v1.2 and OpenSSF Scorecard. Use when the compliance-reviewer orchestrator delegates the Software Lifecycle subject.'
user-invocable: false
---

# Review: Software Lifecycle

Assesses how the project builds, protects, versions and releases its software, as visible in repository files:
CI pipelines, release workflows, version fields, settings-as-code, CODEOWNERS, `SECURITY.md`, SAST config and
committed binaries. It uses local, pinned summaries of SemVer 2.0.0, NIST SP 800-218 SSDF 1.1, SLSA v1.2 and the
OpenSSF Scorecard checks. Git history, tags, releases and forge settings are not read.

## Inputs

CI/CD definitions (`.github/workflows/*`, `azure-pipelines*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`), release-tool
config, Dockerfiles and scripts used by CI, version-bearing manifests, settings-as-code and CODEOWNERS,
`SECURITY.md`, SAST config, and `CHANGELOG*` (version history only), per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/semver.md` — SV-01…SV-11. Always load.
- `references/standards/nist-ssdf.md` — SSDF-01…SSDF-19. Always load.
- `references/standards/slsa.md` — SLSA-01…SLSA-14. Always load.
- `references/standards/openssf-scorecard.md` — OSC-01…OSC-21. Always load.
- `references/standards/azure-waf-safe-deployment.md` — SDP-01 (staged rollouts). Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, `references/lifecycle-signals.md` and the five
   standards files.
2. Files only: judge only what the files show. Never read Git history, tags or releases, and never assume forge
   settings. Release assets and registries are judged through the workflow steps that produce them.
3. Platform: identify the CI platform(s) and forge from `lifecycle-signals.md` §1. Apply Scorecard elements through
   the platform equivalents there; skip an element with "no equivalent on <platform>" if none exists.
4. Publish scope: decide whether the repo publishes versioned artifacts (publishable manifest with name and version,
   release or deploy pipeline, or versioned API). If not, SL-02 and SL-05 are N/A ("repo publishes no versioned
   artifacts") and SL-03 judges only SV-01, SV-07 and SV-08 on any declared version.
5. Settings (SL-04): judge SSDF-11, SSDF-15, SLSA-10…14, OSC-01…03 and OSC-05 only from settings-as-code
   (`lifecycle-signals.md` §3); otherwise skip them ("repository settings not visible in files"). Documentation
   claims are not evidence. SSDF-10 and OSC-04 (CODEOWNERS) apply whenever the forge supports CODEOWNERS. If every
   SL-04 element is skipped, SL-04 is N/A with that reason, never a failure.
6. Versions (SL-03): judge the published version field per `lifecycle-signals.md` §9 (ecosystem equivalents
   accepted; 4-part assembly/file versions are not judged; a `v` prefix only in tag patterns).
7. Committed binaries (SL-12): match `lifecycle-signals.md` §10 patterns; exclude paths matched by `.gitignore` (read as a plain file; never run Git), build-output
   and environment folders, and binaries referenced by a manifest (review-dependency-management DEP-08). Use
   confidence `medium` unless the binary sits in a source folder.
8. Boundaries: don't fail for tests in CI (review-testing TST-06), dependency pinning, lock files, SBOM or update
   automation (review-dependency-management), contributing/branching docs or change logs (review-maintainability),
   pipeline secrets or OIDC credentials (review-security-operational SMG-12), or lint/format rules
   (review-software-quality). Staged rollouts and rollback paths are judged here (SDP-01 under SL-02): fail SDP-01
   only when a production deployment job or deployment config in scope releases straight to all of production with
   no staged step (ring, canary, slot swap, blue-green), no gate between stages and no rollback step; confidence
   `medium`. Runtime redundancy and restart behaviour stay with review-reliability.
9. For each check (SL-01…SL-05, SL-07, SL-09…SL-12), evaluate only the elements it lists whose "Applies when"
   condition holds. If none apply, mark the check N/A with that reason. SL-06 and SL-08 are retired: don't evaluate
   them or write them to `checkResults`.
10. Evidence rule: fail only on concrete evidence in the files (see `lifecycle-signals.md` fail signals). Use
    confidence `medium` unless the evidence is unambiguous.
11. Severity: every Finding takes the check's default severity from `checklist.md`;
    `checkResults.severityIfFailed` is always that default.
12. Citations: `standard` = "<source name> — <element ID>" (source names in each standards file header);
    `url` = citation base + page path + "#" + primary anchor (SSDF: the PDF URL + `#page=N`). Never cite
    `lifecycle-signals.md`. `urlsFetched` stays empty.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
