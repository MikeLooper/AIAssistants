"""Regression tests for label normalization in compliance_report.py (stdlib unittest).

Run: python -m unittest discover -s compliance-reviewer/skills/compliance-report/scripts
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compliance_report as cr  # noqa: E402

HEADER = {"schemaVersion": 1, "runId": "t", "status": "completed", "startedAt": "x", "completedAt": "x",
          "targetPath": "t", "targetGitHead": None, "inputsHash": "h"}


def check(cid, sub, subject, result="pass", sev="Warning", ids=()):
    return {"checkId": cid, "subject": subject, "subSubject": sub, "severityIfFailed": sev, "result": result,
            "findingIds": list(ids), **({"reason": "r"} if result != "pass" else {})}


class LabelTests(unittest.TestCase):
    def setUp(self):
        self.run = tempfile.mkdtemp()
        cr._CHECKLISTS.clear()

    def tearDown(self):
        shutil.rmtree(self.run)

    def write(self, name, data):
        with open(os.path.join(self.run, name), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def quiet(self, fn, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = fn(*args)
        return code, out.getvalue()

    def build(self, rel_subject="Operations / Reliability", rel_sub="Reliability", extra_check=None):
        self.write("state.json", {"runId": "t", "subjects": ["review-reliability", "review-performance"]})
        rel = [check(f"REL-0{i}", rel_sub, rel_subject) for i in range(1, 9)]
        rel[0] = check("REL-01", rel_sub, rel_subject, "fail", "Error", ["REL-01#1"])
        if extra_check:
            rel.append(extra_check)
        finding = {"id": "REL-01#1", "subject": rel_subject, "subSubject": rel_sub, "checkId": "REL-01",
                   "severity": "Error", "title": "No timeout", "standard": "S",
                   "evidence": [{"file": "a.cs", "lineStart": 1, "lineEnd": 2}]}
        self.write("22-review-reliability.json", dict(HEADER, stepId="22-review-reliability", skill="review-reliability",
                                                      subject=rel_subject, findings=[finding], strengths=[],
                                                      checkResults=rel))
        perf = [check(f"PERF-0{i}", "Performance", "Operations") for i in range(1, 9)]
        self.write("23-review-performance.json", dict(HEADER, stepId="23-review-performance", skill="review-performance",
                                                      subject="Operations", findings=[], strengths=[],
                                                      checkResults=perf))

    def test_checklists_lint_clean(self):
        code, out = self.quiet(cr.labels_lint, [])
        self.assertEqual(code, 0, out)

    def test_drift_warns_and_is_normalized(self):
        self.build()
        code, out = self.quiet(cr.validate, self.run)
        res = json.loads(out)
        self.assertTrue(res["ok"], res["problems"])
        self.assertTrue(any("should be" in w["problem"] for w in res["warnings"]))
        self.quiet(cr.aggregate, self.run)
        with open(os.path.join(self.run, "90-aggregate.json"), encoding="utf-8") as f:
            agg = json.load(f)
        self.assertEqual([s["subject"] for s in agg["subjectScores"]], ["Reliability", "Performance"])
        self.assertEqual(agg["findings"][0]["subSubject"], "Timeouts")
        self.assertGreater(agg["labelsNormalized"]["review-reliability"], 0)
        out_md = os.path.join(self.run, "report.md")
        self.quiet(cr.render, self.run, out_md)
        with open(out_md, encoding="utf-8") as f:
            report = f.read()
        self.assertIn("#### Timeouts", report)
        self.assertNotIn("#### Performance", report)  # sub-subject equal to its subject: no heading
        self.assertNotIn("Operations", report)

    def test_unknown_check_blocks_retired_warns(self):
        self.build(extra_check=check("REL-99", "X", "Reliability"))
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1)
        self.assertIn("unknown checkId 'REL-99'", out)
        cr._CHECKLISTS.clear()
        self.build(extra_check=check("SQ-07", "X", "Reliability"))
        cr._CHECKLISTS["review-reliability"] = dict(cr.load_checklist("review-reliability"))
        cr._CHECKLISTS["review-reliability"]["retired"] = {"SQ-07"}
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 0, out)
        self.assertIn("retired check SQ-07", out)

    def test_missing_check_result_blocks(self):
        self.build()
        path = os.path.join(self.run, "23-review-performance.json")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        d["checkResults"] = d["checkResults"][:-1]
        self.write("23-review-performance.json", d)
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1)
        self.assertIn("PERF-08", out)


if __name__ == "__main__":
    unittest.main()
