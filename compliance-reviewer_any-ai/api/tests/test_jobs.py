import sys
import threading
import time

import pytest

from comp_review_api.jobs import ActiveJobError, JobKind, JobManager, JobStatus

PY = sys.executable


@pytest.fixture
def manager():
    m = JobManager(max_concurrent=1, max_retained=50)
    yield m
    m.shutdown()


def _submit(m, tmp_path, code, finalize=None, timeout_s=30, name="x"):
    return m.submit(JobKind.review, name, [PY, "-u", "-c", code], tmp_path, tmp_path / name, timeout_s,
                    finalize or (lambda job: JobStatus.completed if job.exit_code == 0 else JobStatus.failed))


def _wait_for(predicate, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        if predicate():
            return True
        time.sleep(0.05)
    return False


def test_completed_job_captures_output(manager, tmp_path):
    job = _submit(manager, tmp_path, "print('hello'); print('world')")
    manager.wait(job.id, 30)
    assert job.status == JobStatus.completed
    assert job.exit_code == 0
    assert job.log_tail(None) == ["hello", "world"]
    assert job.log_tail(1) == ["world"]
    assert job.log_tail(0) == []
    assert job.started_at and job.finished_at and job.duration_s is not None
    assert job.error is None
    assert (tmp_path / "x").is_dir()  # work dir created


def test_finalizer_sets_failure(manager, tmp_path):
    def fin(job):
        job.result = {"a": 1}
        job.error = "bad"
        return JobStatus.failed

    job = _submit(manager, tmp_path, "import sys; sys.exit(3)", fin)
    manager.wait(job.id, 30)
    assert job.status == JobStatus.failed
    assert job.exit_code == 3
    assert job.error == "bad"
    assert job.result == {"a": 1}


def test_finalizer_exception_fails_the_job(manager, tmp_path):
    def fin(job):
        raise RuntimeError("kaput")

    job = _submit(manager, tmp_path, "pass", fin)
    manager.wait(job.id, 30)
    assert job.status == JobStatus.failed
    assert "kaput" in job.error


def test_timeout_kills_the_process(manager, tmp_path):
    job = _submit(manager, tmp_path, "import time; time.sleep(30)", timeout_s=0.5)
    manager.wait(job.id, 30)
    assert job.status == JobStatus.failed
    assert job.timed_out
    assert "time limit" in job.error


def test_cancel_running_and_queued_jobs(manager, tmp_path):
    running = _submit(manager, tmp_path, "import time; print('started', flush=True); time.sleep(30)", name="a")
    queued = _submit(manager, tmp_path, "print('never')", name="b")
    assert _wait_for(lambda: running.log_tail(None) == ["started"])
    assert queued.status == JobStatus.queued
    manager.cancel(queued.id)
    assert queued.status == JobStatus.cancelled
    manager.cancel(running.id)
    manager.wait(running.id, 30)
    assert running.status == JobStatus.cancelled
    assert queued.log_tail(None) == []
    # cancelling a finished job changes nothing
    assert manager.cancel(running.id).status == JobStatus.cancelled
    assert manager.cancel("missing") is None


def test_list_get_and_delete(manager, tmp_path):
    a = _submit(manager, tmp_path, "pass", name="a")
    manager.wait(a.id, 30)
    b = manager.submit(JobKind.test, "b", [PY, "-c", "pass"], tmp_path, tmp_path / "b", 30,
                       lambda job: JobStatus.completed)
    manager.wait(b.id, 30)
    assert [j.id for j in manager.list()] == [b.id, a.id]
    assert [j.id for j in manager.list(JobKind.test)] == [b.id]
    assert manager.get(a.id) is a
    assert manager.delete(a.id)
    assert manager.get(a.id) is None
    assert not (tmp_path / "a").exists()
    assert manager.delete("missing")


def test_delete_refuses_a_running_job(manager, tmp_path):
    job = _submit(manager, tmp_path, "import time; time.sleep(30)")
    assert _wait_for(lambda: job.status == JobStatus.running)
    assert not manager.delete(job.id)
    manager.cancel(job.id)
    manager.wait(job.id, 30)


def test_old_finished_jobs_are_pruned(tmp_path):
    m = JobManager(max_concurrent=1, max_retained=2)
    try:
        ids = []
        for i in range(4):
            job = _submit(m, tmp_path, "pass", name=f"j{i}")
            m.wait(job.id, 30)
            ids.append(job.id)
        kept = {j.id for j in m.list()}
        assert ids[-1] in kept and ids[0] not in kept
        assert len(kept) <= 2
        assert not (tmp_path / "j0").exists()
    finally:
        m.shutdown()


def test_a_command_that_cannot_start_fails(manager, tmp_path):
    job = manager.submit(JobKind.review, "x", [str(tmp_path / "no-such-program")], tmp_path, tmp_path / "w", 30,
                         lambda job: JobStatus.completed)
    manager.wait(job.id, 30)
    assert job.status == JobStatus.failed
    assert "could not start" in job.error


def test_reject_active_submission_is_atomic(manager, tmp_path):
    barrier = threading.Barrier(2)
    results = []

    def submit():
        barrier.wait()
        try:
            result = manager.submit(
                JobKind.test, "same", [PY, "-c", "import time; time.sleep(30)"], tmp_path, tmp_path / "same",
                30, lambda job: JobStatus.completed, reject_active=True)
        except ActiveJobError as e:
            result = e
        results.append(result)

    threads = [threading.Thread(target=submit) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    accepted = [result for result in results if not isinstance(result, ActiveJobError)]
    conflicts = [result for result in results if isinstance(result, ActiveJobError)]
    assert len(accepted) == len(conflicts) == 1
    assert conflicts[0].job is accepted[0]
    manager.cancel(accepted[0].id)
    manager.wait(accepted[0].id, 30)
