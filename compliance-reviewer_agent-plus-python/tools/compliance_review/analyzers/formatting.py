"""CS-02: formatting/indentation is consistent, or enforced by a
formatter/linter config. Checks for config presence; optionally runs the
project's own formatter in --check/verify mode if the tool is installed
(never modifies files).
"""
from __future__ import annotations

from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck, run_subprocess, tool_available

CONFIG_FILES = [".editorconfig", ".eslintrc", ".eslintrc.json", ".eslintrc.js", "ruff.toml", "pyproject.toml"]


def run(target_path: Path) -> list[AnalyzerCheck]:
    found = next((f for f in CONFIG_FILES if (target_path / f).is_file()), None)
    common = dict(
        title="No formatter/linter config found to enforce consistent style",
        recommendation="Add a .editorconfig (and/or ruff/eslint config) so formatting stays enforced as the team grows.",
        standard="fallback rubric",
        confidence="High",
        effort="Small",
    )

    if found is None:
        return [AnalyzerCheck(
            "CS-02", "Implementation", "Coding Standards", "Information", False,
            "no .editorconfig or linter/formatter config file found", evidence=[], **common,
        )]

    evidence = [Evidence(file=found)]
    verify_note = ""
    if (target_path / found).name == ".editorconfig" and tool_available("dotnet") and any(target_path.rglob("*.csproj")):
        code, _out, _err = run_subprocess(["dotnet", "format", "--verify-no-changes"], cwd=target_path, timeout=180)
        if code not in (-1,):
            verify_note = " (dotnet format --verify-no-changes " + ("passed)" if code == 0 else "reported differences)")

    return [AnalyzerCheck(
        "CS-02", "Implementation", "Coding Standards", "Information", True,
        f"{found} is present{verify_note}", evidence=evidence, **common,
    )]
