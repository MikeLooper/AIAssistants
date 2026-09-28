import unittest

from tools.compliance_review.aggregate import AggregateResult
from tools.compliance_review.report import build_context, render, render_report
from tools.compliance_review.scoring import SubjectScore


class RendererTests(unittest.TestCase):
    def test_scalar_and_nested_sections(self):
        template = (
            "{{title}}\n"
            "{{#items}}- {{name}}\n{{#tags}}  * {{tag}}\n{{/tags}}{{/items}}"
        )
        context = {
            "title": "Report",
            "items": [
                {"name": "a", "tags": [{"tag": "x"}, {"tag": "y"}]},
                {"name": "b", "tags": []},
            ],
        }
        out = render(template, context)
        self.assertIn("Report", out)
        self.assertIn("- a", out)
        self.assertIn("  * x", out)
        self.assertIn("  * y", out)
        self.assertIn("- b", out)

    def test_empty_list_section_renders_nothing(self):
        out = render("before{{#items}}X{{/items}}after", {"items": []})
        self.assertEqual(out, "beforeafter")


class RenderReportSmokeTest(unittest.TestCase):
    def test_render_report_does_not_crash_on_empty_run(self):
        aggregate = AggregateResult(
            overallScore=0.0, overallBand="Poor",
            subjectScores=[SubjectScore(subject="Security", passWeight=0, totalWeight=0)],
            severityCounts={"Error": 0, "Warning": 0, "Information": 0},
            findings=[], strengths=[], topRisks=[], duplicatesSuppressed=[],
        )
        context = build_context(
            aggregate, target_name="demo", generated_at="now", run_id="r1", target_path="/x",
            target_git_head=None, started_at="t0", completed_at="t1",
            skipped_subjects={}, urls_fetched=[], link_approvals={}, full_results=[],
        )
        report = render_report(context)
        self.assertIn("demo", report)
        self.assertIn("Overall score: 0.0/100", report)


if __name__ == "__main__":
    unittest.main()
