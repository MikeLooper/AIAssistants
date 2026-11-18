# comp-review-ui

An Angular web front end for [comp-review-api](../api/README.md). It starts compliance reviews of uploaded source code, runs the validation testers, follows jobs while they run, and shows the final report (and the test result for a tester). It runs on **port 12101**.

## Quick start

Prerequisites: Node.js 24+ and npm 11+, and comp-review-api running (by default at `http://localhost:12001`).

```powershell
cd compliance-reviewer_any-ai\webui
npm install
npm start                 # ng serve: http://localhost:12101
npm run build             # production build in dist/comp-review-ui/browser
```

To serve a build, host the files in `dist/comp-review-ui/browser` with any static web server, with unknown paths falling back to `index.html`, and add that server's origin to the API's `CorsOrigins` setting.

## Pages

| Page | What it does |
|------|--------------|
| **Review** | Pick the source, as a **zip file** or a **directory** (both through the browser's file dialogs), then choose the AI tool, the model (free text with suggestions from the API's `AvailableModels`), all or selected subjects, advanced usage and analyzers, and a time limit. A zip is uploaded as is. A directory is zipped in the browser first (with fflate), with the picked folder as the top-level folder, and uploaded as `<folder>.zip`. By default, build output, dependency and VCS folders (`.git`, `node_modules`, `bin`, `obj`, `target`, `dist`, `.venv`, `__pycache__` …) are left out, because they add findings that aren't about the source. The page shows upload progress, then opens the job. |
| **Testers** | Lists the nine validation testers. Run one, or select several and run them together (the API queues them). Options: tool, model, required share of flaws, skip build, time limit. Hidden in production. |
| **Jobs** | Every job the API holds, refreshed while you watch: status, verdict, score and duration. |
| **Job** | Live status and console output while the job runs, with a Cancel button. When it finishes, it shows the overall score, cost and duration, then the **test result** (testers) and the **compliance report**, rendered from Markdown with a toggle to the Markdown source and a download button. |
| **About** | This UI's settings, the API's health checks, the reviewer version, the AI tools found on the API host, and the API's full configuration. |

The header shows the environment and the API's health, which is checked every minute.

Browsers can only read files that the person picks in a file dialog, so a path typed into a text box can't be uploaded. That's why both sources use **Browse** dialogs. The directory dialog relies on `webkitdirectory`, which current versions of Chrome, Edge, Firefox and Safari support.

## Configuration

Settings are read at startup from [`public/config.json`](public/config.json) (served as `/config.json`). Edit that file, or the copy in a build's output folder, and reload the page; no rebuild is needed.

```json
{
  "environment": "development",
  "apiBaseUrl": "http://localhost:12001",
  "pollIntervalMs": 3000
}
```

| Key | Default | What it does |
|-----|---------|--------------|
| `environment` | `development` | `development` or `production`. Production hides the Testers page and its menu link (the route redirects to Review) and lists only review jobs. |
| `apiBaseUrl` | `http://localhost:12001` | Where comp-review-api runs. |
| `pollIntervalMs` | `3000` | How often running jobs and the job list are refreshed (at least 250). |

A missing or broken `config.json` leaves the defaults in place, and the About page says so. The UI's `environment` is separate from the API's `Environment`; set both to `production` for a production deployment.

The dev server port (12101) is set in `angular.json` (`serve.options.port`).

## Tests

```powershell
npm test                  # Vitest, once
npm run test:watch        # Vitest, watch mode
npm run test:coverage     # with a coverage report (coverage/)
```

There are 81 tests. They cover the config loader, the API client (form fields, upload progress, error messages), the browser zipping and folder filter, job polling, the production guard and routes, the shell, and every page, using Angular's `HttpTestingController` with no real API. Line coverage is about 99%.

## Layout

| Path | Role |
|------|------|
| `src/app/core/app-config.ts` | Loads and validates `config.json`; exposes the environment and API URL as signals. |
| `src/app/core/api.service.ts` | Typed client for every API endpoint, plus `errorMessage()` for readable errors. |
| `src/app/core/zip.ts` | Folder filter and in-browser zipping for directory uploads. |
| `src/app/core/job-poller.ts` | Polls a job until it finishes. |
| `src/app/core/production.guard.ts` | Blocks the tester route in production. |
| `src/app/features/` | The Review, Testers, Jobs, Job and About pages. |
| `src/app/shared/` | Markdown view, status badge, tool and model picker. |
| `src/app/testing/helpers.ts` | Test-only providers and fixtures. |
