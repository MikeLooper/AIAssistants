"""Runs every Phase-2 analyzer and returns their combined AnalyzerCheck list.

`file_checks` need no approval -- they only read files already in the repo.
`vulnerability_scanners` shell out to installed CLI tools and are only run
when the caller passes run_vuln_scanners=True (the CLI's --run-analyzers
flag), mirroring the agent pipeline's analyzer-approval requirement.
"""
from __future__ import annotations

from pathlib import Path

from . import ci, dotnet, formatting, lockfile, node, openapi, python_pkg, sbom, secrets
from .base import AnalyzerCheck

FILE_CHECK_MODULES = [lockfile, ci, secrets, formatting, openapi, sbom]
VULN_SCANNER_MODULES = [dotnet, node, python_pkg]


def run_all(target_path: Path, run_vuln_scanners: bool = False) -> list[AnalyzerCheck]:
    checks: list[AnalyzerCheck] = []
    for module in FILE_CHECK_MODULES:
        checks.extend(module.run(target_path))
    if run_vuln_scanners:
        for module in VULN_SCANNER_MODULES:
            checks.extend(module.run(target_path))
    return checks


__all__ = ["run_all", "AnalyzerCheck"]
