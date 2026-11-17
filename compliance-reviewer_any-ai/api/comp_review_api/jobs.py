"""Background jobs: one reviewer or tester run each, executed as a child process.

Reviews take minutes, so the API starts a job and returns at once; callers poll the job for its status, its
output so far and, at the end, its result. Jobs live in memory and are lost when the API restarts. At most
`max_concurrent` run at once (the rest wait as `queued`), and only the newest `max_retained` finished jobs
are kept, together with their working folders."""

from __future__ import annotations

import datetime as dt
import logging
import threading
import uuid
from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Sequence

from . import process
from .archive import remove_tree

log = logging.getLogger(__name__)

LOG_LINES = 5000


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

    @property
    def finished(self) -> bool:
        return self in (JobStatus.completed, JobStatus.failed, JobStatus.cancelled)


class JobKind(str, Enum):
    review = "review"
    test = "test"


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


@dataclass
class Job:
    id: str
    kind: JobKind
    name: str
    command: list[str]
    cwd: Path
    work_dir: Path
    timeout_s: float
    options: dict[str, Any] = field(default_factory=dict)
    status: JobStatus = JobStatus.queued
    created_at: dt.datetime = field(default_factory=_now)
    started_at: dt.datetime | None = None
    finished_at: dt.datetime | None = None
    exit_code: int | None = None
    error: str | None = None
    result: dict[str, Any] | None = None
    log: deque = field(default_factory=lambda: deque(maxlen=LOG_LINES))
    timed_out: bool = False
    cancel_requested: bool = False
    _proc: Any = None
    _future: Future | None = None

    @property
    def duration_s(self) -> float | None:
        if not self.started_at:
            return None
        return round(((self.finished_at or _now()) - self.started_at).total_seconds(), 1)

    def log_tail(self, lines: int | None) -> list[str]:
        items = list(self.log)
        return items if lines is None else items[-lines:] if lines > 0 else []


# A finalizer turns a finished process into the job's result. It sets job.result and returns the final
# status (completed or failed), setting job.error when it fails.
Finalizer = Callable[[Job], JobStatus]


class JobManager:
    def __init__(self, max_concurrent: int = 1, max_retained: int = 50, env: dict | None = None):
        self._pool = ThreadPoolExecutor(max_workers=max_concurrent, thread_name_prefix="job")
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        self._max_retained = max_retained
        self._env = env

    # ------------------------------------------------------------------ public API

    def submit(self, kind: JobKind, name: str, command: Sequence[str], cwd: Path, work_dir: Path,
               timeout_s: float, finalize: Finalizer, options: dict[str, Any] | None = None,
               job_id: str | None = None) -> Job:
        job = Job(id=job_id or new_job_id(), kind=kind, name=name, command=list(command), cwd=cwd,
                  work_dir=work_dir, timeout_s=timeout_s, options=options or {})
        with self._lock:
            self._jobs[job.id] = job
        job._future = self._pool.submit(self._run, job, finalize)
        self._prune()
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def list(self, kind: JobKind | None = None) -> list[Job]:
        with self._lock:
            jobs = list(self._jobs.values())
        jobs = [j for j in jobs if kind is None or j.kind == kind]
        return sorted(jobs, key=lambda j: j.created_at, reverse=True)

    def cancel(self, job_id: str) -> Job | None:
        job = self.get(job_id)
        if job is None or job.status.finished:
            return job
        job.cancel_requested = True
        if job._future is not None and job._future.cancel():  # still queued: never starts
            self._finish(job, JobStatus.cancelled, "cancelled before it started")
        elif job._proc is not None:
            process.kill_tree(job._proc)
        return job

    def delete(self, job_id: str) -> bool:
        """Forget a finished job and delete its working folder. Returns False if it isn't finished."""
        job = self.get(job_id)
        if job is None:
            return True
        if not job.status.finished:
            return False
        with self._lock:
            self._jobs.pop(job_id, None)
        remove_tree(job.work_dir)
        return True

    def wait(self, job_id: str, timeout: float | None = None) -> Job | None:
        """Block until the job finishes (used by tests)."""
        job = self.get(job_id)
        if job and job._future is not None:
            try:
                job._future.result(timeout=timeout)
            except Exception:  # cancelled futures raise; the job state says what happened
                pass
        return job

    def shutdown(self) -> None:
        for job in self.list():
            if not job.status.finished:
                self.cancel(job.id)
        self._pool.shutdown(wait=False, cancel_futures=True)

    # ------------------------------------------------------------------ execution

    def _run(self, job: Job, finalize: Finalizer) -> None:
        if job.cancel_requested:
            self._finish(job, JobStatus.cancelled, "cancelled before it started")
            return
        job.status = JobStatus.running
        job.started_at = _now()
        job.work_dir.mkdir(parents=True, exist_ok=True)
        try:
            job._proc = process.start(job.command, job.cwd, self._env)
        except OSError as e:
            self._finish(job, JobStatus.failed, f"could not start the process: {e}")
            return
        if job.cancel_requested:  # cancelled while the process was starting
            process.kill_tree(job._proc)
        timer = threading.Timer(job.timeout_s, self._on_timeout, args=(job,))
        timer.daemon = True
        timer.start()
        try:
            assert job._proc.stdout is not None
            for line in job._proc.stdout:
                job.log.append(line.rstrip("\r\n"))
            job.exit_code = job._proc.wait()
        finally:
            timer.cancel()
        if job.cancel_requested:
            self._finish(job, JobStatus.cancelled, "cancelled")
            return
        if job.timed_out:
            self._finish(job, JobStatus.failed, f"stopped after the {job.timeout_s / 60:g} minute time limit")
            return
        try:
            status = finalize(job)
        except Exception as e:  # a broken result must not leave the job running forever
            log.exception("finalizing job %s failed", job.id)
            status, job.error = JobStatus.failed, f"could not read the job's result: {e}"
        self._finish(job, status, job.error)

    def _on_timeout(self, job: Job) -> None:
        if job._proc is not None and job._proc.poll() is None:
            job.timed_out = True
            process.kill_tree(job._proc)

    def _finish(self, job: Job, status: JobStatus, error: str | None) -> None:
        job.status = status
        job.error = error if status != JobStatus.completed else None
        job.finished_at = _now()
        job._proc = None
        log.info("job %s (%s %s) %s%s", job.id, job.kind.value, job.name, status.value,
                 f": {job.error}" if job.error else "")

    def _prune(self) -> None:
        with self._lock:
            finished = sorted((j for j in self._jobs.values() if j.status.finished), key=lambda j: j.created_at)
            excess = len(self._jobs) - self._max_retained
            doomed = finished[:max(0, excess)]
            for job in doomed:
                self._jobs.pop(job.id, None)
        for job in doomed:
            remove_tree(job.work_dir)


def new_job_id() -> str:
    return uuid.uuid4().hex[:12]
