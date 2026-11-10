---
name: review-twelve-factor
description: 'Reviews deployable services against the Twelve-Factor App methodology, one check per factor (codebase, dependencies, config, backing services, build/release/run, stateless processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes), against a local summary of 12factor.net and a local Twelve-Factor Rubric that accepts modern platform equivalents. Use when the compliance-reviewer orchestrator delegates the Twelve-Factor subject.'
user-invocable: false
---

# Review: Twelve-Factor App

Assesses whether each deployable is built to run as a twelve-factor app: one codebase, declared and isolated
dependencies, config outside the code, backing services as attached resources, separated build/release/run stages,
stateless and disposable processes, port binding, process-model scaling, dev/prod parity, logs as event streams and
one-off admin processes. Modern platform equivalents (container images, orchestrator-injected config, secret
managers, OTLP exporters) count when they meet a factor's intent.

## Inputs

The capped file list assigned by `compliance-inventory` (config files including environment-named ones, `Dockerfile`,
`docker-compose*.yml`, process and workload definitions, entry point and startup files, logging configuration,
dependency manifests, `.env.example`, admin or migration script locations), plus the header value `targetGitHead`.
Review only those files.

## Standards (local, authoritative)

- `references/standards/twelve-factor-app.md`: TFA-01…TFA-55, summarized from 12factor.net. Always load.
- `references/standards/twelve-factor-rubric.md`: TFR-01…TFR-20, the applicability table and accepted modern
  equivalents. Always load.
- Do **not** fetch any URL for this skill. Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation, apply the closest element if it clearly fits. Otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md` and both standards files.
2. Skip generated and vendored files (`obj/`, `bin/`, `target/`, `build/`, `dist/`, `node_modules/`, `vendor/`);
   read lock files only to confirm a declaration exists. Note any skipped.
3. Classify each deployable with the rubric's applicability table and mark excluded checks N/A
   ("not applicable to <kind>"). A check fails if any deployable in the file list fails it; name the deployable.
   If the kind is unclear, treat it as a long-running service, use confidence `low` for kind-dependent findings and
   add `localized-standard-gap: deployable kind unclear` to `notes`.
4. Modern equivalents listed in the rubric satisfy an element. Fail only on a concrete rubric fail signal in the
   reviewed files. If the comparison partner isn't visible (e.g. no production backing-service definition for TF-10,
   no Dockerfile, manifest or deploy step for TF-05), mark the check N/A ("<what> not visible"). Development-gated
   configuration passes everywhere except TF-10.
5. TF-01: version control is shown by a non-null `targetGitHead` or a `.hg/`/`.svn/` directory at the root; never
   read Git data, and never fail TF-01 because version control isn't visible (mark TFA-01 N/A instead).
6. For each check TF-01…TF-12, evaluate only the elements it lists whose "Applies when" condition holds; if none
   apply, mark the check N/A with that reason.
7. Boundaries: don't fail for lock files or version pinning (review-dependency-management), secret delivery hygiene
   or log-file protection (review-security-operational; hardcoded credentials fail TF-03 *and* SEC-OP-05 on purpose),
   log structure, telemetry export or health endpoints (review-observability), message ack, requeue or idempotency
   (review-reliability), scale-out efficiency other than statelessness (review-performance; statelessness, session state and sticky sessions are judged only here, TF-06), release automation, SemVer or committed binaries
   (review-software-lifecycle), config documentation (review-maintainability), or test-time substitutes
   (review-testing). TF-07 accepts TLS termination at a platform router; never recommend a plain-HTTP public listener.
8. Severity: every Finding takes the check's default severity from `checklist.md`;
   `checkResults.severityIfFailed` is always that default.
9. Citations: `standard` = "<source name> — <element ID>" of the failed element (source names in each standards
   file header); `url` = `https://12factor.net/` + the element's page path, or for rubric elements the
   `docs/reports/`-relative path + `#tfr-NN`. `urlsFetched` stays empty.
10. Note strengths where config is cleanly externalized with a documented template, images are built once and
    promoted, processes are stateless with graceful shutdown, or development mirrors production services.

## Output

Labels: copy `subject`/`subSubject` from `references/checklist.md` (the `Subject:` line and the check's `Sub-subject`
column); never invent or combine labels. Follow `compliance-review-core`'s `finding-schema.md`.
