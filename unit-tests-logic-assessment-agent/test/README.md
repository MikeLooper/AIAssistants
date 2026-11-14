# Unit Test Coverage Reviewer test targets

Three very small to-do APIs, one each in C#, Java and Python, that serve as review targets for the [Unit Test Coverage Reviewer](../README.md). Each app ships with unit tests that have a **known set of deliberate coverage gaps** and a known set of paths that are properly tested. This README is the answer key: you can check what a review found, what it missed, what it wrongly flagged, and how consistent the results are across languages and AI tools.

## Layout

| App | Directory | Stack | Unit tests | Port |
|-----|-----------|-------|------------|------|
| C# API | [apis/dotNET](apis/dotNET) | .NET 10, ASP.NET Core minimal API | xUnit 2.9, Moq 4.20 ([TodoApi.Tests](apis/dotNET/TodoApi.Tests)) | 5300 |
| Java API | [apis/java](apis/java) | Java 25, Spring Boot 4.1.2 (Web MVC), Maven | JUnit 5, Mockito (`spring-boot-starter-test`) ([src/test](apis/java/src/test/java/com/example/todoapi)) | 8090 |
| Python API | [apis/python](apis/python) | Python 3.12+, FastAPI, Uvicorn | `unittest` + `unittest.mock`, standard library only ([tests](apis/python/tests)) | 8010 |

All three apps have the same design, so the same gap has the same number in every language:

| Unit | C# | Java (`src/main/java/com/example/todoapi/`) | Python |
|------|----|------|--------|
| Service (business rules; holds almost every gap) | `TodoApi/TodoService.cs` | `TodoService.java` | `todo_service.py` |
| Repository contract | `TodoApi/ITodoRepository.cs` | `TodoRepository.java` | `todo_repository.py` (`TodoRepository` protocol) |
| In-memory repository (fully tested) | `TodoApi/InMemoryTodoRepository.cs` | `InMemoryTodoRepository.java` | `todo_repository.py` (`InMemoryTodoRepository`) |
| API layer (no tests at all) | `TodoApi/Program.cs` | `TodoController.java` | `main.py` |
| Model, requests, errors | `TodoItem.cs`, `Exceptions.cs` | `TodoItem.java`, `TodoRequests.java`, `ValidationException.java`, `NotFoundException.java` | `models.py`, `errors.py` |
| Service tests | `TodoApi.Tests/TodoServiceTests.cs` | `src/test/.../TodoServiceTest.java` | `tests/test_todo_service.py` |
| Repository tests | `TodoApi.Tests/InMemoryTodoRepositoryTests.cs` | `src/test/.../InMemoryTodoRepositoryTest.java` | `tests/test_todo_repository.py` |

A to-do has an `id`, a `title`, a `priority` (1 to 5) and a completed flag. Data is kept in memory only.

