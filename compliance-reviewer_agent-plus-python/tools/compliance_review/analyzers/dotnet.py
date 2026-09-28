"""DEP-03 (.NET): known vulnerable NuGet packages via
`dotnet list package --vulnerable --include-transitive`.
Only invoked when the caller has approved running analyzers (see cli.py
--run-analyzers), per .github/skills/compliance-inventory/references/analyzers.md.
"""
from __future__ import annotations

from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck, run_subprocess, tool_available

COMMON = dict(
    recommendation="Upgrade the flagged package(s) to a patched version.",
    standard="fallback rubric",
    confidence="High",
    effort="Medium",
)


def run(target_path: Path) -> list[AnalyzerCheck]:
    if not any(target_path.rglob("*.csproj")) and not any(target_path.glob("*.sln")):
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "no .csproj/.sln project found", **COMMON)]
    if not tool_available("dotnet"):
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "the 'dotnet' CLI is not installed/available on PATH", **COMMON)]

    code, out, err = run_subprocess(
        ["dotnet", "list", "package", "--vulnerable", "--include-transitive"], cwd=target_path, timeout=300,
    )
    if code == -1:
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               f"dotnet list package failed to run: {err}", **COMMON)]

    lower = out.lower()
    has_vulnerabilities = "has the following vulnerable packages" in lower
    vuln_lines = [line.strip() for line in out.splitlines() if ">" in line and "vulnerable" not in line.lower()]
    reason = (
        f"dotnet list package reported vulnerable packages:\n{out.strip()[-2000:]}"
        if has_vulnerabilities
        else "dotnet list package --vulnerable reported no vulnerable packages"
    )
    return [AnalyzerCheck(
        "DEP-03", "Implementation", "Dependency Management", "Error", not has_vulnerabilities, reason,
        title="dotnet list package reports known-vulnerable NuGet package(s)",
        evidence=[Evidence(file="(dotnet list package --vulnerable output)", excerpt=line) for line in vuln_lines[:10]],
        **COMMON,
    )]
