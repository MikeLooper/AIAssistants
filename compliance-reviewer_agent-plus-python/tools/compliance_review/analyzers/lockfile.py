"""DEP-02 / TF-02: a dependency lock file exists and is committed.

Deliberately produced as two separate AnalyzerChecks (matching the two
checklist ids in review-dependency-management and review-twelve-factor) so
aggregate.py's cross-subject dedup exercises the same path a real run does.
"""
from __future__ import annotations

from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck

MANIFEST_GLOBS = ["**/*.csproj", "pom.xml", "**/pom.xml", "requirements.txt", "pyproject.toml", "package.json"]
LOCK_FILE_GLOBS = [
    "**/packages.lock.json", "poetry.lock", "package-lock.json", "yarn.lock", "Pipfile.lock", "**/Gemfile.lock",
]


def _first_match(root: Path, patterns: list[str]) -> Path | None:
    for p in patterns:
        match = next(root.glob(p), None)
        if match is not None:
            return match
    return None


def run(target_path: Path) -> list[AnalyzerCheck]:
    manifest = _first_match(target_path, MANIFEST_GLOBS)
    has_lock = _first_match(target_path, LOCK_FILE_GLOBS) is not None

    if manifest is None:
        reason = "no dependency manifest found"
        return [
            AnalyzerCheck("DEP-02", "Implementation", "Dependency Management", "Warning", None, reason),
            AnalyzerCheck("TF-02", "Application Design", "Twelve-Factor", "Error", None, reason),
        ]

    passed = has_lock
    reason = "a lock file is committed" if passed else "no lock file (packages.lock.json/poetry.lock/package-lock.json/etc.) found alongside the dependency manifest"
    common = dict(
        title="No committed dependency lock file",
        evidence=[Evidence(file=manifest.relative_to(target_path).as_posix(), excerpt="dependency manifest")],
        recommendation="Enable lock-file generation for the detected package manager and commit the result "
        "(e.g. <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile> for NuGet, `poetry lock`, "
        "`npm install --package-lock-only`).",
        standard="Twelve-Factor App II. Dependencies",
        url="https://12factor.net/dependencies",
        confidence="High",
        effort="Small",
    )
    return [
        AnalyzerCheck("DEP-02", "Implementation", "Dependency Management", "Warning", passed, reason, **common),
        AnalyzerCheck("TF-02", "Application Design", "Twelve-Factor", "Error", passed, reason, **common),
    ]
