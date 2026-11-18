# comp-review-api

An HTTP API for the Compliance Reviewer. It runs the headless reviewer ([`scripts/run_review.py`](../scripts/run_review.py)) on uploaded source code and runs the validation testers in [`test/logic/`](../test/logic). It's a FastAPI application with a Swagger UI, and it listens on **port 12001**.

The Angular Web UI in [`../webui`](../webui/README.md) is a front end for this API.

## Quick start

Prerequisites: Python 3.10+ and the CLI of the AI tool that runs reviews, signed in (Claude Code `claude`, or GitHub Copilot CLI `copilot`), the same as for `run_review.py`. The testers also need the sample apps' build tools (.NET 10, JDK 25 with Maven, Python 3.12+); see [test/README.md](../test/README.md).

```powershell
cd compliance-reviewer_any-ai\api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # requirements-dev.txt for the unit tests
python run.py                          # http://127.0.0.1:12001/swagger
```

`python run.py --port 12005 --host 0.0.0.0 --config my-settings.json --reload` overrides settings for one run. `/` redirects to `/swagger`; the OpenAPI document is at `/openapi.json`.

## How it works

Reviews take minutes, so every review or tester run is a **background job**:

1. `POST /api/reviews` (a zip) or `POST /api/testers/{name}` starts a job and returns `202` with the job at once.
2. Poll `GET /api/jobs/{id}`. It returns the status (`queued`, `running`, `completed`, `failed`, `cancelled`), the latest console lines of the script (its progress output), and, once the job has finished, its `result`.
3. When it finishes, `result.report` holds the reviewer's Markdown report (also at `GET /api/jobs/{id}/report`). For a tester, `result.testResultMarkdown` and `result.testResult` hold the test result, and `result.verdict` is `pass` or `fail`.

For a review, the API saves the upload, checks it and unzips it into `<WorkDir>/jobs/<jobId>/source/<zip name>/`. If the zip has one top-level folder (the usual result of zipping a folder), that folder is the target, so the report and run ID are named after it. The API then runs `run_review.py <target> --tool … --subjects … --out-file … --summary-json … --no-report` with the reviewer workspace (`compliance-reviewer_any-ai`) as the working directory. The extracted source is deleted when the job ends (unless `KeepSources` is on). As with any review, the transition files go to `transitions/<runId>/` and a copy of the report to `docs/reports/`.

At most `MaxConcurrentJobs` jobs run at a time; the rest wait as `queued`. Jobs live in memory: restarting the API forgets them and deletes their working folders. Only the newest `MaxRetainedJobs` finished jobs are kept.

