"""Implements the scoring formula and rating bands from
.github/skills/compliance-review-core/references/severity-and-scoring.md

    score = (weighted checks passed) / (weighted checks that apply) * 100
    weights: Error=5, Warning=2, Information=1; N/A is excluded entirely.
    bands: 90-100 Excellent, 75-89 Good, 60-74 Fair, <60 Poor.

The overall score is the weighted average of subject scores, weighted by each
subject's own total applicable weight -- which is mathematically the same as
summing every subject's pass/total weights directly, so that's what
`compute_overall_score` does (avoids compounding rounding error).
"""
from __future__ import annotations

from dataclasses import dataclass

from .schemas import SEVERITY_WEIGHT, CheckResult

BANDS = (
    (90, "Excellent"),
    (75, "Good"),
    (60, "Fair"),
    (0, "Poor"),
)


def band_for_score(score: float) -> str:
    for threshold, band in BANDS:
        if score >= threshold:
            return band
    return "Poor"


@dataclass
class SubjectScore:
    subject: str
    passWeight: int
    totalWeight: int

    @property
    def score(self) -> float:
        if self.totalWeight == 0:
            return 0.0
        return round(self.passWeight / self.totalWeight * 100, 2)

    @property
    def band(self) -> str:
        return band_for_score(self.score)


def weight_for(check: CheckResult) -> int:
    return SEVERITY_WEIGHT[check.severityIfFailed]


def compute_subject_score(subject: str, check_results: list[CheckResult]) -> SubjectScore:
    """Aggregates every checkResult for one subject (across all its skills)."""
    pass_weight = 0
    total_weight = 0
    for check in check_results:
        if check.subject != subject or check.result == "N/A":
            continue
        w = weight_for(check)
        total_weight += w
        if check.result == "pass":
            pass_weight += w
    return SubjectScore(subject=subject, passWeight=pass_weight, totalWeight=total_weight)


def compute_all_subject_scores(check_results: list[CheckResult]) -> list[SubjectScore]:
    subjects = list(dict.fromkeys(c.subject for c in check_results))
    return [compute_subject_score(s, check_results) for s in subjects]


def compute_overall_score(subject_scores: list[SubjectScore]) -> tuple[float, str]:
    total_pass = sum(s.passWeight for s in subject_scores)
    total_weight = sum(s.totalWeight for s in subject_scores)
    if total_weight == 0:
        return 0.0, "Poor"
    score = round(total_pass / total_weight * 100, 2)
    return score, band_for_score(score)
