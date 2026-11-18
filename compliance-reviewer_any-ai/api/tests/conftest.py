from __future__ import annotations

import io
import shutil
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from comp_review_api.commands import TESTER_DEFINITIONS
from comp_review_api.config import Settings
from comp_review_api.main import create_app

FAKES = Path(__file__).parent / "fakes"


@pytest.fixture
def fake_root(tmp_path: Path) -> Path:
    """A minimal Compliance Reviewer workspace: VERSION, the reviewer script, testers and two subjects."""
    root = tmp_path / "reviewer"
    (root / "scripts").mkdir(parents=True)
    shutil.copy(FAKES / "fake_run_review.py", root / "scripts" / "run_review.py")
    logic = root / "test" / "logic"
    logic.mkdir(parents=True)
    for t in TESTER_DEFINITIONS:
        shutil.copy(FAKES / "fake_tester.py", logic / t.script)
    for subject in ("review-testing", "review-maintainability"):
        (root / "compliance-reviewer" / "skills" / subject).mkdir(parents=True)
    (root / "compliance-reviewer" / "skills" / "compliance-report").mkdir(parents=True)
    (root / "VERSION").write_text("1.0.0\n")
    return root


@pytest.fixture
def settings(fake_root: Path, tmp_path: Path) -> Settings:
    return Settings(reviewer_root=str(fake_root), work_dir=str(tmp_path / "work"), max_concurrent_jobs=2).validate()


@pytest.fixture
def client(settings: Settings):
    app = create_app(settings)
    with TestClient(app) as c:
        yield c


def make_zip(files: dict[str, str | bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


def wait_job(client: TestClient, job_id: str, timeout: float = 30) -> dict:
    client.app.state.services.jobs.wait(job_id, timeout)
    return client.get(f"/api/jobs/{job_id}").json()