**Choosing the AI model.** Every review and tester request takes an optional `tool` (`auto`, `claude` or `copilot`) and `model` (passed to the tool's `--model` option). Leave them out to use the `DefaultTool` and `DefaultModel` settings. With no `DefaultModel`, the tool uses its own default model. `AvailableModels` lists the models the Web UI suggests for each tool; you can still type any model name. Names are limited to letters, digits and `. _ : / [ ] -`, and can't start with `-`.

## Endpoints

| Method and path | What it does |
|-----------------|--------------|
| `GET /api/about` | Reviewer version (from `VERSION`), environment, Python version, whether `claude` and `copilot` are on PATH, the review subjects, and every effective setting. |
| `GET /api/health` | `healthy`, `degraded` (no AI tool CLI on PATH) or `unhealthy` (`503`: the reviewer script is missing or the work folder isn't writable), with the individual checks. |
| `POST /api/reviews` | Multipart form: `file` (a `.zip`, required), `tool`, `model`, `subjects` (`all` or comma-separated names from `/api/about`), `advanced` (`true`/`false`), `analyzers` (used with `advanced`), `timeoutMin`. Returns `202` and the job; `400` for a bad zip or value, `413` for an upload over `MaxUploadMb`. |
| `GET /api/jobs?kind=review\|test` | All jobs, newest first, without their console output. |
| `GET /api/jobs/{id}?logLines=200` | One job: status, options, exit code, the latest `logLines` console lines (0–5000) and its result. |
| `GET /api/jobs/{id}/report` | The report as `text/markdown`; `404` until the job has one. |
| `POST /api/jobs/{id}/cancel` | Cancels a queued job, or stops a running one together with the AI tool process it started. |
| `DELETE /api/jobs/{id}` | Forgets a finished job and deletes its files (`409` while it's queued or running). |
| `GET /api/testers` | The nine testers (`api-dotnet`, `api-java`, `api-python`, `ui-…`, `mcp-…`) and their scripts. |
| `POST /api/testers/{name}` | Runs `test/logic/test_<kind>_<language>.py`. JSON body (all optional): `tool`, `model`, `minFound` (0–100, default 90), `noBuild`, `timeoutMin`. Returns `202` and the job; `409` if that tester is already queued or running. |

**Production.** When `Environment` is `production`, the tester endpoints aren't registered at all. They're absent from `/openapi.json` and the Swagger UI, and a direct call to any `/api/testers` path gets `404 Not Found`, the same as an unknown path, so it doesn't reveal that they exist. No tester can be started in production.

Example with `curl`:

```powershell
curl -F "file=@myapp.zip" -F "tool=claude" -F "model=claude-sonnet-5-5" http://127.0.0.1:12001/api/reviews
curl http://127.0.0.1:12001/api/jobs/<id>
curl http://127.0.0.1:12001/api/jobs/<id>/report -o myapp-review.md
curl -X POST http://127.0.0.1:12001/api/testers/api-python -H "Content-Type: application/json" -d '{"noBuild": true}'
```

## Configuration

Settings come from [`appsettings.json`](appsettings.json), or from the file named by `--config` or `COMP_REVIEW_API_CONFIG`. Environment variables named `COMP_REVIEW_API_<SETTING_IN_UPPER_SNAKE_CASE>` override the file, for example `COMP_REVIEW_API_ENVIRONMENT=production` or `COMP_REVIEW_API_DEFAULT_MODEL=claude-opus-5-5`. In variables, lists are comma-separated and `AvailableModels` is JSON. An invalid or unknown setting stops the API at startup.

| Setting | Default | What it does |
|---------|---------|--------------|
| `Environment` | `development` | `development` or `production`. Production switches the tester endpoints off: they're absent from Swagger, and calls get 404. |
| `Host`, `Port` | `127.0.0.1`, `12001` | Where the API listens. |
| `DefaultTool` | `auto` | AI tool when a request names none: `auto` (`run_review.py`'s own detection), `claude` or `copilot`. |
| `DefaultModel` | none | Model when a request names none; none means the tool's own default. |
| `AvailableModels` | Claude and Copilot lists | Model suggestions per tool, shown by the Web UI. |
| `CorsOrigins` | the Web UI on port 12101 | Browser origins allowed to call the API. |
| `MaxUploadMb` | `200` | Largest upload accepted. |
| `MaxExtractedMb`, `MaxExtractedFiles` | `1000`, `50000` | Limits on the unzipped size and file count (zip-bomb protection). |
| `MaxConcurrentJobs` | `1` | Jobs that run at the same time. Keep `1` unless you need more: the reviewer names runs `<date-time to the minute>-<target>`, so two reviews of the same folder name started in the same minute would share a run ID. |
| `MaxRetainedJobs` | `50` | Jobs kept in memory; the oldest finished ones (and their files) are removed first. |
| `ReviewTimeoutMin`, `TestTimeoutMin` | `60`, `60` | Default time limits, passed to the scripts' `--timeout`. A request can set its own (`timeoutMin`). The API stops a job itself 20 minutes after that limit if the script hasn't ended. |
| `KeepSources` | `false` | Keep the unzipped source after a review (for debugging). |
| `WorkDir` | `<system temp>/comp-review-api` | Where uploads and job files go. Its `jobs` folder is emptied at startup. |
| `ReviewerRoot` | the folder above `api` | The reviewer workspace that holds `scripts/run_review.py`, `test/logic/` and `VERSION`. |

## Security notes

- The API has **no authentication** and binds to `127.0.0.1` by default. Every request can spend model credit, so don't expose it on a network without putting authentication in front of it.
- Uploaded archives are checked before anything is extracted: entries with absolute paths or `..`, symbolic links, too many files and too many bytes are refused, and the byte limit is enforced while extracting too, since zip headers can lie.
- Commands are built as argument lists, never shell strings. Model, subject and analyzer values are checked against strict patterns, so none can be read as another option of the AI tool.
- The reviewer's own rules keep the target read-only; the API also deletes the extracted copy after the review.

## Tests

```powershell
pip install -r requirements-dev.txt
python -m pytest                                        # 99 tests
python -m pytest --cov=comp_review_api --cov-report=term-missing
```

The tests never call an AI tool. [`tests/conftest.py`](tests/conftest.py) builds a throwaway reviewer workspace whose `run_review.py` and tester scripts are stand-ins ([`tests/fakes/`](tests/fakes)), so the real job runner, process handling, zip handling and endpoints run end to end. Statement coverage is about 97%; the gaps are POSIX-only process branches.

## Layout

| Path | Role |
|------|------|
| `run.py` | Entry point: loads the settings and starts Uvicorn. |
| `comp_review_api/main.py` | FastAPI app factory (`create_app`), routes and Swagger setup. |
| `comp_review_api/config.py` | Settings: defaults, `appsettings.json`, `COMP_REVIEW_API_*` variables, validation. |
| `comp_review_api/commands.py` | Tester catalog, input validation and the reviewer and tester command lines. |
| `comp_review_api/services.py` | Starts review and tester jobs and reads their output files into results. |
| `comp_review_api/jobs.py` | In-memory background job manager (queue, timeout, cancel, retention). |
| `comp_review_api/archive.py` | Upload saving and safe zip extraction. |
| `comp_review_api/process.py` | Starts child processes and stops whole process trees. |
| `comp_review_api/schemas.py` | Request and response models (camelCase JSON). |
