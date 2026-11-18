"""comp-review-api: an HTTP API over the Compliance Reviewer's headless reviewer and validation testers.

Run it with ``python run.py`` (from the ``api`` folder); the Swagger UI is at ``/swagger``."""

from __future__ import annotations

import logging
import platform
import shutil
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Literal

from fastapi import APIRouter, FastAPI, File, Form, HTTPException, Query, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse, Response

from . import commands
from .archive import ArchiveError, UploadTooLarge, remove_tree
from .commands import ReviewOptions, TesterOptions
from .config import Settings, load_settings
from .jobs import JobKind, JobManager
from .schemas import (AboutResponse, ErrorResponse, HealthResponse, JobDetail, JobSummary, TesterInfo,
                      TesterRunRequest, ToolInfo)
from .services import ConflictError, Services

log = logging.getLogger("comp_review_api")

TesterName = Enum("TesterName", {t.name.replace("-", "_"): t.name for t in commands.TESTER_DEFINITIONS}, type=str)

DESCRIPTION = """
HTTP API for the **Compliance Reviewer**.

* **Reviews** — upload a zip of an application's source code; the API unzips it into a temporary folder and
  runs `scripts/run_review.py` against it as a background job.
* **Jobs** — poll a job for its status and console output; when it finishes, its result holds the
  Markdown report (and, for testers, the test result).
* **Testers** — run the validation tests in `test/logic/` against the built-in sample apps
  (switched off when `Environment` is `production`).

Reviews and testers use model credit and take several minutes each.
"""

TAGS = [
    {"name": "About", "description": "Version, configuration and health."},
    {"name": "Reviews", "description": "Start a compliance review of uploaded source code."},
    {"name": "Jobs", "description": "Status, output and results of reviewer and tester jobs."},
    {"name": "Testers", "description": "Validation tests of the reviewer against the sample apps in `test/`."},
]

_ERRORS = {400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}


def _services(request: Request) -> Services:
    return request.app.state.services


def _tool_info() -> list[ToolInfo]:
    tools = []
    for name in ("claude", "copilot"):
        path = shutil.which(name)
        tools.append(ToolInfo(name=name, found=bool(path), path=path))
    return tools


# ---------------------------------------------------------------------- about / health

about_router = APIRouter(tags=["About"])


@about_router.get("/api/about", response_model=AboutResponse, summary="Reviewer version and API configuration")
def about(request: Request) -> AboutResponse:
    s = _services(request).settings
    return AboutResponse(reviewer_version=commands.reviewer_version(s), environment=s.environment,
                         python_version=platform.python_version(), tools=_tool_info(),
                         subjects=commands.list_subjects(s), configuration=s.public_dict())


@about_router.get("/api/health", response_model=HealthResponse, summary="Health check",
                  responses={503: {"model": HealthResponse, "description": "The API can't run reviews."}})
def health(request: Request) -> Response:
    s = _services(request).settings
    checks = {"reviewerScript": s.reviewer_script.is_file()}
    details: dict[str, str] = {}
    try:
        s.work_path.mkdir(parents=True, exist_ok=True)
        probe = s.work_path / ".health"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        checks["workDir"] = True
    except OSError as e:
        checks["workDir"] = False
        details["workDir"] = str(e)
    checks["aiTool"] = any(t.found for t in _tool_info())
    if not checks["reviewerScript"]:
        details["reviewerScript"] = f"not found: {s.reviewer_script}"
    if not checks["aiTool"]:
        details["aiTool"] = "neither the claude nor the copilot CLI is on PATH"
    if not (checks["reviewerScript"] and checks["workDir"]):
        state, code = "unhealthy", status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        state, code = ("healthy" if checks["aiTool"] else "degraded"), status.HTTP_200_OK
    body = HealthResponse(status=state, checks=checks, details=details)
    return JSONResponse(body.model_dump(by_alias=True), status_code=code)


