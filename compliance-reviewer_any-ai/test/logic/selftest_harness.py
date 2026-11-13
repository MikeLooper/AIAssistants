"""Offline self-tests for harness.py (no AI tool is run). python -m unittest selftest_harness (from test/logic)."""

import json
import re
import tempfile
import unittest
from pathlib import Path

import harness


def finding(fid, check, file, severity="Warning", line=1):
    return {"id": fid, "checkId": check, "severity": severity, "title": fid,
            "evidence": [{"file": file, "lineStart": line, "lineEnd": line, "excerpt": "x"}]}


def write_run(tmp: Path, subject_findings: dict, aggregate_findings: list, target="test/apis/dotNET") -> Path:
    run = tmp / "2026-11-11_1200-dotNET"
    run.mkdir()
    for i, (skill, fs) in enumerate(subject_findings.items()):
        (run / f"{10 + i}-{skill}.json").write_text(json.dumps({"skill": skill, "findings": fs}), encoding="utf-8")
    (run / "90-aggregate.json").write_text(json.dumps({"findings": aggregate_findings, "overallScore": 40,
                                                       "overallBand": "Poor"}), encoding="utf-8")
    (run / "state.json").write_text(json.dumps({"targetPath": target, "status": "completed"}), encoding="utf-8")
    return run


class AnswerKeyTests(unittest.TestCase):
    def test_every_app_has_twelve_flaws_with_checks(self):
        for kind in harness.KINDS:
            for lang in harness.LANGS:
                key = harness.load_app_key(kind, lang)
                self.assertEqual(len(key.flaws), 12, key.name)
                self.assertTrue(all(f.checks for f in key.flaws))

    def test_locations_exist_on_disk(self):
        for kind in harness.KINDS:
            for lang in harness.LANGS:
                key = harness.load_app_key(kind, lang)
                for f in key.flaws:
                    for loc in f.locations:
                        self.assertTrue((key.app_dir / loc).is_file(), f"{key.name} {f.id}: {loc}")

    def test_expected_checks_exist_in_the_checklists(self):
        skills = harness.REPO_ROOT / "compliance-reviewer" / "skills"
        known = set()
        for checklist in skills.glob("review-*/references/checklist.md"):
            for line in checklist.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\|\s*([A-Z]+(?:-[A-Z]+)*-\d+)\s*\|", line)
                if m:
                    known.add(m.group(1))
        self.assertIn("MCP-01", known)
        for kind in harness.KINDS:
            key = harness.load_app_key(kind, "dotNET")
            patterns = [c for f in key.flaws for c in f.checks] + key.incidental
            for p in patterns:
                self.assertTrue(any(harness.check_matches(k, [p]) for k in known), f"{kind}: unknown check {p}")

    def test_mcp_apps_use_stdio_only(self):
        signals = {"dotNET": ("TodoMcp.csproj", "Program.cs", "WithStdioServerTransport", "WithHttpTransport"),
                   "java": ("pom.xml", "src/main/java/com/example/todomcp/TodoMcpServer.java",
                            "StdioServerTransportProvider", "Streamable"),
                   "python": ("requirements.txt", "server.py", "mcp.run()", "streamable-http")}
        for lang, (manifest, entry, stdio, http) in signals.items():
            app = harness.TEST_DIR / "mcps" / lang
            self.assertTrue((app / manifest).is_file(), lang)
            source = (app / entry).read_text(encoding="utf-8")
            self.assertIn(stdio, source, lang)
            self.assertNotIn(http, source, lang)


