"""Regression tests for compliance_report.py: labels, compact schema, citations, scripted steps, redaction and
the secret/personal-data pattern pass (stdlib unittest).

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


def v2_file(skill, step, checks, findings=(), strengths=()):
    return dict(HEADER, schemaVersion=2, stepId=f"{step}-{skill}", batchId="batch-1", skill=skill,
                findings=list(findings), strengths=list(strengths), checks=checks)


class CompactSchemaTests(unittest.TestCase):
    """schemaVersion 2: compact checks, element-only citations, labels and severities from the checklist."""

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

    def api_checks(self, **override):
        ids = list(cr.load_checklist("review-api-design")["checks"])
        checks = {"pass": [i for i in ids if i not in ("API-05", "API-13")],
                  "fail": {"API-05": {"findingIds": ["API-05#1"]}},
                  "na": {"API-13": "no long-running operations"}}
        checks.update(override)
        return checks

    def finding(self, **kw):
        f = {"id": "API-05#1", "checkId": "API-05", "element": "AZ-031", "severity": "Error",
             "title": "Non-standard status codes", "recommendation": "Use standard codes.",
             "confidence": "High", "effort": "Small",
             "evidence": [{"file": "Program.cs", "lineStart": 10, "lineEnd": 12, "excerpt": "x"}]}
        f.update(kw)
        return f

    def test_compact_file_validates_and_scores(self):
        self.write("state.json", {"runId": "t", "subjects": ["review-api-design"]})
        self.write("13-review-api-design.json", v2_file("review-api-design", "13", self.api_checks(), [self.finding()]))
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(out)["warnings"], [])
        self.quiet(cr.aggregate, self.run)
        with open(os.path.join(self.run, "90-aggregate.json"), encoding="utf-8") as f:
            agg = json.load(f)
        f0 = agg["findings"][0]
        self.assertEqual(f0["standard"], "Microsoft Azure REST API Guidelines — AZ-031")
        self.assertTrue(f0["url"].startswith("https://github.com/microsoft/api-guidelines/blob/"))
        self.assertTrue(f0["url"].endswith("#rest-use-standard-status-codes"))
        self.assertEqual((f0["subject"], f0["subSubject"]), ("API Design", "Status Codes & Errors"))
        self.assertEqual(agg["labelsNormalized"]["review-api-design"], 0)
        score = agg["subjectScores"][0]
        cl = cr.load_checklist("review-api-design")
        weights = {c: cr.SEV_WEIGHT[s] for c, s in cl["severities"].items() if c != "API-13"}
        self.assertEqual(score["totalWeight"], sum(weights.values()))
        self.assertEqual(score["passWeight"], sum(weights.values()) - weights["API-05"])

    def test_explicit_citation_wins_and_unknown_element_warns(self):
        self.write("state.json", {"runId": "t", "subjects": ["review-api-design"]})
        f = self.finding(element="ZZ-999")
        g = self.finding(id="API-05#2", element=None, standard="Custom", url="https://example.com/x",
                         evidence=[{"file": "Other.cs", "lineStart": 1, "lineEnd": 2}])
        checks = self.api_checks(fail={"API-05": {"findingIds": ["API-05#1", "API-05#2"]}})
        self.write("13-review-api-design.json", v2_file("review-api-design", "13", checks, [f, g]))
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 0, out)
        self.assertIn("ZZ-999", out)
        results = cr.load_results(self.run)
        by_id = {x["id"]: x for x in results[0]["findings"]}
        self.assertEqual(by_id["API-05#1"]["standard"], "ZZ-999")
        self.assertEqual(by_id["API-05#2"]["url"], "https://example.com/x")

    def test_check_in_two_buckets_or_missing_blocks(self):
        self.write("state.json", {"runId": "t", "subjects": ["review-api-design"]})
        checks = self.api_checks()
        checks["na"]["API-01"] = "duplicate"
        self.write("13-review-api-design.json", v2_file("review-api-design", "13", checks, [self.finding()]))
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1)
        self.assertIn("API-01 is listed under both", out)
        checks = self.api_checks()
        checks["pass"].remove("API-02")
        self.write("13-review-api-design.json", v2_file("review-api-design", "13", checks, [self.finding()]))
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1)
        self.assertIn("API-02", out)

    def test_oas_page_hint_picks_version(self):
        self.assertTrue(cr.standards.resolve("review-api-design", "OAS-39", "3.1.x")[1]
                        .startswith("https://spec.openapis.org/oas/v3.1.2.html#"))
        self.assertTrue(cr.standards.resolve("review-api-design", "OAS-39")[1]
                        .startswith("https://spec.openapis.org/oas/v3.0.4.html#"))


class CitationTests(unittest.TestCase):
    def test_every_active_element_resolves(self):
        self.assertEqual(cr.standards.citations_lint(), [])

    def test_formats(self):
        r = cr.standards.resolve
        self.assertEqual(r("review-disaster-recovery", "SP34-01")[1],
                         "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=35")
        self.assertEqual(r("review-maintainability", "MR-14"),
                         ("Compliance Reviewer Maintainability Rubric — MR-14",
                          "../../compliance-reviewer/skills/review-maintainability/references/standards/"
                          "maintainability-rubric.md#mr-14"))
        self.assertEqual(r("review-twelve-factor", "TFA-01")[1], "https://12factor.net/codebase")
        self.assertEqual(r("review-software-quality", "PEP-22")[0], "PEP 257 — PEP-22")
        self.assertEqual(r("review-performance", "AZPE-01")[0], "Azure Architecture Center — AZPE-01")
        self.assertEqual(r("review-mcp-server", "MCPS-01")[1],
                         "https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio")
        self.assertIsNone(r("review-api-design", "NOPE-1"))

    def test_resolution_is_scoped_to_the_citing_skill(self):
        r = cr.standards.resolve
        self.assertIsNotNone(r("review-reliability", "AZRL-32"))
        self.assertIsNone(r("review-api-design", "AZRL-32"))  # owned by review-reliability only

    def test_cross_skill_element_warns_and_cites_plain_text(self):
        entry, warnings = {"id": "F-1", "element": "AZRL-32"}, []
        cr.cite(entry, "review-api-design", warnings)
        self.assertEqual((entry["standard"], entry["url"]), ("AZRL-32", ""))
        self.assertEqual(len(warnings), 1)
        self.assertIn("not in review-api-design's standards", warnings[0])


def luhn_number(prefix):
    """A Luhn-valid card number built at run time (no card-like literal in the source)."""
    scan = cr.scanner()
    return next(prefix + str(d) for d in range(10) if scan.luhn(prefix + str(d)))


FAKE_AWS = "AKIA" + "ZQ4T7FAKEKEY2B9X"          # pattern-valid, clearly fake, not on the allowlist
FAKE_GH = "ghp_" + "Fake0Token0For0Unit0Tests0Only0000000"


class SecretPatternTests(unittest.TestCase):
    """secret-patterns.json via sensitive_scan: true positives, placeholders, allowlist, PII checks, masking."""

    def setUp(self):
        self.s = cr.scanner()

    def test_true_positives(self):
        hits = self.s.excerpt_hits
        self.assertIn("aws-access-key-id", hits(f'key = "{FAKE_AWS}"'))
        self.assertIn("github-token", hits(f"token: {FAKE_GH}"))
        self.assertIn("secret-assignment", hits('"ApiKey": "s3cr3t-value"', "appsettings.json"))
        self.assertIn("connection-string-password", hits('"Server=db;User Id=sa;Password=Hunter2x;"'))
        self.assertIn("config-secret-assignment", hits("DB_PASSWORD=Hunter2x", ".env"))
        self.assertIn("private-key-block", hits("-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAx1y2z3"))
        self.assertIn("jwt", hits("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NSJ9.c2lnbmF0dXJlLXZhbHVl"))

    def test_placeholders_allowlist_and_header_only(self):
        hits = self.s.excerpt_hits
        for text in ('"ApiKey": "${API_KEY}"', '"ApiKey": "<redacted:api-key>"', 'password = "changeme"',
                     'password: "your-password-here"', '"ClientSecret": "<secret>"', "token: str",
                     "key = AKIAIOSFODNN7EXAMPLE", "-----BEGIN PRIVATE KEY-----"):
            self.assertEqual(hits(text, "config.yml"), [], text)

    def test_pii_rules(self):
        hits = self.s.excerpt_hits
        card = luhn_number("492900001234567")
        self.assertIn("payment-card-number", hits(f'"cardNumber": "{card}"'))
        self.assertEqual(hits('"cardNumber": "4242424242424242"'), [])          # published test number
        broken = card[:-1] + str((int(card[-1]) + 1) % 10)
        self.assertEqual(hits(f'"cardNumber": "{broken}"'), [])                # Luhn fails
        self.assertIn("iban", hits("iban: DE44500105175407324931"))
        self.assertEqual(hits("iban: DE44500105175407324932"), [])             # bad checksum
        self.assertEqual(hits("email: jane@example.com"), [])                  # emails aren't excerpt problems

    def test_mask_keeps_key_names(self):
        masked = self.s.mask(f'"AwsKey": "{FAKE_AWS}", "Password": "Hunter2x"', "appsettings.json")
        self.assertNotIn(FAKE_AWS, masked)
        self.assertNotIn("Hunter2x", masked)
        self.assertIn('"AwsKey": "<redacted:', masked)
        self.assertEqual(self.s.excerpt_hits(masked, "appsettings.json"), [])

    def test_scan_target_never_stores_values_and_skips_binaries(self):
        tmp = tempfile.mkdtemp()
        try:
            files = {"src/settings.py": f'AWS_KEY = "{FAKE_AWS}"\n',
                     "tests/fixtures/users.json": '{"email": "maria.rossi@realmail.it",\n "card": "' +
                                                  luhn_number("453201511283036") + '"}',
                     "package-lock.json": f'"{FAKE_AWS}"', "certs/server.pfx": None,
                     ".env": "API_TOKEN=abcd1234efgh\n", ".env.example": "API_TOKEN=abcd1234efgh\n", "bin.dat": None}
            for rel, text in files.items():
                path = os.path.join(tmp, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(b"\0\1\2" + FAKE_AWS.encode() if text is None else text.encode())

            class T:
                root = tmp
            secrets, _s_total, pii, _p_total = self.s.scan_target(T, sorted(files), ["tests/fixtures/users.json"])
            by_file = {c["file"]: c for c in secrets}
            self.assertEqual(by_file["src/settings.py"]["rule"], "aws-access-key-id")
            self.assertEqual(by_file["src/settings.py"]["confidence"], "high")
            self.assertIsNone(by_file["certs/server.pfx"]["line"])                 # binary key file: name only
            self.assertIn(".env", by_file)
            self.assertNotIn(".env.example", by_file)
            self.assertNotIn("package-lock.json", by_file)                         # lock files skipped
            self.assertNotIn("bin.dat", by_file)                                   # binaries skipped
            self.assertEqual({c["rule"] for c in pii}, {"payment-card-number", "email-address"})
            self.assertNotIn(FAKE_AWS, json.dumps(secrets))
            self.assertTrue(all(set(c) == {"file", "line", "rule", "confidence"} for c in secrets + pii))
        finally:
            shutil.rmtree(tmp)


class RedactionTests(unittest.TestCase):
    """Phase 1: validate rejects excerpts and free-text fields with secrets; aggregate and render mask them."""

    def setUp(self):
        self.run = tempfile.mkdtemp()
        cr._CHECKLISTS.clear()

    def tearDown(self):
        shutil.rmtree(self.run)

    def quiet(self, fn, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = fn(*args)
        return code, out.getvalue()

    def write_run(self, excerpt, title, recommendation="Move it to a secret store.", fail_reason=None,
                  na_reason=None):
        skill = "review-security-operational"
        ids = list(cr.load_checklist(skill)["checks"])
        finding = {"id": "SEC-OP-05#1", "checkId": "SEC-OP-05", "element": "SMG-02", "severity": "Error",
                   "title": title, "recommendation": recommendation,
                   "confidence": "High", "effort": "Small",
                   "evidence": [{"file": "appsettings.json", "lineStart": 3, "lineEnd": 3, "excerpt": excerpt}]}
        fail = {"findingIds": ["SEC-OP-05#1"]}
        if fail_reason:
            fail["reason"] = fail_reason
        passed = [i for i in ids if i != "SEC-OP-05"]
        checks = {"pass": passed, "fail": {"SEC-OP-05": fail}}
        if na_reason:
            checks["pass"], checks["na"] = passed[1:], {passed[0]: na_reason}
        cr.write_json(os.path.join(self.run, "state.json"), {"runId": "t", "subjects": [skill], "targetPath": "t"})
        cr.write_json(os.path.join(self.run, "17-review-security-operational.json"),
                      v2_file(skill, "17", checks, [finding]))

    def test_secret_in_excerpt_fails_validate_and_renders_masked(self):
        self.write_run(f'"AwsKey": "{FAKE_AWS}"', f"Hardcoded AWS key {FAKE_AWS}")
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1)
        self.assertIn("aws-access-key-id", out)
        self.assertNotIn(FAKE_AWS, out)
        self.quiet(cr.aggregate, self.run)
        agg = cr.read_json(os.path.join(self.run, "90-aggregate.json"))
        self.assertNotIn(FAKE_AWS, json.dumps(agg))
        out_md = os.path.join(self.run, "report.md")
        self.quiet(cr.render, self.run, out_md)
        with open(out_md, encoding="utf-8") as f:
            report = f.read()
        self.assertNotIn(FAKE_AWS, report)
        self.assertIn("<redacted:api-key>", report)

    def test_redacted_excerpt_passes(self):
        self.write_run('"AwsKey": "<redacted:api-key>"', "Hardcoded AWS key")
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 0, out)

    def assert_blocked(self, field, rule, value):
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 1, out)
        self.assertIn(f"{field} contains a secret or personal-data value", out)
        self.assertIn(rule, out)
        self.assertNotIn(value, out)

    def test_secret_in_title_fails_validate(self):
        self.write_run('"AwsKey": "<redacted:api-key>"', f"Hardcoded AWS key {FAKE_AWS}")
        self.assert_blocked("title", "aws-access-key-id", FAKE_AWS)

    def test_personal_data_in_recommendation_fails_validate(self):
        card = luhn_number("492900001234567")
        self.write_run('"AwsKey": "<redacted:api-key>"', "Hardcoded AWS key",
                       recommendation=f"Remove the test card {card} from the seed data.")
        self.assert_blocked("recommendation", "payment-card-number", card)

    def test_secret_in_fail_reason_fails_validate(self):
        self.write_run('"AwsKey": "<redacted:api-key>"', "Hardcoded AWS key",
                       fail_reason=f"The key {FAKE_GH} is committed in plain text.")
        self.assert_blocked("reason", "github-token", FAKE_GH)

    def test_personal_data_in_na_reason_fails_validate(self):
        self.write_run('"AwsKey": "<redacted:api-key>"', "Hardcoded AWS key",
                       na_reason="Not applicable; the only account is iban: DE44500105175407324931.")
        self.assert_blocked("reason", "iban", "DE44500105175407324931")

    def test_prose_mentioning_secrets_passes(self):
        self.write_run('"Password": "<redacted:password>"', "Hard-coded password in appsettings.json",
                       recommendation="Move the password and connection string to a secret store such as Key Vault.",
                       fail_reason="A database password is stored in a committed config file.",
                       na_reason="No API keys or tokens are used by this service.")
        code, out = self.quiet(cr.validate, self.run)
        self.assertEqual(code, 0, out)


class InventoryAndRunTests(unittest.TestCase):
    """Scripted steps 00/01, N/A files, dispatch payloads, validate --mark and resume."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.target = os.path.join(self.tmp, "app")
        files = {
            "Program.cs": "var app = WebApplication.CreateBuilder(args).Build();\n"
                          "app.MapGet(\"/todos\", () => Results.Ok());\napp.UseExceptionHandler(\"/error\");\n"
                          "var key = builder.Configuration[\"ApiKey\"];\napp.Run();\n",
            "Todo.csproj": "<Project Sdk=\"Microsoft.NET.Sdk.Web\"><ItemGroup>"
                           "<PackageReference Include=\"Swashbuckle.AspNetCore\" Version=\"6.0.0\" /></ItemGroup></Project>",
            "appsettings.json": "{\"ApiKey\": \"secret\", \"Logging\": {}}",
            "README.md": "# Todo\n",
            "obj/generated.cs": "// should be excluded",
            "tests/Todo.Tests/Todo.Tests.csproj": "<Project Sdk=\"Microsoft.NET.Sdk\"></Project>",
            "tests/Todo.Tests/TodoTests.cs": "using Xunit; public class T { [Fact] public void A() {} }",
            "infra/main.bicep": "resource sa 'Microsoft.Storage/storageAccounts@2023-01-01' = {}",
            "scripts/deploy/legacy/upload.sh": "export AWS_ACCESS_KEY_ID=" + FAKE_AWS + "\n",
        }
        for rel, text in files.items():
            path = os.path.join(self.target, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        self.transitions = os.path.join(self.tmp, "transitions")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_cmd(self, fn, *args, **kw):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = fn(*args, **kw)
        text = out.getvalue()
        try:
            return code, [json.loads(text)]
        except ValueError:
            return code, [json.loads(x) for x in text.splitlines() if x.strip().startswith("{")]

    def test_full_scripted_flow(self):
        code, out = self.run_cmd(cr.init_run, self.target, "all", "off", "auto", None, "r1",
                                 transitions_dir=self.transitions)
        self.assertEqual(code, 0, out)
        run = os.path.join(self.transitions, "r1")
        code, out = self.run_cmd(cr.run_inventory, run)
        self.assertEqual(code, 0, out)
        inv = cr.read_json(os.path.join(run, "01-inventory.json"))
        self.assertEqual(inv["schemaVersion"], 2)
        self.assertEqual(inv["languages"], ["csharp"])
        self.assertIn("ASP.NET Core", inv["frameworks"])
        self.assertTrue(inv["apiSpecsFound"])
        self.assertFalse(inv["iacFound"])  # advanced off: the Bicep file is out of scope
        self.assertEqual(inv["skippedSubjects"]["review-disaster-recovery"], "advanced usage off (IaC not reviewed)")
        self.assertEqual(inv["skippedSubjects"]["review-mcp-server"], "no MCP server found")
        all_files = {f for b in inv["fileBatches"] for fl in b["subjectFiles"].values() for f in fl}
        self.assertNotIn("infra/main.bicep", all_files)
        self.assertNotIn("obj/generated.cs", all_files)
        placed = [s for b in inv["fileBatches"] for s in b["subjects"]]
        self.assertEqual(len(placed), len(set(placed)))
        testing = next(b["subjectFiles"]["review-testing"] for b in inv["fileBatches"]
                       if "review-testing" in b["subjectFiles"])
        self.assertIn("tests/Todo.Tests/TodoTests.cs", testing)
        for b in inv["fileBatches"]:
            for skill, fl in b["subjectFiles"].items():
                if skill not in ("review-testing", "review-dependency-management"):
                    self.assertFalse([f for f in fl if f.startswith("tests/")], skill)
        self.assertEqual(inv["testInventory"]["totals"]["unit"], 1)
        self.assertTrue(inv["testInventory"]["signals"]["untrustedInput"])
        state = cr.read_json(os.path.join(run, "state.json"))
        self.assertEqual(state["steps"]["02-analyzers"], "skipped")

        # secret candidates: values never stored; IaC skipped with advanced off; no personal data -> N/A
        cands = {c["file"]: c for c in inv["secretCandidates"]}
        self.assertEqual(cands["scripts/deploy/legacy/upload.sh"]["confidence"], "high")
        self.assertIn("appsettings.json", cands)
        self.assertNotIn(FAKE_AWS, json.dumps(inv))
        self.assertFalse(inv["personalDataFound"])
        self.assertEqual(inv["skippedSubjects"]["review-data-protection"], "no personal data found")
        # a gitleaks report in the run folder is merged into the candidates (deduplicated by file and line)
        cr.write_json(os.path.join(run, cr.GITLEAKS_RAW), [
            {"File": os.path.join(self.target, "scripts", "deploy", "legacy", "upload.sh"), "StartLine": 1,
             "RuleID": "aws-access-token", "Secret": "REDACTED", "Match": "REDACTED"},
            {"File": "Program.cs", "StartLine": 4, "RuleID": "generic-api-key", "Secret": "REDACTED"}])

        code, out = self.run_cmd(cr.write_na, run)
        self.assertIn("24-review-disaster-recovery.json", out[0]["written"])
        self.assertIn("29-review-data-protection.json", out[0]["written"])
        code, payloads = self.run_cmd(cr.dispatch, run)
        secop = next(s for p in payloads for s in p["subjects"] if s["skill"] == "review-security-operational")
        keys = [(c["file"], c["line"]) for c in secop["secretCandidates"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn(("Program.cs", 4), keys)
        self.assertEqual(secop["secretCandidatesTotal"], len(keys))
        self.assertEqual(len(payloads), len(inv["fileBatches"]))
        first = payloads[0]["subjects"][0]
        self.assertTrue(first["out"].endswith(f"{first['stepId']}.json"))
        self.assertTrue(all(p.startswith("compliance-reviewer/packs/") for p in first["packs"]))

        # a worker writes every dispatched subject as all-pass (compact schema)
        for p in payloads:
            for s in p["subjects"]:
                ids = list(cr.load_checklist(s["skill"])["checks"])
                doc = dict(p["header"], stepId=s["stepId"], status="completed", completedAt="x",
                           batchId=p["batchId"], skill=s["skill"], findings=[], strengths=[], checks={"pass": ids})
                cr.write_json(s["out"], doc)
        code, out = self.run_cmd(cr.validate, run, True)
        self.assertEqual(code, 0)
        state = cr.read_json(os.path.join(run, "state.json"))
        self.assertTrue(all(v in ("completed", "skipped") for k, v in state["steps"].items()
                            if k not in ("90-aggregate", "99-report")), state["steps"])
        code, _ = self.run_cmd(cr.aggregate, run)
        self.assertEqual(code, 0)
        self.assertEqual(cr.read_json(os.path.join(run, "90-aggregate.json"))["overallScore"], 100.0)

        # resume from a subject step supersedes its whole batch
        sibling = payloads[0]["subjects"]
        nn = cr.step_number(sibling[-1]["stepId"])
        code, out = self.run_cmd(cr.resume_run, run, str(nn))
        moved = set(out[0]["superseded"])
        self.assertTrue({f"{s['stepId']}.json" for s in sibling} <= moved)
        self.assertIn("90-aggregate.json", moved)
        self.assertFalse(out[0]["inputsHashChanged"])

    def test_personal_data_makes_data_protection_applicable(self):
        extra = {"Models/Customer.cs": "public class Customer { public string Email { get; set; } "
                                       "public string CardNumber { get; set; } }",
                 "tests/Todo.Tests/fixtures/customers.json": '[{"name": "Maria Rossi", "card": "' +
                                                              luhn_number("453201511283036") + '"}]'}
        for rel, text in extra.items():
            path = os.path.join(self.target, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        self.run_cmd(cr.init_run, self.target, "review-data-protection,review-security-operational", "off", "auto",
                     None, "r5", transitions_dir=self.transitions)
        run = os.path.join(self.transitions, "r5")
        code, out = self.run_cmd(cr.run_inventory, run)
        self.assertEqual(code, 0, out)
        self.assertTrue(out[0]["personalDataFound"])
        inv = cr.read_json(os.path.join(run, "01-inventory.json"))
        self.assertNotIn("review-data-protection", inv["skippedSubjects"])
        self.assertEqual(inv["piiCandidates"][0]["rule"], "payment-card-number")
        signals = {s["signal"] for s in inv["personalDataSignals"]}
        self.assertIn("personal-data fields", signals)
        code, payloads = self.run_cmd(cr.dispatch, run)
        dp = next(s for p in payloads for s in p["subjects"] if s["skill"] == "review-data-protection")
        self.assertEqual(dp["stepId"], "29-review-data-protection")
        self.assertTrue(dp["piiCandidates"])
        self.assertIn("Models/Customer.cs", dp["files"])
        self.assertIn("tests/Todo.Tests/fixtures/customers.json", dp["files"])

    def test_all_subjects_na_renders_na_overall_score(self):
        # Data Protection only, on a target without personal data: the only subject is N/A, so no check applies
        self.run_cmd(cr.init_run, self.target, "review-data-protection", "off", "auto", None, "r6",
                     transitions_dir=self.transitions)
        run = os.path.join(self.transitions, "r6")
        code, out = self.run_cmd(cr.run_inventory, run)
        self.assertEqual(code, 0, out)
        self.assertFalse(out[0]["personalDataFound"])
        self.run_cmd(cr.write_na, run)
        code, out = self.run_cmd(cr.validate, run, True)
        self.assertEqual(code, 0, out)
        with contextlib.redirect_stdout(io.StringIO()) as log:
            self.assertEqual(cr.aggregate(run), 0)
        self.assertIn("overall N/A N/A", log.getvalue())
        agg = cr.read_json(os.path.join(run, "90-aggregate.json"))
        self.assertIsNone(agg["overallScore"])
        self.assertEqual(agg["overallBand"], "N/A")
        report_path = os.path.join(self.tmp, "reports", "app-compliance-review.md")
        with contextlib.redirect_stdout(io.StringIO()) as log:
            self.assertEqual(cr.render(run, report_path), 0)
        self.assertIn("overall N/A N/A", log.getvalue())
        with open(report_path, encoding="utf-8") as f:
            report = f.read()
        self.assertIn("**Overall score: N/A — N/A**", report)
        self.assertIn("| Data Protection | N/A | N/A |", report)
        self.assertNotIn("/100", report)
        self.assertNotIn("None", report)

    def test_init_rejects_out_file_inside_target_and_unknown_subject(self):
        code, out = self.run_cmd(cr.init_run, self.target, "all", "off", "auto",
                                 os.path.join(self.target, "r.md"), "r2", transitions_dir=self.transitions)
        self.assertEqual(code, 1)
        self.assertIn("inside the target", out[0]["error"])
        code, out = self.run_cmd(cr.init_run, self.target, "review-nope", "off", "auto", None, "r3",
                                 transitions_dir=self.transitions)
        self.assertEqual(code, 1)

    def test_picks_replace_a_subject_list(self):
        self.run_cmd(cr.init_run, self.target, "review-maintainability", "off", "auto", None, "r4",
                     transitions_dir=self.transitions)
        run = os.path.join(self.transitions, "r4")
        picks = os.path.join(self.tmp, "picks.json")
        cr.write_json(picks, {"review-maintainability": ["README.md"]})
        code, out = self.run_cmd(cr.run_inventory, run, picks)
        self.assertEqual(code, 0, out)
        inv = cr.read_json(os.path.join(run, "01-inventory.json"))
        self.assertEqual(inv["fileBatches"][0]["subjectFiles"]["review-maintainability"], ["README.md"])
        cr.write_json(picks, {"review-maintainability": ["missing.md"]})
        code, out = self.run_cmd(cr.run_inventory, run, picks)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
