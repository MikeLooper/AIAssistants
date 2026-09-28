"""SL-01 / TST-06: CI runs build and automated tests on every push/PR."""
from __future__ import annotations

from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck

TEST_COMMAND_MARKERS = [
    "dotnet test", "pytest", "npm test", "npm run test", "mvn test", "gradle test", "go test",
]


def _workflow_files(target_path: Path) -> list[Path]:
    workflows_dir = target_path / ".github" / "workflows"
    files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")) if workflows_dir.is_dir() else []
    files += [p for p in (target_path / "azure-pipelines.yml", target_path / "Jenkinsfile") if p.is_file()]
    return files


def run(target_path: Path) -> list[AnalyzerCheck]:
    files = _workflow_files(target_path)
    common = dict(
        recommendation="Add a CI workflow (e.g. GitHub Actions) that runs the build and test command on every push/PR.",
        standard="SLSA v1.0 build requirements",
        url="https://slsa.dev/spec/v1.0/requirements",
        confidence="High",
        effort="Small",
    )

    if not files:
        reason = "no .github/workflows/*.yml, azure-pipelines.yml or Jenkinsfile found"
        evidence = [Evidence(file=".github/workflows/", excerpt="(missing or empty)")]
        return [
            AnalyzerCheck(
                "SL-01", "Software Lifecycle", "Software Lifecycle", "Error", False, reason,
                title="No CI pipeline builds or tests the solution on push/PR", evidence=evidence, **common,
            ),
            AnalyzerCheck(
                "TST-06", "Implementation", "Testing", "Error", False, reason,
                title="The test suite has no CI pipeline to run it automatically", evidence=evidence, **common,
            ),
        ]

    runs_tests = False
    matched_file = files[0]
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore").lower()
        if any(marker in text for marker in TEST_COMMAND_MARKERS):
            runs_tests = True
            matched_file = f
            break

    reason = (
        "a CI workflow exists and references a test command"
        if runs_tests
        else "a CI workflow exists but no recognized test command (dotnet test/pytest/npm test/etc.) was found in it"
    )
    evidence = [Evidence(file=matched_file.relative_to(target_path).as_posix())]
    return [
        AnalyzerCheck("SL-01", "Software Lifecycle", "Software Lifecycle", "Error", runs_tests, reason,
                       title="CI pipeline does not appear to run the test suite", evidence=evidence, **common),
        AnalyzerCheck("TST-06", "Implementation", "Testing", "Error", runs_tests, reason,
                       title="CI pipeline does not appear to run the test suite", evidence=evidence, **common),
    ]
