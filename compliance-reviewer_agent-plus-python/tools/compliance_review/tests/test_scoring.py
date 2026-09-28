import unittest

from tools.compliance_review.schemas import CheckResult
from tools.compliance_review.scoring import (
    band_for_score,
    compute_all_subject_scores,
    compute_overall_score,
    compute_subject_score,
)


def cr(subject, severity, result):
    return CheckResult(checkId="X", subject=subject, subSubject="Sub", severityIfFailed=severity, result=result)


class BandTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(band_for_score(90), "Excellent")
        self.assertEqual(band_for_score(89.99), "Good")
        self.assertEqual(band_for_score(75), "Good")
        self.assertEqual(band_for_score(74.99), "Fair")
        self.assertEqual(band_for_score(60), "Fair")
        self.assertEqual(band_for_score(59.99), "Poor")
        self.assertEqual(band_for_score(0), "Poor")


class SubjectScoreTests(unittest.TestCase):
    def test_na_excluded_from_denominator(self):
        checks = [
            cr("S", "Error", "pass"),   # weight 5, pass
            cr("S", "Warning", "fail"),  # weight 2, fail
            cr("S", "Information", "N/A"),  # excluded entirely
        ]
        score = compute_subject_score("S", checks)
        self.assertEqual(score.passWeight, 5)
        self.assertEqual(score.totalWeight, 7)
        self.assertAlmostEqual(score.score, 5 / 7 * 100, places=2)

    def test_all_na_yields_zero_not_error(self):
        checks = [cr("S", "Error", "N/A")]
        score = compute_subject_score("S", checks)
        self.assertEqual(score.totalWeight, 0)
        self.assertEqual(score.score, 0.0)

    def test_multiple_subjects_are_independent(self):
        checks = [cr("A", "Error", "pass"), cr("B", "Error", "fail")]
        scores = {s.subject: s for s in compute_all_subject_scores(checks)}
        self.assertEqual(scores["A"].score, 100.0)
        self.assertEqual(scores["B"].score, 0.0)


class OverallScoreTests(unittest.TestCase):
    def test_matches_sum_of_pass_over_sum_of_total(self):
        # Regression check against the hand-computed PilotUtilityApi run: builds a
        # CheckResult list per subject whose Error(5)/Warning(2)/Information(1)
        # weighted pass/fail counts reproduce the recorded pass/total weights.
        def make_weighted(subject, pass_w, fail_w):
            out = []
            for weight, sev in ((5, "Error"), (2, "Warning"), (1, "Information")):
                while pass_w >= weight:
                    out.append(cr(subject, sev, "pass"))
                    pass_w -= weight
                while fail_w >= weight:
                    out.append(cr(subject, sev, "fail"))
                    fail_w -= weight
            return out

        checks = []
        for subject, pass_w, total_w in [
            ("Software Quality", 23, 31),
            ("Software Lifecycle", 2, 15),
            ("Application Design", 13, 24),
            ("API Design", 19, 24),
            ("Security", 22, 51),
            ("Implementation", 35, 53),
            ("Operations", 15, 20),
        ]:
            checks.extend(make_weighted(subject, pass_w, total_w - pass_w))

        scores = compute_all_subject_scores(checks)
        overall, band = compute_overall_score(scores)
        self.assertAlmostEqual(overall, 59.17, places=1)
        self.assertEqual(band, "Poor")


if __name__ == "__main__":
    unittest.main()
