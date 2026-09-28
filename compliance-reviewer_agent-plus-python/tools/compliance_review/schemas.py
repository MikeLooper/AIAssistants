"""Shared data shapes for the compliance-review Python pipeline.

Mirrors the JSON contracts defined in the agent-based pipeline so output from
this package is interchangeable with runs produced by the `compliance-reviewer`
agent:
- .github/skills/compliance-review-core/references/finding-schema.md
- .github/skills/compliance-review-core/references/transition-schema.md

Only the stdlib is used (dataclasses), so this package has no install step.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

SCHEMA_VERSION = 1

Severity = Literal["Error", "Warning", "Information"]
Confidence = Literal["High", "Medium", "Low"]
Effort = Literal["Small", "Medium", "Large"]
CheckOutcome = Literal["pass", "fail", "N/A"]

# weight-and-scoring.md
SEVERITY_WEIGHT: dict[str, int] = {"Error": 5, "Warning": 2, "Information": 1}


def _to_dict(obj: Any) -> Any:
    """dataclasses.asdict, but drops None values so JSON output stays compact."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {
            k: _to_dict(v)
            for k, v in dataclasses.asdict(obj).items()
            if v is not None
        }
    if isinstance(obj, list):
        return [_to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    return obj


@dataclass
class Evidence:
    file: str
    lineStart: int = 0
    lineEnd: int = 0
    excerpt: str = ""


@dataclass
class Finding:
    id: str
    subject: str
    subSubject: str
    checkId: str
    severity: Severity
    title: str
    evidence: list[Evidence]
    standard: str = ""
    url: str = ""
    recommendation: str = ""
    confidence: Confidence = "Medium"
    effort: Effort = "Medium"

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class Strength:
    id: str
    subject: str
    subSubject: str
    title: str
    evidence: list[Evidence]
    checkId: Optional[str] = None
    standard: Optional[str] = None
    url: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class CheckResult:
    checkId: str
    subject: str
    subSubject: str
    severityIfFailed: Severity
    result: CheckOutcome
    reason: Optional[str] = None
    findingIds: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class WorkerEnvelope:
    """Same shape the compliance-subject-reviewer agent returns per subject/batch."""

    skill: str
    subject: str
    batchIndex: int = 0
    findings: list[Finding] = field(default_factory=list)
    strengths: list[Strength] = field(default_factory=list)
    checkResults: list[CheckResult] = field(default_factory=list)
    urlsFetched: list[str] = field(default_factory=list)
    notes: Optional[str] = None
    schemaVersion: int = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)


@dataclass
class TransitionHeader:
    """Required header fields for every NN-*.json transition file."""

    runId: str
    stepId: str
    targetPath: str
    status: Literal["started", "completed", "failed"] = "started"
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    targetGitHead: Optional[str] = None
    inputsHash: Optional[str] = None
    schemaVersion: int = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _to_dict(self)
