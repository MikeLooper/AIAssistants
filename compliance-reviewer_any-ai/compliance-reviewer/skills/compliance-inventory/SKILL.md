---
name: compliance-inventory
description: 'Builds a repo map (languages, frameworks, entry points, API specs, IaC, CI/CD, tests, dependency manifests, config) and assigns each applicable subject a capped list of concrete files, then groups subjects with heavily overlapping file lists into small batches so one worker call can cover them without widening any one subject input. Use when the compliance-reviewer orchestrator runs step 01 of a compliance review, before any subject skill is invoked.'
user-invocable: false
---

# Compliance Inventory

## Procedure

Work from the target's working files only: list files from the working tree, minus the generated and build-output folders in `references/subject-file-map.md`. Never run Git or read `.git/` (see "Repository contents" in `compliance-review-core`'s `finding-schema.md`).

**Input: `advanced`** (the orchestrator's resolved `--advanced` flag, default `false`). When it is `false`, infrastructure-as-code is out of scope for the whole run. **IaC files** here means `*.bicep`, `*.tf`/`*.tfvars`, ARM templates, CloudFormation/SAM templates, Pulumi programs and stacks, Kubernetes manifests and Helm charts/values (wherever they are), and Kustomize files. `Dockerfile`s, `docker-compose*.yml`, devcontainer config, `Procfile`/`app.json`, CI/CD pipeline files and application config files are not IaC and stay in scope.

1. **Detect languages.** Search the target for the signals in `compliance-review-core`'s `references/languages.md` (`*.csproj`/`*.sln` → csharp, `pom.xml`/`build.gradle*` → java, `pyproject.toml`/`requirements.txt`/`setup.py` → python, `package.json`/`tsconfig.json` → javascript). Record every language found; a repo may have more than one.
2. **Detect frameworks and entry points.** Look for well-known framework markers (e.g. `Program.cs`/`Startup.cs`, `Application.java`/Spring Boot annotations, `manage.py`/`main.py`/FastAPI/Flask/Django imports) to identify the app's entry points.
3. **Find API specs.** Search for `openapi.*`, `swagger.*`, and controller/route files (`Controllers/`, `@RestController`/`@RequestMapping`, `@app.route`/FastAPI routers). If none are found, record that API Design is N/A for this run.
4. **Find infrastructure and process files.** Dockerfiles, `docker-compose*.yml`, devcontainer config, process definitions (`Procfile`, `app.json`, serverless manifests), logging configuration (`logback*.xml`, `log4j2*.xml`, `nlog.config`, `logging.conf`/`.yaml`), IaC (`*.bicep`, `*.tf`, `*.yaml` under `k8s`/`helm`; only when `advanced` is `true`; otherwise don't search for or list IaC files), CI/CD (`.github/workflows/*.yml`, `azure-pipelines*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`), repository process files (`CODEOWNERS`, `SECURITY.md`, settings-as-code such as `.github/settings.yml` or Terraform branch-protection/ruleset files, release-tool config such as `release-please-config.json`, `.releaserc*`, `.goreleaser.yml`, `GitVersion.yml`), test folders (`tests/`, `test/`, `*Test.java`, `test_*.py`, `*.Tests/`), dependency manifests (`*.csproj`, `pom.xml`, `build.gradle*`, `requirements.txt`, `package.json` if present), and config files (`appsettings*.json`, `application*.properties/yml`, `.env.example`, `pyproject.toml`).
5. **Determine `iacFound`.** When `advanced` is `false`, set `iacFound: false` without searching, and mark `review-disaster-recovery`, `review-cost-sustainability` and `review-monitoring` `applicable: false` with reason `"advanced usage off (IaC not reviewed)"`. Otherwise, set `iacFound: true` only if step 4 found actual infrastructure-as-code (`*.bicep`, `*.tf`, `*.yaml`/`*.yml` under `k8s`/`helm`, or equivalent ARM/CloudFormation/Pulumi files) — a `Dockerfile`/`docker-compose*.yml` alone does not count. `review-disaster-recovery`, `review-cost-sustainability` and `review-monitoring` are entirely IaC-driven (backup/replication config, autoscaling/sizing config, alert/dashboard-as-code), so when `iacFound` is false, mark all three `applicable: false` in the output below with reason `"no infrastructure-as-code found"`, the same way `review-api-design` is skipped when no API spec is found. The orchestrator then skips the worker call for these subjects entirely, recording an N/A `checkResults` entry per their checklist instead. CI pipeline files, DR documents and monitoring files outside IaC folders (Prometheus rule files, Grafana JSON) don't set `iacFound` by themselves.
6. **Map files to subjects.** For each of the 17 subject skills, list the files relevant to its checklist as **concrete relative file paths** — expand every glob; never emit a bare directory or `**` pattern — following `references/subject-file-map.md` (including its exclusions: test files go only to `review-testing`; manifests go to `review-dependency-management`, plus `review-twelve-factor` and the root manifest to `review-maintainability`). Cap every subject's list at **12 files** (the original skill averaged about 5 per subject and never exceeded 11) (`maxFilesPerSubject`). If more files match, sample: entry points first, then one or two representative files per layer/folder, then the files most relevant to the checklist; record `sampled: true` and `totalMatched`. Record each subject's `applicable` flag (false only for API Design with no API found, or the IaC-gated trio when `iacFound` is false). A file may appear in more than one subject's list. When `advanced` is `false`, exclude every IaC file (definition above) from every subject's list, even where a row of the file map names IaC, Kubernetes or Helm files.
   - **`testInventory` (for `review-testing`).** Because the 12-file sample can't show the test pyramid, also record a summary computed from the full set of test files (cheap name and reference greps only; don't read every test):
     - `testProjects`: one entry per test project or test folder with its `path`, `category` and `files` (test-file count). Category: `e2e` if it references Playwright, Selenium, Cypress, Puppeteer or REST-assured against a base URL; else `integration` if it references Testcontainers, `WebApplicationFactory`/`TestServer`, `@SpringBootTest`/`@DataJpaTest`, WireMock/MockServer or a real database fixture; else `unit` if it uses a test framework (xUnit/NUnit/MSTest, JUnit/TestNG, pytest/unittest, Jest/Vitest/Mocha, Go `testing`); otherwise `unclassified`. A folder or project name (`*.UnitTests`, `*.IntegrationTests`, `e2e/`, `tests/integration/`) decides only between categories whose references are both present.
     - `totals`: test-file counts per category (`unit`, `integration`, `e2e`, `unclassified`).
     - `productionRoots`: the production project or package roots (for example each non-test `*.csproj` folder, Maven/Gradle module, Python package or workspace package), excluding generated code and migrations.
     - `signals`: `accessControl` (authentication/authorization setup or attributes found), `integrationPoints` (a data store, outbound HTTP/messaging client, or two or more services found), `untrustedInput` (HTTP endpoints or file/message parsers found), `loadTests` (load-test scripts or configs found, per the `review-testing` row of `subject-file-map.md`) and `faultInjection` (chaos or fault-injection definitions found), each `true`/`false`.

     If the repository has no test files, record `totals` as all zeros and `testProjects` as `[]`.
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
  "advanced": false,
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
    "review-disaster-recovery": "advanced usage off (IaC not reviewed)"
  },
  "testInventory": {
    "testProjects": [
      { "path": "test/Web.Tests", "category": "unit", "files": 42 },
      { "path": "test/Web.IntegrationTests", "category": "integration", "files": 6 },
      { "path": "test/Web.E2E", "category": "e2e", "files": 8 }
    ],
    "totals": { "unit": 42, "integration": 6, "e2e": 8, "unclassified": 0 },
    "productionRoots": ["src/Web", "src/Domain", "src/Infrastructure"],
    "signals": { "accessControl": true, "integrationPoints": true, "untrustedInput": true, "loadTests": false, "faultInjection": false }
  }
}
```

`advanced` echoes the input (optional and non-breaking; older runs lack it and were effectively `true`). `subjects[*].batch` is a single batch id (or `null` when not applicable); add `sampled` and `totalMatched` for any subject whose list was capped. `testInventory` is optional and non-breaking (older runs lack it); write it whenever `review-testing` is among the chosen subjects. The orchestrator passes it to the worker call that covers `review-testing`. The orchestrator makes one worker call per `fileBatches` entry, in order.
## References

- [`references/subject-file-map.md`](./references/subject-file-map.md) — which file globs feed which subject skill.
- [`references/analyzers.md`](./references/analyzers.md) — the optional analyzer step (step 02), run only when advanced usage is on and only for approved analyzers.


