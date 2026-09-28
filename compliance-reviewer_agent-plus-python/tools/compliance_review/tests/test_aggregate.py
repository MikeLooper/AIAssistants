import unittest

from tools.compliance_review.aggregate import (
    dedup_findings,
    select_top_risks,
    severity_counts,
)
from tools.compliance_review.schemas import Evidence, Finding


def finding(id_, subject, sub_subject, severity, file_, line_start=0, line_end=0, confidence="High", effort="Small"):
    return Finding(
        id=id_, subject=subject, subSubject=sub_subject, checkId=id_.split("#")[0], severity=severity,
        title=f"title-{id_}", evidence=[Evidence(file=file_, lineStart=line_start, lineEnd=line_end)],
        confidence=confidence, effort=effort,
    )


class DedupTests(unittest.TestCase):
    def test_overlapping_evidence_keeps_higher_severity(self):
        a = finding("A#1", "Security", "Web & API", "Error", "f.cs", 10, 20)
        b = finding("B#1", "Application Design", "Twelve-Factor", "Warning", "f.cs", 12, 15)
        kept, dup = dedup_findings([a, b])
        self.assertEqual([f.id for f in kept], ["A#1"])
        self.assertEqual(dup[0].suppressedId, "B#1")
        self.assertEqual(dup[0].primaryId, "A#1")

    def test_tied_severity_keeps_earlier_pipeline_order(self):
        # Software Lifecycle runs before Testing in PIPELINE_ORDER.
        sl = finding("SL#1", "Software Lifecycle", "Software Lifecycle", "Error", ".github/workflows/")
        tst = finding("TST#1", "Implementation", "Testing", "Error", ".github/workflows/")
        kept, dup = dedup_findings([tst, sl])  # order in the input list shouldn't matter
        self.assertEqual([f.id for f in kept], ["SL#1"])
        self.assertEqual(dup[0].suppressedId, "TST#1")

    def test_non_overlapping_findings_both_kept(self):
        a = finding("A#1", "Security", "Web & API", "Error", "f.cs", 10, 20)
        b = finding("B#1", "Security", "Web & API", "Error", "f.cs", 30, 40)
        kept, dup = dedup_findings([a, b])
        self.assertEqual({f.id for f in kept}, {"A#1", "B#1"})
        self.assertEqual(dup, [])

    def test_merged_evidence_includes_both_locations(self):
        a = finding("A#1", "Security", "Web & API", "Error", "f.cs", 10, 20)
        b = finding("B#1", "Application Design", "Twelve-Factor", "Warning", "g.cs", 1, 5)
        b.evidence.append(Evidence(file="f.cs", lineStart=10, lineEnd=20))  # forces overlap with a
        kept, _dup = dedup_findings([a, b])
        primary = kept[0]
        files = {e.file for e in primary.evidence}
        self.assertIn("f.cs", files)
        self.assertIn("g.cs", files)


class SeverityCountTests(unittest.TestCase):
    def test_counts_by_severity(self):
        findings = [
            finding("A#1", "S", "X", "Error", "f"),
            finding("B#1", "S", "X", "Warning", "f", 100, 100),
            finding("C#1", "S", "X", "Warning", "g"),
        ]
        counts = severity_counts(findings)
        self.assertEqual(counts, {"Error": 1, "Warning": 2, "Information": 0})


class TopRisksTests(unittest.TestCase):
    def test_error_before_warning_high_confidence_before_low(self):
        low_conf_error = finding("A#1", "S", "X", "Error", "f", confidence="Low")
        high_conf_error = finding("B#1", "S", "X", "Error", "g", confidence="High")
        warning = finding("C#1", "S", "X", "Warning", "h", confidence="High")
        ranked = select_top_risks([low_conf_error, warning, high_conf_error], limit=3)
        self.assertEqual([f.id for f in ranked], ["B#1", "A#1", "C#1"])

    def test_effort_breaks_ties(self):
        small = finding("A#1", "S", "X", "Error", "f", effort="Small")
        large = finding("B#1", "S", "X", "Error", "g", effort="Large")
        ranked = select_top_risks([large, small], limit=2)
        self.assertEqual([f.id for f in ranked], ["A#1", "B#1"])


if __name__ == "__main__":
    unittest.main()
