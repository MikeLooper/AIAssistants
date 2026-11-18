import json
import time

import pytest
from fastapi.testclient import TestClient

from comp_review_api.config import Settings
from comp_review_api.main import create_app

from .conftest import make_zip, wait_job

APP_ZIP = make_zip({"myapp/main.py": "print('hi')", "myapp/README.md": "# app"})


def _upload(client, data=APP_ZIP, filename="myapp.zip", **form):
    return client.post("/api/reviews", files={"file": (filename, data, "application/zip")},
                       data={k: str(v) for k, v in form.items()})


def _args(job: dict) -> list[str]:
    line = next(ln for ln in job["log"] if ln.startswith("ARGS "))
    return json.loads(line[5:])


# ---------------------------------------------------------------------- about / health / docs


def test_about(client):
    r = client.get("/api/about")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "comp-review-api"
    assert body["reviewerVersion"] == "1.0.0"
    assert body["environment"] == "development"
    assert body["subjects"] == ["review-maintainability", "review-testing"]
    assert {t["name"] for t in body["tools"]} == {"claude", "copilot"}
    assert body["configuration"]["Port"] == 12001
    assert body["configuration"]["Environment"] == "development"


def test_health_healthy_or_degraded(client, monkeypatch):
    monkeypatch.setattr("comp_review_api.main.shutil.which", lambda name: f"/bin/{name}")
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    monkeypatch.setattr("comp_review_api.main.shutil.which", lambda name: None)
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "degraded"
    assert r.json()["checks"]["aiTool"] is False


def test_health_unhealthy_without_reviewer_script(client, fake_root):
    (fake_root / "scripts" / "run_review.py").unlink()
    r = client.get("/api/health")
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "unhealthy"
    assert body["checks"]["reviewerScript"] is False
    assert "not found" in body["details"]["reviewerScript"]


def test_swagger_ui_and_root_redirect(client):
    assert client.get("/swagger").status_code == 200
    assert "swagger-ui" in client.get("/swagger").text
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 307) and r.headers["location"] == "/swagger"


