"""Aggregate procedure from .github/skills/compliance-report/SKILL.md (step 90):
merge exact + cross-subject semantic duplicate findings (by overlapping
evidence), compute subject/overall scores, severity counts and the top-5
risks list.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field

from .schemas import CheckResult, Evidence, Finding, Strength
from .scoring import SubjectScore, compute_all_subject_scores, compute_overall_score

SEVERITY_RANK = {"Error": 3, "Warning": 2, "Information": 1}
CONFIDENCE_RANK = {"High": 3, "Medium": 2, "Low": 1}
EFFORT_RANK = {"Small": 1, "Medium": 2, "Large": 3}

# Mirrors the orchestrator's fixed step order (10-27) so tied-severity
# duplicates keep the finding from whichever subject/sub-subject runs first.
PIPELINE_ORDER: list[tuple[str, str]] = [
    ("Software Quality", "Software Quality"),
    ("Software Quality", "Design Patterns"),
    ("Software Quality", "Architecture Patterns"),
    ("Software Lifecycle", "Software Lifecycle"),
    ("Application Design", "Twelve-Factor"),
    ("API Design", "API Design"),
    ("Security", "Identity & Access"),
    ("Security", "Input & Injection"),
    ("Security", "Web & API"),
    ("Security", "Operational"),
    ("Implementation", "Coding Standards"),
    ("Implementation", "Testing"),
    ("Implementation", "Observability"),
    ("Implementation", "Dependency Management"),
    ("Operations", "Reliability"),
    ("Operations", "Performance"),
    ("Operations", "Disaster Recovery"),
    ("Operations", "Monitoring"),
    ("Operations", "Cost & Sustainability"),
    ("Operations", "Maintainability"),
]
PIPELINE_RANK = {key: i for i, key in enumerate(PIPELINE_ORDER)}


def _rank(f: Finding) -> int:
    return PIPELINE_RANK.get((f.subject, f.subSubject), len(PIPELINE_ORDER))


def _evidence_overlaps(a: Evidence, b: Evidence) -> bool:
    if a.file != b.file:
        return False
    if a.lineStart == a.lineEnd == b.lineStart == b.lineEnd == 0:
        return True  # both are file-level (non-line-specific) evidence
    return a.lineStart <= b.lineEnd and b.lineStart <= a.lineEnd


def _findings_overlap(a: Finding, b: Finding) -> bool:
    return any(_evidence_overlaps(ea, eb) for ea in a.evidence for eb in b.evidence)


@dataclass
class DuplicateRecord:
    suppressedId: str
    primaryId: str
    reason: str


def dedup_findings(findings: list[Finding]) -> tuple[list[Finding], list[DuplicateRecord]]:
    """Union-find over overlapping evidence, then keep one primary per group:
    highest severity wins; ties keep the earlier-pipeline-order finding."""
    parent = {f.id: f.id for f in findings}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i in range(len(findings)):
        for j in range(i + 1, len(findings)):
            if _findings_overlap(findings[i], findings[j]):
                union(findings[i].id, findings[j].id)

    groups: dict[str, list[Finding]] = {}
    for f in findings:
        groups.setdefault(find(f.id), []).append(f)

    kept: list[Finding] = []
    duplicates: list[DuplicateRecord] = []
    for group in groups.values():
        if len(group) == 1:
            kept.append(group[0])
            continue
        primary = min(group, key=lambda x: (-SEVERITY_RANK[x.severity], _rank(x)))
        merged_evidence = list(primary.evidence)
        seen = {(e.file, e.lineStart, e.lineEnd) for e in merged_evidence}
        for g in group:
            if g.id == primary.id:
                continue
            for e in g.evidence:
                key = (e.file, e.lineStart, e.lineEnd)
                if key not in seen:
                    merged_evidence.append(e)
                    seen.add(key)
            duplicates.append(DuplicateRecord(
                suppressedId=g.id,
                primaryId=primary.id,
                reason=(
                    f"Overlapping evidence with {primary.id} "
                    f"({primary.subject}/{primary.subSubject}); "
                    f"{g.severity} finding from {g.subject}/{g.subSubject} suppressed as a duplicate."
                ),
            ))
        kept.append(dataclasses.replace(primary, evidence=merged_evidence))
    return kept, duplicates


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts = {"Error": 0, "Warning": 0, "Information": 0}
    for f in findings:
        counts[f.severity] += 1
    return counts


def select_top_risks(findings: list[Finding], limit: int = 5) -> list[Finding]:
    ordered = sorted(
        findings,
        key=lambda f: (-SEVERITY_RANK[f.severity], -CONFIDENCE_RANK[f.confidence], EFFORT_RANK[f.effort]),
    )
    return ordered[:limit]


@dataclass
class AggregateResult:
    overallScore: float
    overallBand: str
    subjectScores: list[SubjectScore]
    severityCounts: dict[str, int]
    findings: list[Finding]
    strengths: list[Strength]
    topRisks: list[Finding]
    duplicatesSuppressed: list[DuplicateRecord]

    def to_dict(self) -> dict:
        return {
            "overallScore": self.overallScore,
            "overallBand": self.overallBand,
            "subjectScores": [
                {"subject": s.subject, "score": s.score, "band": s.band, "passWeight": s.passWeight, "totalWeight": s.totalWeight}
                for s in self.subjectScores
            ],
            "severityCounts": self.severityCounts,
            "findings": [f.to_dict() for f in self.findings],
            "strengths": [s.to_dict() for s in self.strengths],
            "topRisks": [{"findingId": f.id, "severity": f.severity, "title": f.title} for f in self.topRisks],
            "duplicatesSuppressed": [dataclasses.asdict(d) for d in self.duplicatesSuppressed],
        }


def aggregate_run(
    check_results: list[CheckResult],
    findings: list[Finding],
    strengths: list[Strength],
) -> AggregateResult:
    deduped, duplicates = dedup_findings(findings)
    subject_scores = compute_all_subject_scores(check_results)
    overall_score, overall_band = compute_overall_score(subject_scores)
    return AggregateResult(
        overallScore=overall_score,
        overallBand=overall_band,
        subjectScores=subject_scores,
        severityCounts=severity_counts(deduped),
        findings=deduped,
        strengths=strengths,
        topRisks=select_top_risks(deduped),
        duplicatesSuppressed=duplicates,
    )
