"""Starts reviewer and tester jobs and turns their output files into job results."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, BinaryIO

from .archive import ArchiveError, extract_zip, remove_tree, safe_folder_name, save_upload
from .commands import (ReviewOptions, TesterDefinition, TesterOptions, review_command, tester_command)
from .config import Settings
from .jobs import Job, JobKind, JobManager, JobStatus, new_job_id

MB = 1024 * 1024
# Extra time the API allows past the script's own --timeout before it stops the process itself
# (covers the tester's build step and the script's own shutdown).
TIMEOUT_GRACE_S = 20 * 60
LOG_LINES_IN_ERROR = 8


class ConflictError(RuntimeError):
    """The request conflicts with a job that is already queued or running."""


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _read_text(path: Path | str | None) -> str | None:
    if not path:
        return None
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except OSError:
        return None


def _log_excerpt(job: Job) -> str:
    tail = [ln for ln in job.log_tail(LOG_LINES_IN_ERROR) if ln.strip()]
    return ("; last output: " + " | ".join(tail)) if tail else ""


class Services:
    def __init__(self, settings: Settings, jobs: JobManager):
        self.settings = settings
        self.jobs = jobs

    @property
    def jobs_root(self) -> Path:
        return self.settings.work_path / "jobs"

    # ------------------------------------------------------------------ reviews

    def start_review(self, stream: BinaryIO, filename: str | None, opts: ReviewOptions) -> Job:
        s = self.settings
        job_id = new_job_id()
        work = self.jobs_root / job_id
        zip_path = work / "upload.zip"
        try:
            size = save_upload(stream, zip_path, s.max_upload_mb * MB)
            target = extract_zip(zip_path, work / "source" / safe_folder_name(filename), s.max_extracted_mb * MB,
                                 s.max_extracted_files)
        except (ArchiveError, OSError):
            remove_tree(work)
            raise
        finally:
            zip_path.unlink(missing_ok=True)
        out_file, summary_file = work / "report.md", work / "summary.json"
        cmd = review_command(s, target, out_file, summary_file, opts)
        options = {**asdict(opts), "fileName": filename, "uploadBytes": size}
        return self.jobs.submit(JobKind.review, target.name, cmd, s.root, work, opts.timeout_min * 60 + TIMEOUT_GRACE_S,
                                lambda job: self.finalize_review(job, out_file, summary_file, work / "source"),
                                options=options, job_id=job_id)

    def finalize_review(self, job: Job, out_file: Path, summary_file: Path, source_dir: Path) -> JobStatus:
        summary = _read_json(summary_file) or {}
        report = _read_text(out_file) or _read_text(summary.get("docsReport"))
        job.result = {
            "status": summary.get("status"),
            "runId": summary.get("runId"),
            "overallScore": summary.get("overallScore"),
            "overallBand": summary.get("overallBand"),
            "docsReport": summary.get("docsReport"),
            "report": report,
            "summary": summary or None,
        }
        if not self.settings.keep_sources:
            remove_tree(source_dir)
        if job.exit_code == 0 and summary.get("status") == "completed":
            return JobStatus.completed
        job.error = (summary.get("error") or f"the reviewer exited with code {job.exit_code}") + _log_excerpt(job)
        return JobStatus.failed

    # ------------------------------------------------------------------ testers

    def start_tester(self, test: TesterDefinition, opts: TesterOptions) -> Job:
        s = self.settings
        busy = [j for j in self.jobs.list(JobKind.test) if j.name == test.name and not j.status.finished]
        if busy:
            raise ConflictError(f"tester {test.name} is already {busy[0].status.value} as job {busy[0].id}")
        job_id = new_job_id()
        work = self.jobs_root / job_id
        results_dir = work / "results"
        cmd = tester_command(s, test, results_dir, opts)
        return self.jobs.submit(JobKind.test, test.name, cmd, s.root, work, opts.timeout_min * 60 + TIMEOUT_GRACE_S,
                                lambda job: self.finalize_tester(job, test, results_dir),
                                options={**asdict(opts), "app": test.app, "script": test.script}, job_id=job_id)

    def finalize_tester(self, job: Job, test: TesterDefinition, results_dir: Path) -> JobStatus:
        result_file = next(iter(sorted(results_dir.rglob(f"{test.app}-result.json"))), None) if results_dir.is_dir() else None
        data = _read_json(result_file) if result_file else None
        if data is None:
            job.result = None
            job.error = f"the tester wrote no result (exit code {job.exit_code})" + _log_excerpt(job)
            return JobStatus.failed
        report_file = result_file.with_name(f"{test.app}-report.md")
        verdict = data.get("verdict")
        job.result = {
            "verdict": verdict,
            "runId": data.get("runId"),
            "overallScore": data.get("overallScore"),
            "overallBand": data.get("overallBand"),
            "testResultMarkdown": _read_text(result_file.with_name(f"{test.app}-result.md")),
            "report": _read_text(report_file) or _read_text(data.get("reportFile")),
            "testResult": data,
        }
        if verdict in ("pass", "fail"):
            return JobStatus.completed
        job.error = data.get("error") or f"the tester ended with verdict {verdict!r} (exit code {job.exit_code})"
        return JobStatus.failed
