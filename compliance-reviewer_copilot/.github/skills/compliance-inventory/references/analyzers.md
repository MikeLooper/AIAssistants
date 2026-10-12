# Optional Analyzer Step (Step 02)

Runs installed CLI analyzers to supplement file-reading review. Executed only after the user explicitly approves analyzers for this run — otherwise this step is skipped and noted as skipped in `state.json`.

## Detection

Check which of these are installed/available in the target's environment before offering them:

| Language | Analyzer | Command |
|----------|----------|---------|
| C#/.NET | Vulnerable package scan | `dotnet list package --vulnerable --include-transitive` |
| Java (Maven) | Dependency tree | `mvn -q dependency:tree` |
| Java (Gradle) | Dependency tree | `gradle dependencies` |
| Python | Vulnerability scan | `pip-audit` |
| Generic | Linters already configured in the repo | run the project's own configured lint script if one exists (e.g. `npm run lint`, `dotnet format --verify-no-changes`) |

## Procedure

1. List which analyzers above are applicable given the detected languages (from `01-inventory.json`).
2. Ask the user (via the orchestrator's ask-questions step, not here) which of the applicable analyzers to run for this run. Do not run anything unapproved.
3. Run each approved analyzer with `execute`, in the target directory, without modifying any file (all of the commands above are read-only/report-only).
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

5. Write `02-analyzers.json`. The `review-dependency-management` skill (and others where relevant) reads this file if present, in addition to its own file-based checks.
6. If an analyzer isn't installed or errors out, record that in `results` and continue — never block the pipeline on a missing analyzer.