# ---------------------------------------------------------------------- reviews

review_router = APIRouter(tags=["Reviews"])


@review_router.post("/api/reviews", status_code=status.HTTP_202_ACCEPTED, response_model=JobDetail,
                    summary="Review a zip of source code", responses={**_ERRORS, 413: {"model": ErrorResponse}},
                    description="Uploads a zip of the application's source, unzips it into a temporary folder and "
                                "starts `scripts/run_review.py` on it as a background job. Poll "
                                "`GET /api/jobs/{id}` for progress and the report.")
def start_review(
    request: Request,
    file: Annotated[UploadFile, File(description="Zip archive of the source code to review.")],
    tool: Annotated[Literal["auto", "claude", "copilot"] | None, Form(description="AI tool. Default: the DefaultTool setting.")] = None,
    model: Annotated[str | None, Form(description="Model for the AI tool. Default: the DefaultModel setting, else the tool's default.")] = None,
    subjects: Annotated[str, Form(description="`all`, or comma-separated subject names from `GET /api/about`.")] = "all",
    advanced: Annotated[bool, Form(description="Turn on advanced usage (IaC review and CLI analyzers).")] = False,
    analyzers: Annotated[str, Form(description="Analyzers to run when `advanced` is on.")] = "auto",
    timeout_min: Annotated[float | None, Form(alias="timeoutMin", description="Time limit in minutes. Default: the ReviewTimeoutMin setting.")] = None,
) -> JobDetail:
    svc = _services(request)
    s = svc.settings
    try:
        opts = ReviewOptions(
            tool=commands.validate_tool(tool, s.default_tool),
            model=commands.validate_model(model) or s.default_model,
            subjects=commands.validate_subjects(subjects, commands.list_subjects(s)),
            advanced=advanced,
            analyzers=commands.validate_analyzers(analyzers),
            timeout_min=commands.validate_timeout(timeout_min, s.review_timeout_min, 24 * 60),
        )
        if file.filename and not file.filename.lower().endswith(".zip"):
            raise ValueError("the upload must be a .zip file")
        job = svc.start_review(file.file, file.filename, opts)
    except UploadTooLarge as e:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, str(e)) from None
    except (ValueError, ArchiveError) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e)) from None
    return JobDetail.of(job)


# ---------------------------------------------------------------------- jobs

job_router = APIRouter(tags=["Jobs"])


def _job_or_404(request: Request, job_id: str):
    job = _services(request).jobs.get(job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"job {job_id} not found")
    return job


@job_router.get("/api/jobs", response_model=list[JobSummary], summary="List jobs, newest first")
def list_jobs(request: Request, kind: JobKind | None = None) -> list[JobSummary]:
    return [JobSummary.of(j) for j in _services(request).jobs.list(kind)]


@job_router.get("/api/jobs/{job_id}", response_model=JobDetail, responses=_ERRORS,
                summary="A job's status, recent output and result")
def get_job(request: Request, job_id: str,
            log_lines: Annotated[int, Query(alias="logLines", ge=0, le=5000,
                                            description="How many of the latest output lines to return.")] = 200
            ) -> JobDetail:
    return JobDetail.of(_job_or_404(request, job_id), log_lines)


@job_router.get("/api/jobs/{job_id}/report", response_class=PlainTextResponse, responses=_ERRORS,
                summary="The job's Markdown report",
                description="The reviewer's final report as `text/markdown`; 404 until the job has one.")
def get_report(request: Request, job_id: str) -> Response:
    job = _job_or_404(request, job_id)
    report = (job.result or {}).get("report")
    if not report:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"job {job_id} has no report ({job.status.value})")
    return Response(report, media_type="text/markdown; charset=utf-8",
                    headers={"Content-Disposition": f'inline; filename="{job.name}-compliance-review.md"'})


@job_router.post("/api/jobs/{job_id}/cancel", response_model=JobDetail, responses=_ERRORS,
                 summary="Cancel a queued or running job")
