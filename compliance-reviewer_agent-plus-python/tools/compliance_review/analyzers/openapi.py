"""API-01/API-02: an OpenAPI/Swagger spec exists and is at least structurally
valid (required top-level keys present, JSON/YAML parses). Not a full
OpenAPI-Specification validator -- flags parse errors and missing required
keys only.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck

REQUIRED_KEYS = ["openapi", "info", "paths"]


def _find_spec(target_path: Path) -> Path | None:
    for pattern in ("*openapi*.json", "**/*openapi*.json", "*swagger*.json", "**/*swagger*.json"):
        match = next(target_path.glob(pattern), None)
        if match is not None:
            return match
    return None


def run(target_path: Path) -> list[AnalyzerCheck]:
    spec_path = _find_spec(target_path)
    exists_common = dict(
        recommendation="Generate and commit an OpenAPI spec (e.g. via Swashbuckle, springdoc-openapi, or FastAPI's built-in /openapi.json).",
        standard="OpenAPI Specification",
        url="https://spec.openapis.org/oas/latest.html",
        confidence="High",
        effort="Small",
    )

    if spec_path is None:
        return [AnalyzerCheck(
            "API-01", "API Design", "API Design", "Warning", None,
            "no *openapi*.json / *swagger*.json file found (JSON specs only; this check does not parse YAML specs)",
            title="No OpenAPI/Swagger spec file found", **exists_common,
        )]

    evidence = [Evidence(file=spec_path.relative_to(target_path).as_posix())]
    exists_check = AnalyzerCheck(
        "API-01", "API Design", "API Design", "Warning", True, "a spec file is present", evidence=evidence, **exists_common,
    )

    try:
        data = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [exists_check, AnalyzerCheck(
            "API-02", "API Design", "API Design", "Error", False, f"spec is not valid JSON: {exc}",
            title="OpenAPI spec is not valid JSON", evidence=evidence,
            recommendation="Fix the JSON syntax error and regenerate the spec from the running app.",
            standard="OpenAPI Specification", url="https://spec.openapis.org/oas/latest.html",
            confidence="High", effort="Small",
        )]

    missing = [k for k in REQUIRED_KEYS if k not in data]
    passed = not missing
    reason = "all required top-level keys present" if passed else f"missing required top-level key(s): {', '.join(missing)}"
    return [exists_check, AnalyzerCheck(
        "API-02", "API Design", "API Design", "Error", passed, reason,
        title="OpenAPI spec is missing required top-level keys", evidence=evidence,
        recommendation="Ensure the generated spec includes openapi/info/paths (this is a structural check only, not a full schema validation).",
        standard="OpenAPI Specification", url="https://spec.openapis.org/oas/latest.html",
        confidence="High", effort="Small",
    )]
