"""DEP-03 (Python): known vulnerable packages via `pip-audit -f json`.
Only invoked when the caller has approved running analyzers (see cli.py
--run-analyzers), per .github/skills/compliance-inventory/references/analyzers.md.
"""
from __future__ import annotations

import json
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
    has_manifest = (target_path / "requirements.txt").is_file() or (target_path / "pyproject.toml").is_file()
    if not has_manifest:
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "no requirements.txt/pyproject.toml found", **COMMON)]
    if not tool_available("pip-audit"):
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               "'pip-audit' is not installed", **COMMON)]

    code, out, err = run_subprocess(["pip-audit", "-f", "json"], cwd=target_path, timeout=300)
    if code == -1:
        return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", None,
                               f"pip-audit failed to run: {err}", **COMMON)]
    try:
        data = json.loads(out)
        vulns = [dep for dep in data.get("dependencies", data if isinstance(data, list) else []) if dep.get("vulns")]
    except (json.JSONDecodeError, AttributeError):
        vulns = []

    passed = not vulns
    reason = f"pip-audit found {len(vulns)} package(s) with known vulnerabilities" if vulns else "pip-audit found no known vulnerabilities"
    evidence = [
        Evidence(file="(pip-audit output)", excerpt=f"{v.get('name')} {v.get('version')}: {[x.get('id') for x in v.get('vulns', [])]}")
        for v in vulns[:10]
    ]
    return [AnalyzerCheck("DEP-03", "Implementation", "Dependency Management", "Error", passed, reason,
                           title="pip-audit reports known-vulnerable Python package(s)", evidence=evidence, **COMMON)]
