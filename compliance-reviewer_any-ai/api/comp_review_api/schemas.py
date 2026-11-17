"""Request and response models. JSON field names are camelCase."""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .jobs import Job, JobKind, JobStatus


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ToolInfo(ApiModel):
    name: str
    found: bool
    path: str | None = None


class AboutResponse(ApiModel):
    name: str = "comp-review-api"
    reviewer_version: str | None = Field(description="The Compliance Reviewer's version, from its VERSION file.")
    environment: Literal["development", "production"]
    python_version: str
    tools: list[ToolInfo] = Field(description="AI tool CLIs the reviewer can run, and whether each is on PATH.")
    subjects: list[str] = Field(description="Review subjects (skills) that can be passed in `subjects`.")
    configuration: dict[str, Any] = Field(description="The API's effective settings.")


class HealthResponse(ApiModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    checks: dict[str, bool]
    details: dict[str, str] = Field(default_factory=dict)


class TesterInfo(ApiModel):
    name: str = Field(examples=["api-dotnet"])
    title: str = Field(examples=["C# API"])
    kind: str = Field(examples=["apis"])
    language: str = Field(examples=["dotNET"])
    script: str = Field(examples=["test/logic/test_api_dotnet.py"])


class TesterRunRequest(ApiModel):
    tool: Literal["auto", "claude", "copilot"] | None = Field(
        None, description="AI tool to run the reviewer with. Default: the DefaultTool setting.")
    model: str | None = Field(None, description="Model passed to the AI tool. Default: the DefaultModel setting, "
                                                "else the tool's own default.", examples=["claude-sonnet-5-5"])
    min_found: float = Field(90, ge=0, le=100, description="Percent of the seeded flaws that must be found.")
    no_build: bool = Field(False, description="Skip the fresh build of the test app.")
    timeout_min: float | None = Field(None, gt=0, description="Review time limit in minutes. "
                                                              "Default: the TestTimeoutMin setting.")


class JobSummary(ApiModel):
    id: str
    kind: JobKind
    name: str
    status: JobStatus
    created_at: dt.datetime
    started_at: dt.datetime | None
    finished_at: dt.datetime | None
    duration_seconds: float | None
    error: str | None
    overall_score: float | None = None
    overall_band: str | None = None
    verdict: str | None = None

    @classmethod
    def of(cls, job: Job) -> "JobSummary":
        r = job.result or {}
        return cls(id=job.id, kind=job.kind, name=job.name, status=job.status, created_at=job.created_at,
                   started_at=job.started_at, finished_at=job.finished_at, duration_seconds=job.duration_s,
                   error=job.error, overall_score=r.get("overallScore"), overall_band=r.get("overallBand"),
                   verdict=r.get("verdict"))


class JobDetail(JobSummary):
    options: dict[str, Any]
    exit_code: int | None
    log: list[str] = Field(description="The most recent lines of the job's console output.")
    log_line_count: int
    result: dict[str, Any] | None = Field(
        description="Set when the job has finished. Reviews: status, runId, overallScore, overallBand, report "
                    "(Markdown) and the run summary. Testers: verdict, runId, scores, testResultMarkdown, report "
                    "(the reviewer's Markdown report) and the full testResult.")

    @classmethod
    def of(cls, job: Job, log_lines: int | None = 200) -> "JobDetail":
        base = JobSummary.of(job).model_dump()
        return cls(**base, options=job.options, exit_code=job.exit_code, log=job.log_tail(log_lines),
                   log_line_count=len(job.log), result=job.result)


class ErrorResponse(ApiModel):
    detail: str
