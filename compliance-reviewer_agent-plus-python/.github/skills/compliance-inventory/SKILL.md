---
name: compliance-inventory
description: 'Builds a repo map (languages, frameworks, entry points, API specs, IaC, CI/CD, tests, dependency manifests, config) and produces the per-subject file list, split into batches for large repos. Use when the compliance-reviewer orchestrator runs step 01 of a compliance review, before any subject skill is invoked.'
user-invocable: false
---

# Compliance Inventory

## Procedure

1. **Detect languages.** Search the target for the signals in `compliance-review-core`'s `references/languages.md` (`*.csproj`/`*.sln` → csharp, `pom.xml`/`build.gradle*` → java, `pyproject.toml`/`requirements.txt`/`setup.py` → python). Record every language found; a repo may have more than one.
2. **Detect frameworks and entry points.** Look for well-known framework markers (e.g. `Program.cs`/`Startup.cs`, `Application.java`/Spring Boot annotations, `manage.py`/`main.py`/FastAPI/Flask/Django imports) to identify the app's entry points.
3. **Find API specs.** Search for `openapi.*`, `swagger.*`, and controller/route files (`Controllers/`, `@RestController`/`@RequestMapping`, `@app.route`/FastAPI routers). If none are found, record that API Design is N/A for this run.
4. **Find infrastructure and process files.** Dockerfiles, `docker-compose*.yml`, IaC (`*.bicep`, `*.tf`, `*.yaml` under `k8s`/`helm`), CI/CD (`.github/workflows/*.yml`, `azure-pipelines.yml`, `Jenkinsfile`), test folders (`tests/`, `test/`, `*Test.java`, `test_*.py`, `*.Tests/`), dependency manifests (`*.csproj`, `pom.xml`, `build.gradle*`, `requirements.txt`, `package.json` if present), and config files (`appsettings*.json`, `application*.properties/yml`, `.env.example`, `pyproject.toml`).
5. **Determine `iacFound`.** Set `iacFound: true` only if step 4 found actual infrastructure-as-code (`*.bicep`, `*.tf`, `*.yaml`/`*.yml` under `k8s`/`helm`, or equivalent ARM/CloudFormation/Pulumi files) — a `Dockerfile`/`docker-compose*.yml` alone does not count. `review-disaster-recovery`, `review-cost-sustainability` and `review-monitoring` are entirely IaC-driven (backup/replication config, autoscaling/sizing config, alert/dashboard-as-code), so when `iacFound` is false, mark all three `applicable: false` in the output below with reason `"no infrastructure-as-code found"`, the same way `review-api-design` is skipped when no API spec is found. The orchestrator then skips the subagent call for these subjects entirely, recording an N/A `checkResults` entry per their checklist instead.
6. **Map files to subjects.** For each of the 18 subject skills, list the files relevant to its checklist (see `references/subject-file-map.md`). A file may belong to more than one subject.
7. **Batch large subjects.** If a subject's file list exceeds ~40 files (or would clearly exceed a worker's practical context), split it into ordered batches of roughly even size, keeping related files (e.g. a controller and its tests) in the same batch where possible.
8. **Write the output.** Produce `01-inventory.json` with the header fields from `transition-schema.md` plus:

```json
{
  "languages": ["csharp", "python"],
  "frameworks": ["ASP.NET Core", "FastAPI"],
  "apiSpecsFound": true,
  "iacFound": false,
  "subjects": {
    "review-api-design": { "files": ["..."], "batches": [["..."]], "applicable": true },
    "review-security-identity-access": { "files": ["..."], "batches": [["..."], ["..."]], "applicable": true },
    "review-disaster-recovery": { "files": [], "batches": [], "applicable": false },
    "review-cost-sustainability": { "files": [], "batches": [], "applicable": false },
    "review-monitoring": { "files": [], "batches": [], "applicable": false }
  },
  "skippedSubjects": {
    "review-api-design": "reason, if applicable is false",
    "review-disaster-recovery": "no infrastructure-as-code found",
    "review-cost-sustainability": "no infrastructure-as-code found",
    "review-monitoring": "no infrastructure-as-code found"
  }
}
```

## References

- [`references/subject-file-map.md`](./references/subject-file-map.md) — which file globs feed which subject skill.
- [`references/analyzers.md`](./references/analyzers.md) — the optional analyzer step (step 02), run only after user approval.
