---
name: compliance-inventory
description: 'Builds a repo map (languages, frameworks, entry points, API specs, IaC, CI/CD, tests, dependency manifests, config) and assigns each applicable subject a capped list of concrete files, then groups subjects with heavily overlapping file lists into small batches so one worker call can cover them without widening any one subject input. Use when the compliance-reviewer orchestrator runs step 01 of a compliance review, before any subject skill is invoked.'
user-invocable: false
---

# Compliance Inventory

## Procedure

1. **Detect languages.** Search the target for the signals in `compliance-review-core`'s `references/languages.md` (`*.csproj`/`*.sln` → csharp, `pom.xml`/`build.gradle*` → java, `pyproject.toml`/`requirements.txt`/`setup.py` → python). Record every language found; a repo may have more than one.
2. **Detect frameworks and entry points.** Look for well-known framework markers (e.g. `Program.cs`/`Startup.cs`, `Application.java`/Spring Boot annotations, `manage.py`/`main.py`/FastAPI/Flask/Django imports) to identify the app's entry points.
3. **Find API specs.** Search for `openapi.*`, `swagger.*`, and controller/route files (`Controllers/`, `@RestController`/`@RequestMapping`, `@app.route`/FastAPI routers). If none are found, record that API Design is N/A for this run.
4. **Find infrastructure and process files.** Dockerfiles, `docker-compose*.yml`, IaC (`*.bicep`, `*.tf`, `*.yaml` under `k8s`/`helm`), CI/CD (`.github/workflows/*.yml`, `azure-pipelines.yml`, `Jenkinsfile`), test folders (`tests/`, `test/`, `*Test.java`, `test_*.py`, `*.Tests/`), dependency manifests (`*.csproj`, `pom.xml`, `build.gradle*`, `requirements.txt`, `package.json` if present), and config files (`appsettings*.json`, `application*.properties/yml`, `.env.example`, `pyproject.toml`).
5. **Determine `iacFound`.** Set `iacFound: true` only if step 4 found actual infrastructure-as-code (`*.bicep`, `*.tf`, `*.yaml`/`*.yml` under `k8s`/`helm`, or equivalent ARM/CloudFormation/Pulumi files) — a `Dockerfile`/`docker-compose*.yml` alone does not count. `review-disaster-recovery`, `review-cost-sustainability` and `review-monitoring` are entirely IaC-driven (backup/replication config, autoscaling/sizing config, alert/dashboard-as-code), so when `iacFound` is false, mark all three `applicable: false` in the output below with reason `"no infrastructure-as-code found"`, the same way `review-api-design` is skipped when no API spec is found. The orchestrator then skips the subagent call for these subjects entirely, recording an N/A `checkResults` entry per their checklist instead.
6. **Map files to subjects.** For each of the 17 subject skills, list the files relevant to its checklist as **concrete relative file paths** — expand every glob; never emit a bare directory or `**` pattern — following `references/subject-file-map.md` (including its exclusions: test files go only to `review-testing`, manifests only to `review-dependency-management`). Cap every subject's list at **12 files** (the original skill averaged about 5 per subject and never exceeded 11) (`maxFilesPerSubject`). If more files match, sample: entry points first, then one or two representative files per layer/folder, then the files most relevant to the checklist; record `sampled: true` and `totalMatched`. Record each subject's `applicable` flag (false only for API Design with no API found, or the IaC-gated trio when `iacFound` is false). A file may appear in more than one subject's list.
7. **Group subjects into batches.** Every applicable subject goes into **exactly one** batch — never split a subject across batches. Batching exists only to share file reads and the fixed per-call loading cost, so group conservatively:
   - Process subjects from the longest file list to the shortest. Start a new batch with the first unplaced subject; add a later subject `S` to an existing batch only if (a) at least 70% of `S`'s files are already in that batch's file set, (b) the batch's combined distinct files stay ≤ 20, and (c) the batch has fewer than 5 subjects. Otherwise try the next batch, or start a new one. A subject with no overlap runs alone as a single-subject batch.
   - Never emit two batches whose file sets are identical or near-identical, and never combine subjects just to fill a group.
   - Each batch records `subjectFiles` (each subject's own file list). The worker reads each file once but evaluates a subject only against that subject's own files — batching must not widen any subject's input.
8. **Write the output.** Produce `01-inventory.json` with the header fields from `transition-schema.md` plus:

```json
{
  "languages": ["csharp", "python"],
  "frameworks": ["ASP.NET Core", "FastAPI"],
  "apiSpecsFound": true,
  "iacFound": false,
  "maxFilesPerSubject": 12,
  "fileBatches": [
    {
      "batchId": "batch-1",
      "subjects": ["review-api-design", "review-security-web-api"],
      "subjectFiles": {
        "review-api-design": ["docs/openapi.json", "src/Web/Controllers/UsersController.cs"],
        "review-security-web-api": ["src/Web/Program.cs", "src/Web/Controllers/UsersController.cs"]
      }
    },
    {
      "batchId": "batch-2",
      "subjects": ["review-testing"],
      "subjectFiles": { "review-testing": ["test/Web.Tests/UsersControllerTests.cs"] }
    }
  ],
  "subjects": {
    "review-api-design": { "batch": "batch-1", "applicable": true, "fileCount": 2 },
    "review-testing": { "batch": "batch-2", "applicable": true, "fileCount": 1 },
    "review-disaster-recovery": { "batch": null, "applicable": false }
  },
  "skippedSubjects": {
    "review-disaster-recovery": "no infrastructure-as-code found"
  }
}
```

`subjects[*].batch` is a single batch id (or `null` when not applicable); add `sampled` and `totalMatched` for any subject whose list was capped. The orchestrator makes one worker call per `fileBatches` entry, in order.
## References

- [`references/subject-file-map.md`](./references/subject-file-map.md) — which file globs feed which subject skill.
- [`references/analyzers.md`](./references/analyzers.md) — the optional analyzer step (step 02), run only after user approval.


