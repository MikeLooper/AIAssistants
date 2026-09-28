"""Render procedure from .github/skills/compliance-report/SKILL.md (step 99):
fills the same assets/report-template.md the agent pipeline uses with an
AggregateResult, via a tiny dependency-free mustache-subset renderer
(supports {{var}} and {{#list}}...{{/list}}, arbitrarily nested).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .aggregate import AggregateResult
from .schemas import Finding

TEMPLATE_PATH = (
    Path(__file__).resolve().parents[2]
    / ".github" / "skills" / "compliance-report" / "assets" / "report-template.md"
)

_SECTION_RE = re.compile(r"\{\{#(\w+)\}\}\n?(.*?)\{\{/\1\}\}\n?", re.DOTALL)
_VAR_RE = re.compile(r"\{\{(\w+)\}\}")


def render(template: str, context: dict[str, Any]) -> str:
    def replace_section(match: re.Match[str]) -> str:
        name = match.group(1)
        inner = match.group(2)
        items = context.get(name) or []
        return "".join(render(inner, {**context, **item}) for item in items)

    template = _SECTION_RE.sub(replace_section, template)
    return _VAR_RE.sub(lambda m: str(context.get(m.group(1), "")), template)


def _first_evidence_file(f: Finding) -> str:
    return f.evidence[0].file if f.evidence else ""


def _finding_row(f: Finding) -> dict[str, Any]:
    ev = f.evidence[0] if f.evidence else None
    return {
        "severity": f.severity,
        "title": f.title,
        "subject": f.subject,
        "file": ev.file if ev else "",
        "lineStart": ev.lineStart if ev else 0,
        "lineEnd": ev.lineEnd if ev else 0,
        "recommendation": f.recommendation,
        "standard": f.standard,
        "url": f.url,
    }


def build_context(
    aggregate: AggregateResult,
    target_name: str,
    generated_at: str,
    run_id: str,
    target_path: str,
    target_git_head: str | None,
    started_at: str,
    completed_at: str,
    skipped_subjects: dict[str, str],
    urls_fetched: list[str],
    link_approvals: dict[str, str],
    full_results: list[dict[str, Any]],
) -> dict[str, Any]:
    strengths_by_subject: dict[str, list[dict[str, str]]] = {}
    for s in aggregate.strengths:
        strengths_by_subject.setdefault(s.subject, []).append(
            {"title": s.title, "file": s.evidence[0].file if s.evidence else ""}
        )

    return {
        "targetName": target_name,
        "generatedAt": generated_at,
        "runId": run_id,
        "overallScore": aggregate.overallScore,
        "overallBand": aggregate.overallBand,
        "subjectScores": [
            {"subject": s.subject, "score": s.score, "band": s.band} for s in aggregate.subjectScores
        ],
        "errorCount": aggregate.severityCounts.get("Error", 0),
        "warningCount": aggregate.severityCounts.get("Warning", 0),
        "infoCount": aggregate.severityCounts.get("Information", 0),
        "topRisks": [_finding_row(f) for f in aggregate.topRisks],
        "strengthsBySubject": [
            {"subject": subj, "strengths": items} for subj, items in strengths_by_subject.items()
        ],
        "errorFindings": [_finding_row(f) for f in aggregate.findings if f.severity == "Error"],
        "warningFindings": [_finding_row(f) for f in aggregate.findings if f.severity == "Warning"],
        "infoFindings": [_finding_row(f) for f in aggregate.findings if f.severity == "Information"],
        "subjects": full_results,
        "targetPath": target_path,
        "targetGitHead": target_git_head or "unavailable",
        "startedAt": started_at,
        "completedAt": completed_at,
        "skippedSubjects": ", ".join(f"{k} ({v})" for k, v in skipped_subjects.items()) or "none",
        "urlsFetched": ", ".join(urls_fetched) or "none",
        "linkApprovals": ", ".join(f"{k}: {v}" for k, v in link_approvals.items()) or "none",
    }


def render_report(context: dict[str, Any], template_path: Path = TEMPLATE_PATH) -> str:
    template = template_path.read_text(encoding="utf-8")
    return render(template, context)