def cancel_job(request: Request, job_id: str) -> JobDetail:
    _job_or_404(request, job_id)
    job = _services(request).jobs.cancel(job_id)
    return JobDetail.of(job)


@job_router.delete("/api/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT,
                   responses={**_ERRORS, 409: {"model": ErrorResponse}},
                   summary="Delete a finished job and its files")
def delete_job(request: Request, job_id: str) -> Response:
    _job_or_404(request, job_id)
    if not _services(request).jobs.delete(job_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "the job is still queued or running; cancel it first")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------- testers

tester_router = APIRouter(tags=["Testers"])


def _tester_info(t: commands.TesterDefinition) -> TesterInfo:
    return TesterInfo(name=t.name, title=t.title, kind=t.kind, language=t.lang, script=f"test/logic/{t.script}")


@tester_router.get("/api/testers", response_model=list[TesterInfo], summary="List the validation testers")
def list_testers(request: Request) -> list[TesterInfo]:
    return [_tester_info(t) for t in commands.available_testers(_services(request).settings)]


@tester_router.post("/api/testers/{name}", status_code=status.HTTP_202_ACCEPTED, response_model=JobDetail,
                    responses={**_ERRORS, 409: {"model": ErrorResponse}}, summary="Run a validation tester",
                    description="Runs `test/logic/test_<kind>_<language>.py` as a background job: a fresh build of "
                                "the sample app, a full review, then scoring against the answer key. Poll "
                                "`GET /api/jobs/{id}`; the result holds the verdict, the test result and the report.")
def run_tester(request: Request, name: TesterName, body: TesterRunRequest | None = None) -> JobDetail:
    svc = _services(request)
    s = svc.settings
    body = body or TesterRunRequest()
    test = commands.TESTERS_BY_NAME[name.value]
    if not (s.tests_dir / test.script).is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"tester script not found: test/logic/{test.script}")
    try:
        opts = TesterOptions(
            tool=commands.validate_tool(body.tool, s.default_tool),
            model=commands.validate_model(body.model) or s.default_model,
            min_found=body.min_found,
            no_build=body.no_build,
            timeout_min=commands.validate_timeout(body.timeout_min, s.test_timeout_min, 24 * 60),
        )
        job = svc.start_tester(test, opts)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e)) from None
    except ConflictError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from None
    return JobDetail.of(job)


# ---------------------------------------------------------------------- app


def create_app(settings: Settings | None = None, jobs: JobManager | None = None) -> FastAPI:
    settings = settings or load_settings()
    jobs = jobs or JobManager(settings.max_concurrent_jobs, settings.max_retained_jobs)
    services = Services(settings, jobs)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Jobs live in memory, so folders left by an earlier process belong to no job.
        remove_tree(services.jobs_root)
        services.jobs_root.mkdir(parents=True, exist_ok=True)
        log.info("comp-review-api started: environment=%s, reviewer=%s", settings.environment, settings.root)
        yield
        jobs.shutdown()

    app = FastAPI(title="comp-review-api", version=commands.reviewer_version(settings) or "0.0.0",
                  description=DESCRIPTION, openapi_tags=TAGS, docs_url="/swagger", redoc_url=None,
                  lifespan=lifespan, swagger_ui_parameters={"displayRequestDuration": True, "tryItOutEnabled": True})
    app.state.services = services
    app.state.settings = settings
    if settings.cors_origins:
        app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"],
                           allow_headers=["*"], expose_headers=["Content-Disposition"])

    app.include_router(about_router)
    app.include_router(review_router)
    app.include_router(job_router)
    # In production the tester endpoints aren't registered at all: they're absent from the OpenAPI document and
    # Swagger UI, and a direct call gets 404 like any unknown path.
    if not settings.is_production:
        app.include_router(tester_router)

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse("/swagger")

    return app
