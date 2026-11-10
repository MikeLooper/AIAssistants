---
name: review-dependency-management
description: 'Reviews dependency version pinning, lock files, analyzer-reported vulnerabilities, end-of-life runtimes and frameworks, SBOM presence, automated update/scanning configuration, trusted package sources and pre-release dependencies, against OWASP supply-chain guidance and pinned vendor lifecycle data. Use when the compliance-reviewer orchestrator delegates the Implementation / Dependency Management subject.'
user-invocable: false
---

# Review: Dependency Management

Assesses how third-party dependencies are declared, pinned, sourced, scanned and kept on supported versions,
using local, pinned summaries of OWASP supply-chain guidance and vendor lifecycle data.

## Inputs

Dependency manifests, lock files, central package files, package-source config (`nuget.config`, `pip.conf`,
`.npmrc`, Maven `settings.xml`), runtime pins (`global.json`, `.python-version`, `runtime.txt`, `.nvmrc`,
`.node-version`), dependency-update
config (Dependabot/Renovate), scanner suppression files, SBOM files and `02-analyzers.json` (if present),
per `compliance-inventory`.

## Standards (local, authoritative)

- `references/standards/owasp-supply-chain.md` — OTT-01…OTT-09, OCS-01…OCS-15. Always load.
- `references/standards/lifecycle-dotnet.md` — NET-01…06, NFX-01…05. Load when language `csharp` is detected.
- `references/standards/lifecycle-java.md` — JDK-01…08, SPR-01…07. Load when language `java` is detected.
- `references/standards/lifecycle-python.md` — PY-01…07. Load when language `python` is detected.
- `references/standards/lifecycle-javascript.md` — NODE-01…05, EXP-01. Load when language `javascript` is detected.
- Do **not** fetch any URL for this skill, and never use remembered CVE, end-of-life or license facts.
  Do not load `references/standards/MAINTENANCE.md`.
- If no element covers a situation: apply the closest element if it clearly fits; otherwise mark the check N/A
  ("not covered by localized standard") and add `localized-standard-gap: <description>` to `notes`.

## Procedure

1. Load `references/checklist.md`, `references/sources.md`, the OWASP file and the lifecycle file(s) for the detected
   languages. A `generic`-only target loads no lifecycle file; DEP-04 is then N/A ("no localized lifecycle data for
   detected languages").
2. Reference date = the date part of the `startedAt` header value you were given.
3. For each active check (DEP-01…DEP-05, DEP-07…DEP-09; DEP-06 is retired and is not written to `checkResults`),
   evaluate the elements it lists against the subject's files. Mark the check N/A with a reason when no element
   applies (e.g. DEP-02 for Maven-only targets; DEP-07 when no update/scanning config is in the file list).
4. DEP-03 (analyzer-only): use only vulnerability entries in `02-analyzers.json` (result keys `dotnet-vulnerable`,
   `pip-audit`, `maven-dependency-check`, `gradle-dependency-check`). If there are none, mark DEP-03 N/A
   ("no vulnerability analyzer output for this run"). One finding per package + advisory; evidence is the declaring
   manifest line (or the direct dependency for a transitive package), with the advisory id in the excerpt; cite
   OTT-09 (or OCS-03), not the CVE. Severity: Critical/High → Error, Moderate/Medium → Warning, Low → Information,
   none reported → Error. DEP-09 (OTT-08) may cite `dotnet-deprecated` entries as evidence of deprecated packages;
   `dotnet-outdated` entries are context only (an older but supported version is not a finding by itself).
5. DEP-04 (date rule): find each declared runtime/framework target and its lifecycle row. `YYYY-MM` dates mean the
   last day of that month. Support end before the reference date → finding (Error). Within 180 days after it → pass,
   and add `eol-approaching: <product> <line> on <date>` to `notes`. "With the host OS" lines pass. Multi-targeting:
   one finding per EOL target (`netstandard*` is never EOL). Version ranges: fail only if the highest permitted
   version is EOL; a lower bound below the oldest supported line adds `eol-lower-bound: <range>` to `notes`.
   With Spring Boot, evaluate Boot, not the Framework it manages (unless the manifest overrides the Framework
   version). `Microsoft.AspNetCore.*`/`EntityFrameworkCore.*`/`Extensions.*` at major N follow .NET N (NET-06).
   Pre-release lines aren't EOL; a production manifest targeting one fails DEP-09 instead.
   A line newer than every row → N/A + `localized-standard-gap: <product> <line> not in lifecycle snapshot <date>`.
   If the reference date is more than 9 months after a lifecycle file's "Localized" date, add
   `localized-standard-stale: <file> localized <date>` to `notes`.
6. Evidence rule: fail a practice element only on concrete evidence in the files (floating version, `http://` feed,
   pre-release version in production scope, missing lock file where the ecosystem supports one). Don't fail on
   speculation. Use confidence `medium` unless the evidence is unambiguous.
7. Severity: practice elements take the check's default from `checklist.md`, except that a plain-`http://` package
   source or unmapped mixed public/private feeds is Error. `checkResults.severityIfFailed` is the check's default.
8. Citations: `standard` = "<source name> — <element ID>" (source name from the standards file header);
   `url` = citation base + "#" + primary anchor (first anchor listed). `urlsFetched` stays empty.
9. Boundaries: **owned here** — vulnerable or outdated library versions, through analyzer output only (DEP-03);
   EOL runtimes and frameworks (DEP-04); pinning (DEP-01); lock files (DEP-02, sole owner); SBOM (DEP-05); update
   automation (DEP-07); manifest-referenced binaries (DEP-08); test-only packages in production dependency scope
   (DEP-09). **Don't fail for** CI/CD workflow hardening, action/image pinning in workflows, provenance or signing
   (review-software-lifecycle SL-05, SL-09, SL-10); committed binaries not referenced by a manifest (SL-12); unsafe
   *use* of parsers, serializers or loggers (review-security-input-injection, review-security-operational); install
   commands and download-and-execute in CI (SL-10, OSC-13); licence files (review-maintainability MAINT-10).
   Without analyzer output, vulnerable versions of libraries such as XStream, fastjson, Kryo, SnakeYAML, Expat or
   Log4j 2 aren't reported by any skill (accepted consequence of plan DEC-2); add `no-analyzer-output` to `notes`.

## Output

Findings, strengths and check results per `compliance-review-core`'s `finding-schema.md`.
