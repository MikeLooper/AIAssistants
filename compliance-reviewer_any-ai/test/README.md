# Compliance Reviewer test targets

Six very small to-do applications (three APIs and three server-rendered UIs, in C#, Java and Python) that serve as review targets for the Compliance Reviewer. Each one contains a **known set of deliberate flaws**. This README is the answer key, so you can check what a review found, what it missed and how consistent the results are across languages and AI tools.

> **Warning: these apps are insecure on purpose.** They contain hard-coded secrets, XSS, open redirects, stack-trace leaks and similar flaws. Run them only on localhost and never deploy them. The secrets in them are fake values.

## Layout

| App | Directory | Stack | Port |
|-----|-----------|-------|------|
| C# API | [apis/dotNET](apis/dotNET) | .NET 10, ASP.NET Core minimal API, Swashbuckle | 5100 |
| Java API | [apis/java](apis/java) | Java 25, Spring Boot 4.1.2 (Web MVC), springdoc-openapi, Maven | 8080 |
| Python API | [apis/python](apis/python) | Python 3.12+, FastAPI, Uvicorn | 8000 |
| C# UI | [uis/dotNET](uis/dotNET) | .NET 10, ASP.NET Core Razor Pages | 5200 |
| Java UI | [uis/java](uis/java) | Java 25, Spring Boot 4.1.2 (Web MVC + Thymeleaf), Maven | 8081 |
| Python UI | [uis/python](uis/python) | Python 3.12+, Flask 3.1.3 + Jinja | 5000 |

All six use the same domain and store their data in memory only. Each app runs on its own: the UIs don't call the APIs.

The [logic/](logic) folder holds the automated tests that run the reviewer against these apps and score the results against the answer key below; see [Automated validation](#automated-validation).

- **APIs:** `GET /health`, `GET /todos`, `GET /todos/{id}`, `POST /todos`, `PUT /todos/{id}`, `DELETE /todos/{id}?key=<api key>`. A to-do has `id`, `title` and a completed flag.
- **UIs:** one page that lists to-dos, with forms to add a to-do (title, priority, optional return URL) and to mark one done, plus an admin action `/admin/clear?password=…` (C#: `/?handler=Clear&password=…`) that deletes every to-do.

## Running the apps

Prerequisites: .NET SDK 10, JDK 25 with Maven 3.9+, and Python 3.12+.

| App | Commands (run from the app's directory) |
|-----|------------------------------------------|
| C# API | `dotnet run`, then open `http://localhost:5100/swagger` |
| Java API | `mvn spring-boot:run`, then open `http://localhost:8080/swagger-ui/index.html` |
| Python API | `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python main.py`, then open `http://localhost:8000/docs` |
| C# UI | `dotnet run`, then open `http://localhost:5200` |
| Java UI | `mvn spring-boot:run`, then open `http://localhost:8081` |
| Python UI | `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python app.py`, then open `http://localhost:5000` |

Example API calls:

```powershell
curl -X POST http://localhost:5100/todos -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
curl http://localhost:5100/todos
curl -X DELETE "http://localhost:5100/todos/1?key=todo-api-key-7f3c9e2a1b"
```

If Maven fails with `PKIX path building failed` on a machine behind a TLS-inspecting proxy, set `MAVEN_OPTS=-Djavax.net.ssl.trustStoreType=Windows-ROOT` so Java uses the Windows certificate store.

The [.gitignore](.gitignore) here excludes `bin/`, `obj/`, `target/`, `__pycache__/`, `.venv/` and `*.log`. Delete those folders before a manual review: the reviewer judges working files, so build output would add findings (for example SL-12) that aren't part of the answer key. The automated tests do this for you (see [Fresh build](#fresh-build)).

## Reviewing an app

Point the reviewer at **one app directory**, not at `test/`. That keeps this answer key out of the review. For example, from the `compliance-reviewer_any-ai` folder:

```
/compliance-reviewer test/apis/dotNET
/compliance-reviewer test/uis/python --subjects all --programmatic --output file --out-file docs/reports/test-uis-python.md
```

To compare languages, review all three apps of one kind with the same flags and AI tool. To compare AI tools, review the same app with the same flags in each tool.

## Automated validation

The scripts in [logic/](logic) do the review-and-compare work for you. Each test runs the Compliance Reviewer **headlessly** (no interview, no chat) against one app, then scores the run against the [answer key](#answer-key) below and reports a pass or fail verdict.

> Each test is a full review: it uses model credit and takes several minutes per app.

### The tests

| Script | App | Answer key |
|--------|-----|------------|
| [logic/test_api_dotnet.py](logic/test_api_dotnet.py) | C# API ([apis/dotNET](apis/dotNET)) | A1–A12 |
| [logic/test_ui_dotnet.py](logic/test_ui_dotnet.py) | C# UI ([uis/dotNET](uis/dotNET)) | U1–U12 |
| [logic/test_api_java.py](logic/test_api_java.py) | Java API ([apis/java](apis/java)) | A1–A12 |
| [logic/test_ui_java.py](logic/test_ui_java.py) | Java UI ([uis/java](uis/java)) | U1–U12 |
| [logic/test_api_python.py](logic/test_api_python.py) | Python API ([apis/python](apis/python)) | A1–A12 |
| [logic/test_ui_python.py](logic/test_ui_python.py) | Python UI ([uis/python](uis/python)) | U1–U12 |
| [logic/test_all.py](logic/test_all.py) | All six, one after another (default) or at the same time (`--parallel`) | all |
| [logic/selftest_harness.py](logic/selftest_harness.py) | No app: offline checks of the scoring logic and the answer-key file (no AI run, no cost) | — |

The shared logic is in [logic/harness.py](logic/harness.py). [logic/answer_key.json](logic/answer_key.json) is the machine-readable copy of the answer-key tables: when you change a flaw, its expected checks or its location here, change that file too and run the self-test, which checks that every file it names exists.

### Prerequisites

- Python 3.10+ (standard library only; nothing to install).
- The CLI of the AI tool you test with, signed in:
  - **Claude Code**: `claude`.
  - **GitHub Copilot CLI**: `copilot` (`npm install -g @github/copilot`). The `copilot` shim that VS Code puts on the path isn't enough on its own.
- The app's build tools on the path, because each test builds its app first (see [Fresh build](#fresh-build)): the .NET SDK (`dotnet`) for the C# apps and Maven (`mvn`) with a JDK for the Java apps. The Python apps need only the Python that runs the test. Pass `--no-build` to skip the build when a tool isn't installed.

### Fresh build

Before each review, a test:

1. deletes any old build output in the app (`bin/`, `obj/`, `target/`, `__pycache__/`, `.venv/`), because the reviewer would otherwise report findings on it that aren't in the answer key,
2. copies the app's source to `build/<app>` in the results folder and builds that copy from scratch, so the review is of code that compiles as it is now:
   - C#: `dotnet build --nologo -v q`
   - Java: `mvn -B -q clean package -DskipTests`. On Windows, if `MAVEN_OPTS` doesn't already set a trust store, the test adds `-Djavax.net.ssl.trustStoreType=Windows-ROOT` (see the proxy note above).
   - Python: `python -m compileall -q .` (a syntax check; Python has no build step),
3. deletes the copy.

The build runs in a copy so that no build output lands in the folder being reviewed.

The process needs no person to step in, even with the apps open in an IDE:

- [Directory.Build.props](Directory.Build.props) sends the MSBuild output (`bin/`, `obj/`) of every C# project under `test/` to `test/.build-output/<project path>/`, which is git-ignored and outside every app. This covers builds by the test, by you, and by IDE tooling. VS Code's C# extension restores a project as soon as its `obj/` folder is deleted, and before this redirect that put `obj/` back in the app mid-test.
- Just before the review starts, the test checks the app again. If build output has come back anyway, the test deletes it, waits 2 seconds and checks again, up to 5 times. Only output that keeps coming back stops the test with an error.
- The test deletes the copy's redirected output once the build is done.

If the build fails, the test stops with an error (exit code 2) before any AI cost. The build's output is in `<app>-build.log` next to the result, and the result file shows the build commands, their duration and the old folders it deleted. With `--no-build`, step 1 still runs and steps 2 and 3 are skipped.

### Running the tests

Run from the `compliance-reviewer_any-ai` folder:

```powershell
python test/logic/test_api_dotnet.py                          # one app, AI tool chosen automatically
python test/logic/test_ui_java.py --tool copilot              # one app with GitHub Copilot
python test/logic/test_api_python.py --min-found 80           # require only 80% of the flaws
python test/logic/test_all.py                                 # all six, one after another
python test/logic/test_all.py --parallel --tool claude        # all six at the same time
python test/logic/test_all.py --only apis-java,uis-python     # a subset
python test/logic/test_api_java.py --dry-run                  # show the command, don't run it
python test/logic/test_api_java.py --score-only transitions/<runId>   # score an existing run (no AI cost)
cd test/logic; python -m unittest selftest_harness            # offline self-tests
```

Common options (every script; run any script with `--help` for the full list):

| Option | Default | What it does |
|--------|---------|--------------|
| `--tool auto\|claude\|copilot` | `auto` | AI tool that runs the review (see below). Also settable with the `COMPLIANCE_TEST_TOOL` environment variable. |
| `--min-found PCT` | `90` | Share of the 12 seeded flaws that must be found for a pass (90% means 11). Also `COMPLIANCE_TEST_MIN_FOUND`. |
| `--timeout MIN` | `60` | Time limit for each review, in minutes. Also `COMPLIANCE_TEST_TIMEOUT_MIN`. |
| `--progress SEC` | `30` | While a review runs, print a line each time the reviewer finishes a step (read from `transitions/<runId>/state.json`), plus a "still running" heartbeat every SEC seconds. `0` turns progress output off. Also `COMPLIANCE_TEST_PROGRESS_SEC`. |
| `--model NAME` | tool default | Model, passed to the tool's `--model` option. |
| `--tool-arg ARG` | none | Extra argument for the AI tool's CLI; repeat it for more, e.g. `--tool-arg=--max-budget-usd --tool-arg=5`. |
| `--results-dir DIR` | `test/logic/results` | Where results are written. |
| `--no-build` | off | Skip the fresh build. Old build output is still deleted. |
| `--build-timeout MIN` | `15` | Time limit for each build command, in minutes. Also `COMPLIANCE_TEST_BUILD_TIMEOUT_MIN`. |
| `--dry-run` | off | Print the command that would run, then stop. |
| `--score-only RUN_DIR` | — | Single-app scripts only: skip the review and score an existing `transitions/<runId>` folder. |
| `--parallel`, `--only APPS` | serial, all six | `test_all.py` only. App names are `apis-dotNET`, `apis-java`, `apis-python`, `uis-dotNET`, `uis-java`, `uis-python`. |

**Which AI tool runs the review.** The first rule that applies wins:

1. `--tool claude` or `--tool copilot`.
2. The `COMPLIANCE_TEST_TOOL` environment variable.
3. Started from the Claude Code chat (CLI or VS Code extension): Claude.
4. Started from anywhere else in VS Code, such as GitHub Copilot Chat's agent mode: GitHub Copilot. This also applies when you type the command yourself in a VS Code terminal, so pass `--tool` there if you want Claude.
5. Otherwise: Claude.

**What runs.** Both tools run with the `compliance-reviewer_any-ai` folder as the working directory and write the usual `transitions/<runId>/` and `docs/reports/` files.

- **Claude:** `claude -p "/compliance-reviewer test/<kind>/<lang> --subjects all --programmatic --output file --out-file <results>/<app>-report.md" --output-format json --allowedTools "…"`. The test clears the calling Claude Code session's environment variables so the nested run starts cleanly. It also passes its own list of allowed tools, so the workspace doesn't need to be trusted for `.claude/settings.json` to apply headlessly.
- **Copilot:** `copilot -p "Follow the instructions in .github/prompts/compliance-review.prompt.md exactly. User input: <same arguments>" --allow-all-tools`. `--allow-all-tools` lets Copilot run any command without asking; the reviewer's own rules keep the target read-only.

### How a test is scored

The test reads the run's transition files (`transitions/<runId>/`), not the Markdown report.

- **A flaw is found** when a finding cites one of the flaw's expected checks with evidence in one of the flaw's files, the same rule as the answer key below. "Whole app" flaws (A12, U11, U12) accept any location, and for A12/U12 any Testing check (`TST-*`) counts. Findings are matched in the per-subject files (`NN-review-*.json`), before the reviewer merges duplicates across subjects, so a merged finding still counts.
- **Every other finding** in the final, deduplicated list (`90-aggregate.json`) is put in one of three groups:
  - **Incidental:** its check is listed under [Expected incidental findings](#expected-incidental-findings). Counted, not scored.
  - **Related:** it cites one of a flaw's expected checks, but in a different file. Reported only.
  - **Unexpected:** everything else. An unexpected **Error** fails the test; unexpected Warnings and Information findings are reported only.
- **A test passes** when the review completed, it found at least `--min-found` percent of the 12 flaws, and it has no unexpected Error findings. Missed flaws are always listed, but they fail the test only when they push the share found below the threshold.
- **Exit codes:** `0` pass, `1` fail, `2` error: the AI tool is missing, the app's build failed, the review failed or timed out, or the run couldn't be scored. `test_all.py` returns the worst code of the tests it ran.

### Results

Each run writes a folder under `test/logic/results/` (git-ignored), named `<timestamp>-<tool>` for a single test or `<timestamp>-<tool>-all` for `test_all.py`:

| File | Contents |
|------|----------|
| `<app>-result.md` | The verdict, a found/missed row per flaw with the finding IDs that matched, and tables of unexpected and related findings |
| `<app>-result.json` | The same data, for scripts |
| `<app>-report.md` | The reviewer's own scored report |
| `<app>-<tool>.log` | The AI tool's raw output and exit code, for troubleshooting |
| `summary.md`, `summary.json` | `test_all.py` only: one row per app |

The console shows the same result, ending with a one-line summary per app, for example `[PASS] apis-dotNET (claude): 11/12 flaws (92%, need 90%), missed: A9; unexpected errors: 0, unexpected warn/info: 2`.

### Notes

- **Running in parallel.** The reviewer names a run after the minute it started and the app's folder name, so `apis/dotNET` and `uis/dotNET` started in the same minute could get the same run ID. `test_all.py --parallel` therefore starts the three UI reviews 120 seconds after the three API reviews, and every test checks that its run reviewed its own app. Parallel runs also use model credit faster and may hit the tool's rate limits.
- **Comparing AI tools or languages.** Run `test_all.py` once per tool with the same `--min-found` and compare the two `summary.md` files, or compare the three apps of one kind within a single summary.
- **Re-scoring.** After you change the answer key or the scoring rules, use `--score-only transitions/<runId>` to score earlier runs again without another review.

## Answer key

The flaws are numbered so that the same number means the same flaw in every language. "Expected checks" lists the checklist IDs (from `compliance-reviewer/skills/review-*/references/checklist.md`) that should report the flaw. A flaw counts as found when a finding cites one of those checks, or an equivalent one, with evidence at the listed location. Some flaws can reasonably be reported under more than one check, and the aggregator may merge them.

### APIs

| # | Flaw | Expected checks | C# ([apis/dotNET](apis/dotNET)) | Java ([apis/java](apis/java)) | Python ([apis/python](apis/python)) |
|---|------|-----------------|------|------|--------|
| A1 | Hard-coded API key in configuration in the source tree | SEC-OP-05, SEC-OP-06, TF-03 | `appsettings.json` `ApiKey` | `application.properties` `api.key` | `config.py` `API_KEY` |
| A2 | API key sent in the query string (`?key=`), over plain HTTP | SEC-WA-10, SEC-IA-11 | `Program.cs` `MapDelete` | `TodoController.delete` | `main.py` `delete_todo` |
| A3 | No authentication on create/read/update; only DELETE checks the key, and that check is hand-rolled (not deny-by-default) | SEC-IA-01, SEC-IA-02, SEC-IA-07 | `Program.cs` endpoints | `TodoController` | `main.py` endpoints |
| A4 | No input validation (null, empty, unbounded title); the whole model is bound, including `id` (over-posting) | SEC-II-01 | `Program.cs` `MapPost`/`MapPut`, `TodoItem.cs` | `TodoController.create`/`update` | `main.py` `TodoItem`, `create_todo`/`update_todo` |
| A5 | Exception details and stack traces returned to the client (a null title causes a 500 with the full trace) | SEC-OP-01, SEC-OP-07, OBS-09 | `Program.cs` inline middleware writes `ex.ToString()` | `ErrorHandler.java`; `server.error.include-stacktrace=always` | `main.py` `handle_error`; `FastAPI(debug=True)` |
| A6 | CORS allows any origin, method and header | SEC-WA-05 | `Program.cs` `AllowAnyOrigin` | `@CrossOrigin(origins = "*")` | `CORSMiddleware(allow_origins=["*"])` |
| A7 | Logs built by string concatenation with user input (log injection, unstructured) and the API key written to the log | SEC-OP-03, SEC-OP-04, OBS-01 | `Program.cs` `logger.LogInformation("..." + ...)` | `TodoController` `logger.info("..." + ...)` | `main.py` `logger.info("..." + ...)` |
| A8 | Unsynchronized static/global mutable state used as the data store (not thread-safe, not stateless) | DP-01, TF-06, REL-05 | `TodoStore.cs` | `TodoController` static `items`/`nextId` | `main.py` global `todos`/`next_id` |
| A9 | Wrong status codes and no consistent error shape: create returns 200 instead of 201; "not found" returns 200 with an `error` body | API-05, API-09 | `Program.cs` | `TodoController` | `main.py` |
| A10 | Floating dependency version | DEP-01, DEP-02 | `TodoApi.csproj` `Swashbuckle.AspNetCore Version="*"` | `pom.xml` springdoc `[3.0.0,)` | `requirements.txt` (no versions at all) |
| A11 | API explorer / debug features enabled in every environment | SEC-OP-07 | `Program.cs` `UseSwagger`/`UseSwaggerUI` without an environment check | springdoc enabled by default; stack traces always on | `debug=True`, `reload=True`, bound to `0.0.0.0` |
| A12 | No automated tests | TST-07 (and other TST checks N/A or failed) | whole app | whole app | whole app |

### UIs

| # | Flaw | Expected checks | C# ([uis/dotNET](uis/dotNET)) | Java ([uis/java](uis/java)) | Python ([uis/python](uis/python)) |
|---|------|-----------------|------|------|--------|
| U1 | Stored XSS: to-do titles rendered without encoding | SEC-II-08 | `Pages/Index.cshtml` `@Html.Raw(item.Title)` | `templates/index.html` `th:utext` | `templates/index.html` `\|safe` |
| U2 | No CSRF protection on state-changing forms | SEC-IA-05 | `Pages/Index.cshtml.cs` `[IgnoreAntiforgeryToken]` | no CSRF protection configured (no Spring Security) | no CSRF protection (no Flask-WTF or equivalent) |
| U3 | Hard-coded admin password (and, in Python, a hard-coded Flask `SECRET_KEY`) | SEC-OP-05, SEC-OP-06, TF-03 | `appsettings.json` `AdminPassword` | `application.properties` `admin.password` | `app.py` `ADMIN_PASSWORD`, `SECRET_KEY` |
| U4 | Admin password sent in the query string to a state-changing GET, compared in plain text, with no authentication, authorization, throttling or audit | SEC-WA-10, SEC-IA-01, SEC-IA-02, SEC-IA-07, SEC-IA-09, API-09 | `Index.cshtml.cs` `OnGetClear`; `Program.cs` (no authentication or authorization configured) | `TodoController.clear` | `app.py` `clear` |
| U5 | Open redirect: the user-supplied return URL is redirected to without validation | SEC-IA-04, SEC-II-01 | `Index.cshtml.cs` `OnPostAdd` `Redirect(returnUrl)` | `TodoController.add` `"redirect:" + returnUrl` | `app.py` `add` `redirect(request.form.get("return_url"))` |
| U6 | Detailed error pages / debug mode always on | SEC-OP-01, SEC-OP-07 | `Program.cs` `UseDeveloperExceptionPage()` unconditionally; no HTTPS redirection or HSTS | `server.error.include-stacktrace=always` | `app.run(debug=True, host="0.0.0.0")` (Werkzeug debugger) |
| U7 | Unsynchronized static/global mutable state used as the data store | DP-01, TF-06, REL-05 | `IndexModel` static `Items`/`nextId` | `TodoController` static `items`/`nextId` | `app.py` global `items`/`next_id` |
| U8 | Exception silently swallowed (invalid priority ignored) | SEC-OP-02, SQ-06 | `OnPostAdd` empty `catch { }` | `add` empty `catch (Exception e)` | `add` `except Exception: pass` |
| U9 | App writes its own log file instead of a stdout event stream; log lines are concatenated with user input | TF-11, SEC-OP-04, OBS-01 | `File.AppendAllText("todo-ui.log", ...)` | `logging.file.name=todo-ui.log` | `logging.basicConfig(filename="todo-ui.log")` |
| U10 | Commented-out code | SQ-08 | `OnPostComplete` | `complete` | `complete` |
| U11 | No security headers (CSP, frame-ancestors, nosniff and so on) | SEC-WA-01, SEC-WA-03, SEC-WA-04, SEC-WA-11 | whole app | whole app | whole app |
| U12 | No automated tests | TST-07 (and other TST checks N/A or failed) | whole app | whole app | whole app |

### Expected incidental findings

These come from keeping the apps minimal rather than from seeded flaws. Expect them in every review; don't score them as false positives:

- **Maintainability:** no per-app README, contributing guide, change log, license or architecture docs (MAINT-01, 03, 06, 07, 08, 10).
- **Software Lifecycle:** no CI pipeline, release automation, branch protection, `SECURITY.md` or static analysis (SL-01, 02, 04, 05, 07, 11).
- **Dependency Management:** no lock file, SBOM or automated update configuration (DEP-02, DEP-05, DEP-07), in every app, including the UIs. The APIs also have no package-source configuration (`nuget.config`, Maven mirror settings, pip index or hash pinning) (DEP-08).
- **Observability:** no correlation IDs, tracing, metrics, telemetry export or SLOs (OBS-02 to OBS-08). The APIs' `/health` endpoint is shallow, and the UIs have none. In the APIs, the log level may be hard-coded rather than configurable (OBS-10).
- **Security, web:** no HTTPS enforcement or HSTS (SEC-WA-02, SEC-WA-06), and default `Server` headers (SEC-WA-07). The APIs also don't send `X-Content-Type-Options: nosniff` (SEC-WA-03); in the UIs that is part of U11.
- **Security, APIs only:** these follow from seeded flaws but use other checks:
  - the DELETE key check has no throttling, lockout or failure logging (SEC-IA-09, next to A3);
  - the error handler returns the exception without logging it server-side (SEC-OP-02, next to A5);
  - unbounded, user-supplied titles are written to the log (SEC-OP-09, next to A4 and A7).
- **Security, UIs only:** the admin clear-all action and added to-dos are logged with raw file writes rather than through the logging framework (SEC-OP-08, next to U4 and U9).
- **Coding standards:** public types and members have no documentation comments (CS-04). In the UIs, log lines may be flagged for string concatenation instead of the language's preferred formatting, such as C# interpolation (CS-05, next to U9).
- **Architecture patterns:** in the APIs, each handler builds its own "not found" response instead of using a shared helper or central error mapping (AP-06, next to A9); in the UIs, each handler writes the log file itself instead of using a shared logger (AP-06, next to U9).
- **API design (APIs only):** no committed OpenAPI file (the spec is generated at run time), no versioning, no pagination, sequential integer IDs rather than opaque ones, no request-ID header or machine-readable error code, no ETags and no correlation headers (API-01, 06, 07, 10, 11, 14, 15). The UIs should be N/A for API design, or reviewed only for their form endpoints.
- **Reliability and Performance:** mostly N/A, because the apps have no remote dependencies. The in-memory store and single instance may show up under REL-05 and PERF-08, and the APIs' linear scans of the in-memory list for get, update and delete under PERF-05.
- **Disaster Recovery, Monitoring, Cost & Sustainability:** N/A, because there is no infrastructure as code.

### Checking the flaws by hand

Every flaw above was checked by running the apps:

- Each API creates, lists and deletes to-dos. DELETE without the key returns 401, and with `?key=todo-api-key-7f3c9e2a1b` it succeeds. A missing to-do returns 200 with an `error` body. `POST /todos` with `{}` returns 500 with a stack trace.
- Each UI posts `title=<b>hi</b>` and renders it as live HTML, ignores an invalid priority, and redirects to an external `returnUrl` / `return_url`.
- The C# and Java Swagger UIs return 200.