- **Endpoints:** `GET /health`, `GET /todos?includeCompleted=&minPriority=` (Python: `include_completed`, `min_priority`), `GET /todos/{id}`, `POST /todos`, `PUT /todos/{id}/complete`, `PUT /todos/{id}/title`, `DELETE /todos/{id}`. Validation errors return 400 and unknown ids return 404.
- **Service methods** (C# PascalCase, Java camelCase, Python snake_case): `CreateTodo(title, priority)`, `CompleteTodo(id)`, `ListTodos(includeCompleted, minPriority)`, `DeleteTodo(id)`, `RenameTodo(id, newTitle)` and the static `PriorityLabel(priority)` (`low` for 1–2, `medium` for 3, `high` for 4–5, `unknown` otherwise).

Unlike the Compliance Reviewer test apps, these apps are not deliberately insecure; their only deliberate defects are in the unit tests.

## Running the apps and their unit tests

Prerequisites: .NET SDK 10, JDK 25 with Maven 3.9+, and Python 3.12+.

| App | Run the unit tests (from the app's directory) | Run the app |
|-----|----------------------------------------------|-------------|
| C# API | `dotnet test` | `dotnet run --project TodoApi`, then `http://localhost:5300/todos` |
| Java API | `mvn test` | `mvn spring-boot:run`, then `http://localhost:8090/todos` |
| Python API | `python -m unittest discover -s tests` (no packages needed) | `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python main.py`, then `http://localhost:8010/docs` |

Every unit test passes: 23 in C#, 23 in Java (JUnit counts each parameterized case) and 18 in Python. The gaps are in what the tests *don't* exercise or *don't* assert, not in failing tests.

If Maven fails with `PKIX path building failed` on a machine behind a TLS-inspecting proxy, set `MAVEN_OPTS=-Djavax.net.ssl.trustStoreType=Windows-ROOT` so Java uses the Windows certificate store.

[Directory.Build.props](Directory.Build.props) sends the MSBuild output (`bin/`, `obj/`) of every C# project under `test/` to `test/.build-output/`, so builds by you, the IDE or the test harness never put build output inside an app. The [.gitignore](.gitignore) excludes `bin/`, `obj/`, `target/`, `__pycache__/`, `.venv/`, `*.log` and `.build-output/`.

## Reviewing an app by hand

Point the reviewer at **one app directory**, not at `test/`, so that this answer key stays out of the review. In VS Code, select the **Unit Test Coverage Reviewer** agent and ask, for example:

- *"Review the unit test coverage of `test/apis/dotNET`"*
- *"Review the unit test coverage of `test/apis/python`"*

To compare languages, review all three apps with the same model. To compare AI tools or models, review the same app with each one. Then check the report against the [answer key](#answer-key).

## Answer key

### Seeded gaps

The reviewer should report each of these as a problem. "Expected" is the classification the [assertion-audit skill](../.github/skills/unit-test-coverage-test-assertion-audit/SKILL.md) should give; the automated tests accept either Uncovered or Partially Covered for G1–G9, because some of them sit on the line between the two (for example, an assertion that only checks "not null" may be judged weak or absent).

| # | Gap | Category | Expected | Why |
|---|-----|----------|----------|-----|
| G1 | `CreateTodo`: a title longer than 100 characters | Boundary | Uncovered | No test uses a long title, so the `Length > MaxTitleLength` guard never runs. |
| G2 | `CreateTodo`: `priority < 1 \|\| priority > 5` | Compound decision | Partially Covered (or the `> 5` half Uncovered) | Only priority `0` is tested; the `> 5` operand is never exercised. |
| G3 | `CompleteTodo`: unknown id throws not-found | Error branch | Uncovered | No test completes a missing id. |
| G4 | `CompleteTodo`: an already-completed item is returned unchanged | Weak assertion | Partially Covered | `CompleteTodo_AlreadyCompleted_ReturnsItem` (and its Java/Python twins) asserts only that the result is not null, not that it's unchanged. |
| G5 | `ListTodos`: the `minPriority` filter | Decision branch | Uncovered | Every test passes `null`/`None` (or omits it), so the filter never runs. |
| G6 | `DeleteTodo`: successful delete | Absent assertion | Uncovered | `DeleteTodo_ExistingItem_Deletes` calls the method and asserts nothing ("execution without verification"). |
| G7 | `PriorityLabel`: priority 3 → `medium` | Decision branch | Uncovered | The parameterized test covers 1, 2, 4 and 5 only. |
| G8 | `PriorityLabel`: default arm → `unknown` | Boundary | Uncovered | No out-of-range priority (0, 6, …) is tested. |
| G9 | `RenameTodo`: unknown id throws not-found | Mock bypass | Uncovered, flagged as a mock-bypass risk | The happy-path test mocks the repository to return an item for **any** id (`It.IsAny<int>()`, `anyInt()`, `Mock.return_value`), so the not-found branch can never run and the test would pass even if the lookup were broken. |
| G10 | The API layer has no unit tests | Unmapped unit | Uncovered (unit reported as unmapped) | `Program.cs` / `TodoController.java` / `main.py` and their 400/404 mappings are never tested. |

Locations: every gap except G10 is in the service file and its service test file (see [Layout](#layout)). G10 is the API-layer file.

### Control paths (should be Covered)

These paths are exercised and strongly asserted. Classifying one of them as Uncovered is a false positive.

| # | Path | Test (C# name; Java and Python have equivalent tests with names in their own style) |
|---|------|------|
| C1 | `CreateTodo`: blank title (null, empty, whitespace) throws a validation error | `CreateTodo_BlankTitle_ThrowsValidationException` (asserts type and message) |
| C2 | `CreateTodo`: valid input stores and returns the trimmed item | `CreateTodo_ValidInput_StoresTrimmedItem` |
| C3 | `CompleteTodo`: an open item is marked completed | `CompleteTodo_OpenItem_MarksItCompleted` |
| C4 | `ListTodos`: completed items are hidden unless `includeCompleted` is true | `ListTodos_Default_…`, `ListTodos_IncludeCompleted_…` (assert ids and order) |
| C5 | `DeleteTodo`: an unknown id throws not-found | `DeleteTodo_MissingItem_ThrowsNotFoundException` (asserts the id) |
| C6 | `PriorityLabel`: 4 and 5 return `high` | `PriorityLabel_ReturnsLabel` |
| C7 | Repository `FindById`: an unknown id returns null / empty `Optional` / `None` | `FindById_MissingItem_ReturnsNull` |

The rest of the in-memory repository (`Add`, `All`, `Remove`) and `RenameTodo`'s blank-title guard are also fully tested.

### Expected other findings (not scored)

These follow from keeping the apps small rather than from seeded gaps. Expect them in a review; they are listed in the result file but don't affect the verdict:

- **`RenameTodo` happy path** may be Partially Covered because of the same any-id mock as G9. (In the first Claude run the reviewer considered the mock and decided not to flag it. It still reported G9's branch as Uncovered, which is enough for the gap to count.)
- **`RenameTodo` null title**: the blank-title test passes only `" "`, so a reviewer that splits `null` and whitespace into separate paths reports the `null` path as Uncovered.
- **Empty collections**: `ListTodos` and the repository's `All` on an empty repository aren't tested.
- **Model, request and exception types**: properties, constructors and `ToString`-style members are only exercised indirectly (the agent's scope includes properties and constructors). Expect some of them to be listed as Uncovered or Partially Covered, mainly in the C# auto-properties, the Java getters and setters, `NotFoundException.Id`/`getId()`/`todo_id`, and the request types (C# and Java records, Python Pydantic models).
- **`ListTodos` sort order** (`OrderByDescending(Priority).ThenBy(Id)`): the tie-break on id is never tested with two items of the same priority, so a strict review may call it Partially Covered.
- **`CreateTodo` trimming**: a title with only internal whitespace, or exactly 100 characters, isn't tested; a strict review may list these as boundary cases next to G1.
- **API layer**: every endpoint path (each 200/201/204/400/404 branch) is Uncovered as part of G10, and `/health` and the app entry point (`TodoApiApplication.main`, the `if __name__ == "__main__"` block) may be listed too.
- **Repository contract** (`ITodoRepository`, `TodoRepository`): an interface/protocol with no logic, which may be listed with 0 paths.

## Automated validation

The scripts in [logic/](logic) do the review-and-compare work for you. Each test runs the Unit Test Coverage Reviewer **headlessly** (no chat, no questions) against one app, scores the run against the answer key above, and reports a pass or fail verdict.

> Each test is a full review: it uses model credit and takes several minutes per app.

### The tests

| Script | App | Answer key |
|--------|-----|------------|
| [logic/test_api_dotnet.py](logic/test_api_dotnet.py) | C# API ([apis/dotNET](apis/dotNET)) | G1–G10, C1–C7 |
| [logic/test_api_java.py](logic/test_api_java.py) | Java API ([apis/java](apis/java)) | G1–G10, C1–C7 |
| [logic/test_api_python.py](logic/test_api_python.py) | Python API ([apis/python](apis/python)) | G1–G10, C1–C7 |
| [logic/test_all.py](logic/test_all.py) | All three, one after another (default) or at the same time (`--parallel`) | all |
| [logic/selftest_harness.py](logic/selftest_harness.py) | No app: offline checks of the Markdown scorer and the answer-key file (no AI run, no cost) | — |

The shared logic is in [logic/harness.py](logic/harness.py). [logic/answer_key.json](logic/answer_key.json) is the machine-readable copy of the answer-key tables. When you change an app, a gap or a control, change that file too and run the self-test: it checks that every file the key names exists, that every method name it uses appears in the source, that the "never tested" gaps G5, G7 and G8 really are absent from the tests, and that the scorer gets a perfect score from a model stage-3 audit in each language.

### Prerequisites

- Python 3.10+ (standard library only; nothing to install).
- The CLI of the AI tool you test with, signed in:
  - **Claude Code**: `claude`.
  - **GitHub Copilot CLI**: `copilot` (`npm install -g @github/copilot`). The `copilot` shim that VS Code puts on the path isn't enough on its own.
- The app's build tools on the path, because each test builds the app and runs its unit tests first (see [Fresh build](#fresh-build)): the .NET SDK (`dotnet`) for C# and Maven (`mvn`) with a JDK for Java. The Python app needs only the Python that runs the test. Pass `--no-build` to skip this step when a tool isn't installed. The first C# and Java builds download packages from NuGet and Maven Central.

### Fresh build

Before each review, a test:

1. deletes any old build output in the app (`bin/`, `obj/`, `target/`, `__pycache__/`, `.venv/`),
2. copies the app to `build/<app>` in the results folder, builds the copy and runs its unit tests:
   - C#: `dotnet test --nologo -v q`
   - Java: `mvn -B -q clean verify`. On Windows, if `MAVEN_OPTS` doesn't already set a trust store, the test adds `-Djavax.net.ssl.trustStoreType=Windows-ROOT` (see the proxy note above).
   - Python: `python -m compileall -q .`, then `python -m unittest discover -s tests`,
3. deletes the copy.

This proves that the suites compile and pass as they are now, so a gap the reviewer reports is a real gap and not a broken test. Building a copy keeps build output out of the folder being reviewed. Just before the review starts, the test checks the app again and deletes any build output that has come back (for example, from IDE tooling), up to 5 times.

If the build or a unit test fails, the test stops with an error (exit code 2) before any AI cost. The output is in `<app>-build.log` next to the result. With `--no-build`, step 1 still runs and steps 2 and 3 are skipped.

### Running the tests

Run from the `unit-tests-logic-assessment-agent` folder:

```powershell
python test/logic/test_api_dotnet.py                          # one app, AI tool chosen automatically
python test/logic/test_api_java.py --tool copilot             # one app with GitHub Copilot
python test/logic/test_api_python.py --min-found 80           # require only 80% of the gaps
python test/logic/test_api_java.py --model claude-sonnet-5-5  # pick the model
python test/logic/test_all.py                                 # all three, one after another
python test/logic/test_all.py --parallel --tool claude        # all three at the same time
python test/logic/test_all.py --only dotNET,python            # a subset
python test/logic/test_api_java.py --dry-run                  # show the commands, don't run them
python test/logic/test_api_java.py --score-only 20261114-153000                                  # score an existing run (no AI cost)
python test/logic/test_api_java.py --score-only transitions/03-assertion-audit-20261114-153000.md  # same, by artifact path
cd test/logic; python -m unittest selftest_harness            # offline self-tests
```

Common options (every script; run any script with `--help` for the full list):

| Option | Default | What it does |
|--------|---------|--------------|
| `--tool auto\|claude\|copilot` | `auto` | AI tool that runs the review (see below). Also settable with the `COVERAGE_TEST_TOOL` environment variable. |
| `--min-found PCT` | `90` | Share of the 10 seeded gaps that must be found for a pass (90% means 9). Also `COVERAGE_TEST_MIN_FOUND`. |
| `--timeout MIN` | `60` | Time limit for each review, in minutes. Also `COVERAGE_TEST_TIMEOUT_MIN`. |
| `--progress SEC` | `30` | While a review runs, print a line each time a stage artifact appears in `transitions/`, plus a "still running" heartbeat every SEC seconds. `0` turns progress output off. Also `COVERAGE_TEST_PROGRESS_SEC`. |
| `--model NAME` | tool default | Model, passed to the tool's `--model` option. The agent file's `model:` list is a VS Code setting and isn't used headlessly. |
| `--tool-arg ARG` | none | Extra argument for the AI tool's CLI; repeat it for more, e.g. `--tool-arg=--max-budget-usd --tool-arg=5`. |
| `--results-dir DIR` | `test/logic/results` | Where results are written. |
| `--no-build` | off | Skip the fresh build and unit-test run. Old build output is still deleted. |
| `--build-timeout MIN` | `15` | Time limit for each build command, in minutes. Also `COVERAGE_TEST_BUILD_TIMEOUT_MIN`. |
| `--dry-run` | off | Print the commands that would run, then stop. |
| `--score-only RUN` | — | Single-app scripts only: skip the review and score an existing run, given its Run ID (looked up in `transitions/` and `docs/`) or the path of any of its artifacts. |
| `--parallel`, `--only APPS` | serial, all three | `test_all.py` only. App names are `dotNET`, `java`, `python` (`apis-dotNET` and so on also work). |

**Which AI tool runs the review.** The first rule that applies wins:

1. `--tool claude` or `--tool copilot`.
2. The `COVERAGE_TEST_TOOL` environment variable.
3. Started from the Claude Code chat (CLI or VS Code extension): Claude.
4. Started from anywhere else in VS Code, such as GitHub Copilot Chat's agent mode: GitHub Copilot. This also applies when you type the command yourself in a VS Code terminal, so pass `--tool` there if you want Claude.
5. Otherwise: Claude.

**What runs.** Both tools run with the `unit-tests-logic-assessment-agent` folder as the working directory, so the agent writes its usual `transitions/` and `docs/` files there. The test chooses the Run ID (`YYYYMMDD-HHmmss`, unique even for parallel runs) and passes it in the request, so it knows which artifacts belong to the run. The request names the app folder as the scope, tells the agent not to ask questions, and asks it to give every logical path its own row in the stage-3 tables, with the method named in the row or the table heading, so that the tables can be scored.

- **Claude:** `claude -p "Act as the agent defined in .github/agents/unit-test-coverage-reviewer.agent.md … read each skill file before you run its stage … <request>" --output-format json --allowedTools "Read,Grep,Glob,Write,Edit,TodoWrite,Task,Agent"`. Claude Code doesn't load `.github/agents` or `.github/skills` by itself, so the prompt points it at those files. The allowed tools match the agent's `read`, `search` and `edit` tools. The test clears the calling Claude Code session's environment variables so the nested run starts cleanly.
- **Copilot:** `copilot -p "<request>" --agent unit-test-coverage-reviewer --add-dir <agent folder> --trust-folder --allow-all-tools --no-ask-user`. `--agent` selects the custom agent, and `--add-dir` loads this folder's `.github/agents` and `.github/skills` (the git repository root is the parent folder, which has no agents of its own). `--allow-all-tools` lets Copilot run any tool without asking; the agent's own rules keep the target read-only.

### How a test is scored

The agent writes Markdown, not JSON, so the test parses the tables in the run's stage-3 audit, `transitions/03-assertion-audit-<runId>.md`.

- **Each table row is placed.** Its *unit* is the nearest heading that names a source file or class, or else the row itself. In a `<source> vs <tests>` heading only the source side counts, so `` `errors.py` vs `tests/test_todo_service.py` `` isn't the service. Its *method* comes from a method heading below or at the unit heading (for example ``### Method: `TodoService.create_todo` ``); if there is none, it comes from the row's cells. Its *classification* is the Classification column (Covered, Partially Covered or Uncovered).
- **A gap is found** when a row has the gap's unit and method, its condition matches the gap's patterns (for example G7 needs `medium` or `3`), and it is classified as one of the gap's accepted classes. Patterns are matched against the Path ID, Condition, Outcome and Classification cells only. Test names, assertion strength and notes are ignored, because a note like "no test uses a non-blank title" would otherwise mislead them. G10 is also found when the stage-1 mapping marks the API file as having no test suite. If no audit row matches at all, the test looks in the final report's tables instead.
- **A control is checked** the same way. If its rows are classified only Uncovered, it is a **false positive**. Rows classified only Partially Covered make it *disputed*, which is reported but doesn't fail the test.
- **Every other** Uncovered or Partially Covered row is listed under "Other problems reported (not scored)", for tuning the answer key. Compare it with [Expected other findings](#expected-other-findings-not-scored).
- **A test passes** when the run produced its stage-3 audit, at least `--min-found` percent of the 10 gaps were found, and no control path is a false positive. A missing final report is reported as a warning.
- **Exit codes:** `0` pass, `1` fail, `2` error: the AI tool is missing, the build or unit tests failed, the review timed out or produced no stage-3 audit, or the run names another target. `test_all.py` returns the worst code of the tests it ran.

The patterns behind each gap and control are in [logic/answer_key.json](logic/answer_key.json). They are deliberately tolerant of wording (`not found`, `missing`, `null`, `NotFoundException`, …). If a review clearly reports a gap but the test calls it "not located", look at the "Matching row" column of the result and widen the pattern; `--score-only` then re-scores the same run at no cost.

### Results

Each run writes a folder under `test/logic/results/` (git-ignored), named `<timestamp>-<tool>` for a single test or `<timestamp>-<tool>-all` for `test_all.py`:

| File | Contents |
|------|----------|
| `<app>-result.md` | The verdict; a row per gap and per control with its result, the classification the reviewer gave and the row that matched; the reviewer's own metrics (total paths, problems, problem percentage, severity breakdown); and the other problems it reported |
| `<app>-result.json` | The same data, for scripts |
| `<app>-artifacts/` | Copies of the run's manifest, stage 1–3 artifacts and final report |
| `<app>-<tool>.log` | The AI tool's command, raw output and exit code, for troubleshooting |
| `<app>-build.log` | The build and unit-test output |
| `summary.md`, `summary.json` | `test_all.py` only: one row per app |

The console shows the same result, ending with a one-line summary per app, for example `[PASS] apis-dotNET (claude): 10/10 gaps (100%, need 90%), missed: none; false positives: none; other problems reported: 9`.

The agent's own files stay where it writes them: `transitions/*-<runId>.md` and `docs/coverage-review-<runId>.md` in the `unit-tests-logic-assessment-agent` folder. They aren't git-ignored, so delete the ones you don't want to keep.

### Notes

- **Running in parallel.** Each test gets its own Run ID, so parallel runs can't overwrite each other's artifacts; `test_all.py --parallel` still starts the reviews 10 seconds apart. Parallel runs use model credit faster and may hit the tool's rate limits.
- **Comparing AI tools, models or languages.** Run `test_all.py` once per tool or model with the same `--min-found` and compare the `summary.md` files, or compare the three apps within one summary.
- **Re-scoring.** After you change the answer key or the scoring rules, use `--score-only <runId>` to score earlier runs again without another review.
