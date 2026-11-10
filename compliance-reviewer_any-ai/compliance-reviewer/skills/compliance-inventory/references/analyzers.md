# Optional Analyzer Step (Step 02)

Runs installed CLI analyzers to supplement file-reading review. Executed only when the run's `--advanced` flag is `on`, and only for the analyzers approved for this run (chosen by the user in an interview run, or selected by `--analyzers`, default `auto`). Otherwise this step is skipped and noted as skipped in `state.json`.

## Detection

Check which of these are installed/available in the target's environment before offering or running them. **Auto** marks the analyzers that `--analyzers auto` (the default) selects; the others run only when named.

| Key | Language | Analyzer | Command | Auto |
|-----|----------|----------|---------|------|
| `dotnet-vulnerable` | C#/.NET | Vulnerable package scan | `dotnet list package --vulnerable --include-transitive` | yes |
| `dotnet-deprecated` | C#/.NET | Deprecated packages | `dotnet list package --deprecated` | yes |
| `dotnet-outdated` | C#/.NET | Outdated packages | `dotnet list package --outdated` | yes |
| `maven-tree` | Java (Maven) | Dependency tree | `mvn -q dependency:tree` | yes |
| `gradle-tree` | Java (Gradle) | Dependency tree | `gradle dependencies` | yes |
| `maven-dependency-check` | Java (Maven) | Vulnerability scan (OWASP Dependency-Check) | `mvn org.owasp:dependency-check-maven:check` — offer only if the plugin is already installed or resolvable offline. It may download its vulnerability database: tell the user about the network use when offering it | no |
| `gradle-dependency-check` | Java (Gradle) | Vulnerability scan (OWASP Dependency-Check) | `gradle dependencyCheckAnalyze` — offer only when the `org.owasp.dependencycheck` plugin is already configured in the build; same network note as Maven | no |
| `pip-audit` | Python | Vulnerability scan | `pip-audit` | yes |
| `lint` | Generic | Linters already configured in the repo | run the project's own configured lint script if one exists (e.g. `npm run lint`, `dotnet format --verify-no-changes`) | no |

Why some are not in the auto set: OWASP Dependency-Check downloads a large vulnerability database and is slow; `lint` executes scripts defined by the target itself. The auto-set analyzers may still contact their package registry or advisory service (NuGet, Maven Central, PyPI/OSV) to look up versions and advisories.

## Procedure

1. List which analyzers above are applicable given the detected languages (from `01-inventory.json`) and installed.
2. Resolve the set to run: in an interview run, ask the user (via the orchestrator's question step, not here) which applicable analyzers to run, recommending the auto set; otherwise use `--analyzers` — `auto` (applicable installed analyzers marked Auto), `none`, or a comma-separated list of keys (keep only applicable, installed ones; record the rest as not run). Do not run anything outside the resolved set.
3. Run each approved analyzer with the shell/terminal tool, in the target directory, without modifying any file (all of the commands above are read-only/report-only).
4. Capture stdout/stderr and parse into a simple structured shape:

```json
{
  "schemaVersion": 1,
  "runId": "...",
  "stepId": "02-analyzers",
  "status": "completed",
  "results": {
    "dotnet-vulnerable": { "command": "...", "exitCode": 0, "findings": ["package X has CVE-..."] }
  }
}
```

   Result keys are the **Key** column above. `findings` stays a list of free-text lines (one per reported package or issue).
5. Write `02-analyzers.json`. The `review-dependency-management` skill (and others where relevant) reads this file if present, in addition to its own file-based checks.
6. If an analyzer isn't installed or errors out, record that in `results` and continue — never block the pipeline on a missing analyzer.
