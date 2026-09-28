"""Shared helpers for tool-backed analyzer checks (Phase 2).

Each analyzer module exposes `run(target_path: Path) -> list[AnalyzerCheck]`.
An AnalyzerCheck converts 1:1 into a schemas.CheckResult, and into a
schemas.Finding when it fails. `passed=None` means the tool/manifest needed to
evaluate the check wasn't available -- that maps to result="N/A", never to a
fail, so a missing tool never silently counts against the score.
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ..schemas import CheckResult, Evidence, Finding, Severity


@dataclass
class AnalyzerCheck:
    checkId: str
    subject: str
    subSubject: str
    severityIfFailed: Severity
    passed: Optional[bool]  # True/False, or None if not evaluable (-> N/A)
    reason: str
    title: str = ""
    evidence: list[Evidence] = field(default_factory=list)
    recommendation: str = ""
    standard: str = ""
    url: str = ""
    confidence: str = "High"
    effort: str = "Small"

    def to_check_result(self, finding_id: Optional[str]) -> CheckResult:
        if self.passed is None:
            result = "N/A"
        else:
            result = "pass" if self.passed else "fail"
        return CheckResult(
            checkId=self.checkId,
            subject=self.subject,
            subSubject=self.subSubject,
            severityIfFailed=self.severityIfFailed,
            result=result,
            reason=self.reason,
            findingIds=[finding_id] if finding_id else [],
        )

    def to_finding(self, finding_id: str) -> Optional[Finding]:
        if self.passed is not False:
            return None
        return Finding(
            id=finding_id,
            subject=self.subject,
            subSubject=self.subSubject,
            checkId=self.checkId,
            severity=self.severityIfFailed,
            title=self.title or self.reason,
            evidence=self.evidence,
            standard=self.standard,
            url=self.url,
            recommendation=self.recommendation,
            confidence=self.confidence,
            effort=self.effort,
        )


def tool_available(name: str) -> bool:
    return shutil.which(name) is not None


def run_subprocess(args: list[str], cwd: Path, timeout: int = 120) -> tuple[int, str, str]:
    """Runs a read-only CLI command. Never raises; returns (-1, "", err) on failure."""
    try:
        proc = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -1, "", str(exc)