class MatchingTests(unittest.TestCase):
    def test_check_wildcard_and_case(self):
        self.assertTrue(harness.check_matches("tst-07", ["TST-*"]))
        self.assertTrue(harness.check_matches("SEC-OP-05", ["SEC-OP-05"]))
        self.assertFalse(harness.check_matches("SEC-OP-050", ["SEC-OP-05"]))

    def test_location_suffix_and_separators(self):
        ev = [{"file": "C:\\repo\\test\\apis\\java\\src\\main\\resources\\application.properties"}]
        self.assertTrue(harness.location_matches(ev, ["src/main/resources/application.properties"]))
        self.assertFalse(harness.location_matches([{"file": "xapplication.properties"}], ["application.properties"]))
        self.assertTrue(harness.location_matches([], []))


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.key = harness.load_app_key("apis", "dotNET")

    def test_all_found_passes_and_classifies(self):
        hits = [finding(f"{f.id}#1", f.checks[0].replace("*", "07"), (f.locations or ["Program.cs"])[0])
                for f in self.key.flaws]
        extra = [finding("MAINT-01#1", "MAINT-01", "README.md", "Error"),        # incidental
                 finding("SEC-II-01#9", "SEC-II-01", "Other.cs", "Error"),        # related
                 finding("SQ-03#1", "SQ-03", "Program.cs", "Warning")]            # unexpected, warning
        run = harness.load_run(write_run(self.tmp, {"review-x": hits + extra}, hits + extra))
        s = harness.score_run(run, self.key, 90)
        self.assertEqual(len(s.found), 12)
        self.assertEqual([x["id"] for x in s.incidental], ["MAINT-01#1"])
        self.assertEqual([x["id"] for x in s.related], ["SEC-II-01#9"])
        self.assertEqual([x["id"] for x in s.unexpected_other], ["SQ-03#1"])
        self.assertTrue(s.passed)

    def test_threshold_and_unexpected_error(self):
        flaws = self.key.flaws[:10]  # 10/12 = 83% < 90%
        hits = [finding(f"{f.id}#1", f.checks[0].replace("*", "07"), (f.locations or ["x"])[0]) for f in flaws]
        bad = finding("PERF-01#1", "PERF-01", "Program.cs", "Error")
        run = harness.load_run(write_run(self.tmp, {"review-x": hits + [bad]}, hits + [bad]))
        s = harness.score_run(run, self.key, 90)
        self.assertEqual((len(s.found), s.required), (10, 11))
        self.assertFalse(s.coverage_ok)
        self.assertEqual(len(s.unexpected_errors), 1)
        self.assertTrue(harness.score_run(run, self.key, 80).coverage_ok)

    def test_raw_findings_count_even_when_deduplicated(self):
        a1 = finding("TF-03#1", "TF-03", "appsettings.json")
        run = harness.load_run(write_run(self.tmp, {"review-twelve-factor": [a1]}, []))
        s = harness.score_run(run, self.key, 90)
        self.assertIn("A1", [x["flaw"] for x in s.found])

    def test_wrong_location_does_not_count(self):
        a1 = finding("TF-03#1", "TF-03", "Program.cs")
        run = harness.load_run(write_run(self.tmp, {"review-twelve-factor": [a1]}, [a1]))
        s = harness.score_run(run, self.key, 90)
        self.assertNotIn("A1", [x["flaw"] for x in s.found])


class ProgressTests(unittest.TestCase):
    def test_read_progress(self):
        run = Path(tempfile.mkdtemp())
        (run / "state.json").write_text(json.dumps({
            "subjects": ["review-a", "review-b"],
            "steps": {"00-init": "completed", "01-inventory": "completed", "02-analyzers": "skipped",
                      "10-review-a": "in-progress"}}), encoding="utf-8")
        p = harness.read_progress(run)
        self.assertEqual((len(p["done"]), p["total"], p["current"]), (3, 7, "10-review-a"))
        (run / "state.json").write_text("{ half-written", encoding="utf-8")
        self.assertIsNone(harness.read_progress(run))

    def test_fmt_elapsed(self):
        self.assertEqual(harness._fmt_elapsed(65), "1m05s")
        self.assertEqual(harness._fmt_elapsed(3725), "1h02m05s")