def test_testers_are_documented_in_development(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/testers" in paths and "/api/testers/{name}" in paths
    assert "/api/reviews" in paths and "/api/about" in paths and "/api/health" in paths


def test_testers_are_hidden_and_blocked_in_production(settings):
    settings.environment = "production"
    with TestClient(create_app(settings)) as c:
        doc = c.get("/openapi.json").json()
        assert not any(p.startswith("/api/testers") for p in doc["paths"])
        assert "/api/reviews" in doc["paths"]
        assert c.get("/api/about").json()["environment"] == "production"
        # a direct call is refused the same way as an unknown path, whatever its name or body
        assert c.get("/api/testers").status_code == 404
        assert c.post("/api/testers/api-dotnet", json={"noBuild": True}).status_code == 404
        assert c.post("/api/testers/not-a-test").status_code == 404
        assert c.post("/api/testers/api-dotnet", json={"minFound": 500}).status_code == 404
        assert c.get("/api/jobs").json() == []  # nothing was started


def test_cors_allows_the_web_ui(client):
    r = client.options("/api/about", headers={"Origin": "http://localhost:12101",
                                              "Access-Control-Request-Method": "GET"})
    assert r.headers.get("access-control-allow-origin") == "http://localhost:12101"


# ---------------------------------------------------------------------- reviews


def test_review_happy_path(client, settings):
    r = _upload(client, tool="claude", model="claude-sonnet-5-5", subjects="review-testing")
    assert r.status_code == 202
    job = r.json()
    assert job["kind"] == "review"
    assert job["name"] == "myapp"
    assert job["status"] in ("queued", "running", "completed")
    assert job["options"]["fileName"] == "myapp.zip"

    job = wait_job(client, job["id"])
    assert job["status"] == "completed", job
    assert job["overallScore"] == 87 and job["overallBand"] == "Good"
    assert job["result"]["report"].startswith("# Report for myapp")
    assert job["result"]["runId"] == "2026-11-16_1200-myapp"
    assert job["result"]["summary"]["usage"]["costUsd"] == 1.5
    args = _args(job)
    assert args[args.index("--tool") + 1] == "claude"
    assert args[args.index("--model") + 1] == "claude-sonnet-5-5"
    assert args[args.index("--subjects") + 1] == "review-testing"
    files_line = next(ln for ln in job["log"] if ln.startswith("FILES "))
    assert json.loads(files_line[6:]) == ["README.md", "main.py"]

    report = client.get(f"/api/jobs/{job['id']}/report")
    assert report.status_code == 200
    assert report.headers["content-type"].startswith("text/markdown")
    assert "Score 87" in report.text
    # the extracted source is removed once the review ends
    assert not (settings.work_path / "jobs" / job["id"] / "source").exists()


def test_review_uses_configured_defaults(settings):
    settings.default_model = "claude-haiku-5-5"
    settings.default_tool = "copilot"
    settings.review_timeout_min = 7
    with TestClient(create_app(settings)) as c:
        job = wait_job(c, _upload(c).json()["id"])
        args = _args(job)
        assert args[args.index("--model") + 1] == "claude-haiku-5-5"
        assert args[args.index("--tool") + 1] == "copilot"
        assert args[args.index("--timeout") + 1] == "7"
        assert "--advanced" not in args


def test_review_advanced_options(client):
    job = wait_job(client, _upload(client, advanced="true", analyzers="pip-audit", timeoutMin=5).json()["id"])
    args = _args(job)
    assert args[args.index("--analyzers") + 1] == "pip-audit"
    assert args[args.index("--timeout") + 1] == "5"


def test_keep_sources(settings):
    settings.keep_sources = True
    with TestClient(create_app(settings)) as c:
        job = wait_job(c, _upload(c).json()["id"])
        assert (settings.work_path / "jobs" / job["id"] / "source" / "myapp" / "myapp" / "main.py").exists()


@pytest.mark.parametrize("keep_sources", [False, True])
def test_review_process_start_failure_cleans_source(settings, monkeypatch, keep_sources):
    settings.keep_sources = keep_sources

    def fail_start(*args):
        raise OSError("process could not start")

    monkeypatch.setattr("comp_review_api.jobs.process.start", fail_start)
    with TestClient(create_app(settings)) as c:
        job = wait_job(c, _upload(c).json()["id"])
        source = settings.work_path / "jobs" / job["id"] / "source"
        assert job["status"] == "failed"
        assert source.exists() is keep_sources


def test_review_reported_failure(client):
    job = wait_job(client, _upload(client, make_zip({"app/FAIL": "", "app/a.py": "x"}), "app.zip").json()["id"])
    assert job["status"] == "failed"
    assert job["error"].startswith("step 01: inventory failed")
    assert job["result"]["report"] is None
    assert client.get(f"/api/jobs/{job['id']}/report").status_code == 404


def test_review_crash_without_summary(client):
    job = wait_job(client, _upload(client, make_zip({"app/CRASH": "", "app/a.py": "x"}), "app.zip").json()["id"])
    assert job["status"] == "failed"
    assert "exited with code 2" in job["error"]
    assert "boom" in job["error"]


@pytest.mark.parametrize("form, files, message", [
    ({"model": "--evil"}, None, "invalid model"),
    ({"subjects": "review-nope"}, None, "unknown subject"),
    ({"tool": "gemini"}, None, None),
    ({"timeoutMin": "0"}, None, "timeout"),
    ({}, ("notes.txt", b"hello"), "must be a .zip"),
    ({}, ("bad.zip", b"not a zip"), "not a zip"),
    ({}, ("evil.zip", make_zip({"../evil.py": "x"})), "outside"),
    ({}, ("conflict.zip", make_zip({"a": "x", "a/b": "y"})), "conflicting"),
    ({}, ("conflict.zip", make_zip({"a/b": "y", "a": "x"})), "conflicting"),
])
def test_review_bad_requests(client, form, files, message):
    if files:
        r = _upload(client, files[1], files[0], **form)
    else:
        r = _upload(client, **form)
    assert r.status_code in (400, 422), r.text
    if message:
        assert message in r.json()["detail"]
    assert client.get("/api/jobs").json() == []


def test_review_missing_file(client):
    assert client.post("/api/reviews", data={"tool": "claude"}).status_code == 422


def test_upload_too_large(settings):
    settings.max_upload_mb = 1
    with TestClient(create_app(settings)) as c:
        r = _upload(c, make_zip({"a/big.bin": b"\0" * (2 * 1024 * 1024)}) + b"\0" * (1024 * 1024))
        assert r.status_code == 413


# ---------------------------------------------------------------------- jobs


def test_job_not_found(client):
    for method, url in (("get", "/api/jobs/nope"), ("get", "/api/jobs/nope/report"),
                        ("post", "/api/jobs/nope/cancel"), ("delete", "/api/jobs/nope")):
        r = getattr(client, method)(url)
        assert r.status_code == 404, url


def test_list_jobs_and_filter(client):
    review = wait_job(client, _upload(client).json()["id"])
    tester = wait_job(client, client.post("/api/testers/api-dotnet").json()["id"])
    jobs = client.get("/api/jobs").json()
    assert [j["id"] for j in jobs] == [tester["id"], review["id"]]
    assert [j["id"] for j in client.get("/api/jobs?kind=review").json()] == [review["id"]]
    assert "log" not in jobs[0]
    assert client.get("/api/jobs?kind=bogus").status_code == 422


def test_log_lines_parameter(client):
    job = wait_job(client, _upload(client).json()["id"])
    full = client.get(f"/api/jobs/{job['id']}?logLines=5000").json()
    assert full["logLineCount"] == len(full["log"]) >= 3
    assert client.get(f"/api/jobs/{job['id']}?logLines=1").json()["log"] == full["log"][-1:]
    assert client.get(f"/api/jobs/{job['id']}?logLines=0").json()["log"] == []


def test_cancel_and_delete(client, settings):
    job = _upload(client, make_zip({"app/SLEEP": "", "app/a.py": "x"}), "app.zip").json()
    jobs = client.app.state.services.jobs
    end = time.time() + 15
    while jobs.get(job["id"]).status.value != "running" and time.time() < end:
        time.sleep(0.05)
    assert client.delete(f"/api/jobs/{job['id']}").status_code == 409
    r = client.post(f"/api/jobs/{job['id']}/cancel")
    assert r.status_code == 200
    job = wait_job(client, job["id"])
    assert job["status"] == "cancelled"
    assert client.delete(f"/api/jobs/{job['id']}").status_code == 204
    assert client.get(f"/api/jobs/{job['id']}").status_code == 404
    assert not (settings.work_path / "jobs" / job["id"]).exists()


# ---------------------------------------------------------------------- testers


def test_list_testers(client, fake_root):
    body = client.get("/api/testers").json()
    assert len(body) == 9
    assert body[0] == {"name": "api-dotnet", "title": "C# API", "kind": "apis", "language": "dotNET",
                       "script": "test/logic/test_api_dotnet.py"}
    (fake_root / "test" / "logic" / "test_mcp_java.py").unlink()
    assert "mcp-java" not in [t["name"] for t in client.get("/api/testers").json()]
    assert client.post("/api/testers/mcp-java").status_code == 404


@pytest.mark.parametrize("mode, status, verdict", [("pass", "completed", "pass"), ("fail", "completed", "fail")])
def test_tester_pass_and_fail(client, monkeypatch, mode, status, verdict):
    monkeypatch.setenv("FAKE_TESTER_MODE", mode)
    r = client.post("/api/testers/ui-java", json={"tool": "claude", "model": "claude-opus-5-5", "minFound": 80,
                                                   "noBuild": True, "timeoutMin": 10})
    assert r.status_code == 202
    job = wait_job(client, r.json()["id"])
    assert job["kind"] == "test" and job["name"] == "ui-java"
    assert job["status"] == status
    assert job["verdict"] == verdict
    assert job["result"]["testResultMarkdown"].startswith(f"# uis-java - {verdict.upper()}")
    assert job["result"]["report"] == "# Reviewer report\n"
    assert job["result"]["testResult"]["app"] == "uis-java"
    args = _args(job)
    assert args[args.index("--min-found") + 1] == "80"
    assert args[args.index("--model") + 1] == "claude-opus-5-5"
    assert args[args.index("--timeout") + 1] == "10"
    assert "--no-build" in args
    assert client.get(f"/api/jobs/{job['id']}/report").text == "# Reviewer report\n"


def test_tester_error_verdict_and_missing_result(client, monkeypatch):
    monkeypatch.setenv("FAKE_TESTER_MODE", "error")
    job = wait_job(client, client.post("/api/testers/mcp-python").json()["id"])
    assert job["status"] == "failed" and job["error"] == "build failed"
    assert job["result"]["verdict"] == "error"
    monkeypatch.setenv("FAKE_TESTER_MODE", "none")
    job = wait_job(client, client.post("/api/testers/mcp-python").json()["id"])
    assert job["status"] == "failed"
    assert "wrote no result" in job["error"]
    assert job["result"] is None


def test_tester_validation_and_conflict(client, monkeypatch):
    assert client.post("/api/testers/not-a-test").status_code == 422
    assert client.post("/api/testers/api-java", json={"minFound": 150}).status_code == 422
    assert client.post("/api/testers/api-java", json={"model": "-x"}).status_code == 400
    monkeypatch.setenv("FAKE_TESTER_MODE", "sleep")
    first = client.post("/api/testers/api-java").json()
    r = client.post("/api/testers/api-java")
    assert r.status_code == 409
    assert first["id"] in r.json()["detail"]
    client.post(f"/api/jobs/{first['id']}/cancel")
    assert wait_job(client, first["id"])["status"] == "cancelled"


def test_startup_clears_leftover_job_folders(settings):
    leftover = settings.work_path / "jobs" / "old"
    leftover.mkdir(parents=True)
    with TestClient(create_app(settings)):
        assert not leftover.exists()


def test_create_app_loads_settings_when_none_given(monkeypatch, tmp_path):
    monkeypatch.setenv("COMP_REVIEW_API_WORK_DIR", str(tmp_path / "w"))
    monkeypatch.setenv("COMP_REVIEW_API_ENVIRONMENT", "production")
    app = create_app()
    assert app.state.settings.is_production
    assert isinstance(app.state.settings, Settings)
