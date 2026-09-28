"""DEP-05: a license inventory or SBOM is present."""
from __future__ import annotations

from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck

SBOM_PATTERNS = ["sbom.json", "*.cdx.json", "*.spdx.json", "bom.xml", "*-sbom.*"]


def run(target_path: Path) -> list[AnalyzerCheck]:
    match = next((p for pattern in SBOM_PATTERNS for p in target_path.glob(pattern)), None)
    match = match or next((p for pattern in SBOM_PATTERNS for p in target_path.rglob(pattern)), None)
    passed = match is not None
    evidence = [Evidence(file=match.relative_to(target_path).as_posix())] if match else []
    return [AnalyzerCheck(
        "DEP-05", "Implementation", "Dependency Management", "Information", passed,
        "an SBOM/license-inventory file was found" if passed else "no SBOM/license-inventory artifact found",
        title="No SBOM or dependency license inventory is generated", evidence=evidence,
        recommendation="Generate an SBOM (e.g. via `dotnet CycloneDX`, `cyclonedx-py`, or `npm sbom`) as part of the release process.",
        standard="fallback rubric", confidence="High", effort="Small",
    )]