class BuildOutputTests(unittest.TestCase):
    def test_clean_removes_outermost_build_folders_only(self):
        with tempfile.TemporaryDirectory() as d:
            app = Path(d)
            for sub in ("bin/Debug", "obj", "src/__pycache__", "target/classes/obj"):
                (app / sub).mkdir(parents=True)
            (app / "Program.cs").write_text("x", encoding="utf-8")
            self.assertEqual(sorted(harness.clean_build_output(app)), ["bin", "obj", "src/__pycache__", "target"])
            self.assertEqual(harness.find_build_output(app), [])
            self.assertTrue((app / "Program.cs").exists() and (app / "src").is_dir())

    def test_preflight_deletes_output_that_reappears(self):
        # Simulates IDE tooling restoring the project in place once, right after the first clean-up.
        with tempfile.TemporaryDirectory() as d:
            key = harness.AppKey("apis", "dotNET", [], [])
            app = Path(d)
            (app / "obj").mkdir()
            recreated = []
            real_clean = harness.clean_build_output

            def clean_then_ide_restores(p):
                removed = real_clean(p)
                if not recreated:
                    recreated.append(True)
                    (p / "obj").mkdir()
                return removed

            orig_dir, harness.clean_build_output = harness.AppKey.app_dir, clean_then_ide_restores
            harness.AppKey.app_dir = property(lambda self: app)
            try:
                self.assertIsNone(harness.preflight(key, attempts=3, settle_seconds=0))
                self.assertEqual(harness.find_build_output(app), [])
            finally:
                harness.AppKey.app_dir, harness.clean_build_output = orig_dir, real_clean

    def test_preflight_gives_up_when_output_keeps_coming_back(self):
        with tempfile.TemporaryDirectory() as d:
            key = harness.AppKey("apis", "dotNET", [], [])
            app = Path(d)
            (app / "bin").mkdir()
            orig_dir, real_clean = harness.AppKey.app_dir, harness.clean_build_output
            harness.AppKey.app_dir = property(lambda self: app)
            harness.clean_build_output = lambda p: []  # nothing can be removed
            try:
                err = harness.preflight(key, attempts=2, settle_seconds=0)
                self.assertIn("kept reappearing", err)
                self.assertIn("bin", err)
            finally:
                harness.AppKey.app_dir, harness.clean_build_output = orig_dir, real_clean

    def test_msbuild_output_is_redirected_out_of_the_apps(self):
        props = (harness.TEST_DIR / "Directory.Build.props").read_text(encoding="utf-8")
        self.assertIn("<BaseIntermediateOutputPath>", props)
        self.assertIn("<BaseOutputPath>", props)
        self.assertIn(".build-output", props)
        self.assertEqual(harness.redirected_output_dir(harness.TEST_DIR / "logic" / "results" / "build" / "apis-dotNET"),
                         harness.MSBUILD_OUTPUT_ROOT / "logic" / "results" / "build" / "apis-dotNET")
        self.assertIsNone(harness.redirected_output_dir(Path(tempfile.gettempdir())))

    def test_every_language_has_a_build_step(self):
        for lang in harness.LANGS:
            key = harness.AppKey("apis", lang, [], [])
            self.assertTrue(harness.build_steps(key), lang)


class ToolDetectionTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(harness.detect_tool("copilot", {"CLAUDECODE": "1"})[0], "copilot")
        self.assertEqual(harness.detect_tool(None, {"COMPLIANCE_TEST_TOOL": "copilot", "CLAUDECODE": "1"})[0], "copilot")
        self.assertEqual(harness.detect_tool("auto", {"CLAUDECODE": "1", "TERM_PROGRAM": "vscode"})[0], "claude")
        self.assertEqual(harness.detect_tool(None, {"TERM_PROGRAM": "vscode"})[0], "copilot")
        self.assertEqual(harness.detect_tool(None, {})[0], "claude")
        with self.assertRaises(ValueError):
            harness.detect_tool(None, {"COMPLIANCE_TEST_TOOL": "gpt"})

    def test_parse_status(self):
        text = 'noise {"a":1}\n{"status":"completed","runId":"r1","reportFile":"x.md","overallScore":41.5,"overallBand":"Poor"}\n'
        self.assertEqual(harness.parse_status(text)["runId"], "r1")
        self.assertIsNone(harness.parse_status("no json"))


if __name__ == "__main__":
    unittest.main()
