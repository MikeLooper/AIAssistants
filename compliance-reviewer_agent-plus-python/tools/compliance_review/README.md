# compliance_review (Python CLI)

A dependency-free Python implementation of the deterministic parts of the
`compliance-reviewer` agent pipeline (see [docs/compliance-reviewer/README.md](../../docs/compliance-reviewer/README.md)
for the full agent-based flow this complements).

## Scope

| Phase | What it covers | Status |
|-------|-----------------|--------|
| 1 | Inventory, scoring, cross-subject dedup + aggregation, report rendering, transition/state files | Implemented |
| 2 | Tool-backed checks: lock file presence, CI presence, hardcoded-secret regex scan, `.editorconfig`/formatter presence, OpenAPI structural validation, SBOM presence, and (opt-in) `dotnet`/`npm`/`pip-audit` vulnerability scans | Implemented |
| 3 | Checks that require reading code semantically (architecture quality, naming, spec-vs-implementation drift, auth/authz judgment, etc.) | Not implemented — an LLM (or the `compliance-reviewer` agent) is still needed for these |

Everything this CLI can't evaluate is written out as `N/A` with reason
`"requires semantic review (Phase 3, not implemented in this CLI)"` and is
excluded from scoring, rather than guessed at.

## Usage

```powershell
# From the repo root:
python -m tools.compliance_review <path-to-target-repo>

# Also run installed vulnerability scanners (dotnet/npm/pip-audit), if present:
python -m tools.compliance_review <path-to-target-repo> --run-vuln-scanners

# List runs that didn't finish:
python -m tools.compliance_review --list-resumable
```

Writes the same artifact shapes the agent pipeline uses:
- `transitions/<runId>/00-init.json`, `01-inventory.json`, `02-analyzers.json`, `90-aggregate.json`, `99-report.json`
- `docs/reports/<target-name>-compliance-review-python-<runId>.md`

No install step is required — everything is stdlib only. `--run-vuln-scanners`
shells out to whichever of `dotnet`/`npm`/`pip-audit` are already installed
and skips (marks `N/A`) any that aren't, without failing the run.

## Tests

```powershell
python -m unittest discover -s tools/compliance_review/tests -t .
```

## Layout

```
tools/compliance_review/
  schemas.py       # Finding/Strength/CheckResult/TransitionHeader dataclasses
  state.py         # run-id, transition-file paths, state.json, resume rules
  status.py        # status-line formatting
  inventory.py     # language/framework/API-spec/IaC detection, subject-file mapping, batching
  scoring.py       # severity weights, subject/overall score + band
  aggregate.py     # cross-subject duplicate-evidence merge, severity counts, top-5 risks
  report.py        # tiny mustache-subset renderer for the shared report-template.md
  analyzers/       # Phase 2 tool-backed checks (one module per check/tool)
  cli.py           # wires it all together
  tests/           # unittest-based tests for every module above
```
