"""DEP-03 (Node): known vulnerable npm packages via `npm audit --json`.
Only invoked when the caller has approved running analyzers (see cli.py
--run-analyzers), per .github/skills/compliance-inventory/references/analyzers.md.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck, run_subprocess, tool_available

COMMON = dict(
    recommendation="Run `npm audit fix` (or upgrade manually) to resolve the flagged advisories.",
    standard="fallback rubric",
    confidence="High",
    effort="Medium",
)


def run(target_path: Path) -> list[AnalyzerCheck]:
    if not (target_path / "package.json").is_file():
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "no package.json found", **COMMON)]
    if not tool_available("npm"):
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "'npm' is not installed", **COMMON)]

    code, out, err = run_subprocess(["npm", "audit", "--json"], cwd=target_path, timeout=300)
    if code == -1:
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               f"npm audit failed to run: {err}", **COMMON)]
    try:
        data = json.loads(out)
        total_vulns = data.get("metadata", {}).get("vulnerabilities", {})
        count = sum(v for k, v in total_vulns.items() if k != "total") if total_vulns else 0
    except json.JSONDecodeError:
        count = 0

    passed = count == 0
    reason = f"npm audit found {count} vulnerabilit(y/ies)" if count else "npm audit found no vulnerabilities"
    return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", passed, reason,
                           title="npm audit reports known-vulnerable package(s)",
                           evidence=[Evidence(file="package.json", excerpt=f"npm audit vulnerability count: {count}")],
                           **COMMON)]
