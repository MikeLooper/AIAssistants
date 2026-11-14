"""Offline self-tests for harness.py and answer_key.json (no AI tool is run, no cost).

Run from test/logic:  python -m unittest selftest_harness
"""

import re
import tempfile
import unittest
from pathlib import Path

import harness

# A stage-3 audit in the agent's format (see .github/skills/unit-test-coverage-test-assertion-audit/SKILL.md and
# example-runs/) that reports every seeded gap and classifies every control path as Covered.
PERFECT_AUDIT_DOTNET = """
# Stage 3 — Test Assertion Audit — Run 20261114-120000

- **Run ID**: 20261114-120000
- **Target root**: test/apis/dotNET

## TodoApi — 24 paths

### TodoService.cs vs TodoServiceTests.cs

#### `CreateTodo(string? title, int priority)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | title null/empty/whitespace | `CreateTodo_BlankTitle_ThrowsValidationException` | Strong (exception type + message) | Covered | — |
| P-02 | trimmed title length > 100 | — | — | Uncovered | No test with a long title |
| P-03 | `priority < 1 || priority > 5` | `CreateTodo_PriorityZero_ThrowsValidationException` | Strong | Partially Covered | Only priority < 1 exercised |
| P-04 | valid input -> repository.Add(trimmed item) | `CreateTodo_ValidInput_StoresTrimmedItem` | Strong | Covered | — |

#### `CompleteTodo(int id)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | FindById returns null -> NotFoundException | — | — | Uncovered | — |
| P-02 | item already completed -> returned unchanged | `CompleteTodo_AlreadyCompleted_ReturnsItem` | Weak (NotNull only) | Partially Covered | — |
| P-03 | item open -> IsCompleted = true | `CompleteTodo_OpenItem_MarksItCompleted` | Strong | Covered | — |

#### `ListTodos(bool includeCompleted, int? minPriority)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | includeCompleted == false -> completed filtered out | `ListTodos_Default_ExcludesCompletedItemsAndSortsByPriority` | Strong | Covered | — |
| P-02 | includeCompleted == true -> all items | `ListTodos_IncludeCompleted_ReturnsAllItemsSortedByPriority` | Strong | Covered | — |
| P-03 | minPriority has a value -> Priority >= min filter | — | — | Uncovered | — |
| P-04 | minPriority null -> no priority filter | `ListTodos_Default_ExcludesCompletedItemsAndSortsByPriority` | Strong | Covered | — |

#### `DeleteTodo(int id)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | Remove returns false -> NotFoundException | `DeleteTodo_MissingItem_ThrowsNotFoundException` | Strong | Covered | — |
| P-02 | Remove returns true -> item deleted | `DeleteTodo_ExistingItem_Deletes` | Absent | Uncovered | Execution without verification |

#### `RenameTodo(int id, string? newTitle)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | newTitle null/whitespace -> ValidationException | `RenameTodo_BlankTitle_ThrowsValidationException` | Strong | Covered | — |
| P-02 | FindById returns null -> NotFoundException | — | — | Uncovered | Mock bypass: `FindById(It.IsAny<int>())` always returns an item |
| P-03 | item found -> title trimmed and set | `RenameTodo_ValidTitle_UpdatesTitle` | Strong | Partially Covered | Mock bypass risk |

#### `PriorityLabel(int priority)`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | priority 1 or 2 -> "low" | `PriorityLabel_ReturnsLabel(1|2)` | Strong | Covered | — |
| P-02 | priority 3 -> "medium" | — | — | Uncovered | — |
| P-03 | priority 4 or 5 -> "high" | `PriorityLabel_ReturnsLabel(4, 5)` | Strong | Covered | — |
| P-04 | any other value -> "unknown" (default arm) | — | — | Uncovered | — |

### InMemoryTodoRepository.cs vs InMemoryTodoRepositoryTests.cs
| Path ID | Method | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|--------|-----------|--------------|--------------------|----------------|-------|
| P-01 | FindById | id present | `FindById_ExistingItem_ReturnsIt` | Strong | Covered | — |
| P-02 | FindById | id missing -> null | `FindById_MissingItem_ReturnsNull` | Strong | Covered | — |

### Program.cs — NO TEST SUITE
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---------|-----------|--------------|--------------------|----------------|-------|
| P-01 | GET /todos/{id}: item missing -> 404 | — | — | Uncovered | Unmapped unit |

**Tallies**: Covered 13 / Partially Covered 3 / Uncovered 8 / Mock bypass risks 1
"""

PY_NAMES = [("TodoServiceTests", "TodoServiceTests"), ("TodoService.cs", "todo_service.py"),
            ("InMemoryTodoRepositoryTests.cs", "tests/test_todo_repository.py"),
            ("InMemoryTodoRepository.cs", "todo_repository.py"), ("Program.cs", "main.py"),
            ("CreateTodo", "create_todo"), ("CompleteTodo", "complete_todo"), ("ListTodos", "list_todos"),
            ("DeleteTodo", "delete_todo"), ("RenameTodo", "rename_todo"), ("PriorityLabel", "priority_label"),
            ("FindById", "find_by_id"), ("includeCompleted", "include_completed"), ("minPriority", "min_priority"),
            ("null", "None")]


def to_python(text: str) -> str:
    for a, b in PY_NAMES:
        text = text.replace(a, b)
    return text


def flatten(text: str) -> str:
    """Same audit, one table per class: the method moves from the heading into the Path ID cell."""
    out, method = [], None
    for line in text.splitlines():
        m = re.match(r"^#### `(\w+)\(", line)
        if m:
            method = m.group(1)
            continue
        if method and re.match(r"^\| P-\d\d \|", line):
            line = line.replace("| P-", f"| {method} P-", 1)
        if line.startswith("### "):
            method = None
        out.append(line)
    return "\n".join(out)


def score(text: str, lang: str = "dotNET", **kw) -> harness.Score:
    return harness.score_run(harness.parse_tables(text), harness.load_app_key(lang), 90, **kw)


class ParsingTests(unittest.TestCase):
    def test_split_cells_keeps_pipes_inside_code_spans(self):
        cells = harness.split_cells("| P-03 | `priority < 1 || priority > 5` | a \\| b | Covered |")
        self.assertEqual(["P-03", "`priority < 1 || priority > 5`", "a | b", "Covered"], cells)

    def test_classification_column_wins_over_notes(self):
        rows = harness.parse_tables("| Path | Classification | Notes |\n|---|---|---|\n| P-01 | Uncovered | covered elsewhere? |")
        self.assertEqual("uncovered", rows[0].classification)

    def test_classify(self):
        self.assertEqual("partial", harness.classify("**Partially Covered**"))
        self.assertEqual("uncovered", harness.classify("❌ Uncovered"))
        self.assertEqual("covered", harness.classify("✅ Covered"))
        self.assertIsNone(harness.classify("—"))

    def test_headings_are_scoped_by_level(self):
        rows = harness.parse_tables("### A.cs\n#### `M1()`\n| x | y |\n|---|---|\n| 1 | 2 |\n### B.cs\n| x | y |\n|---|---|\n| 3 | 4 |")
        self.assertEqual(["A.cs", "`M1()`"], rows[0].headings)
        self.assertEqual(["B.cs"], rows[1].headings)

    def test_report_metrics(self):
        m = harness.report_metrics("| Total logical paths ($N_{\\text{total}}$) | 24 |\n| Total problems ($N$) | 11 |\n"
                                   "| **Problem percentage** | **45.8%** |\n| Critical / High / Medium / Low | 1 / 5 / 3 / 2 |")
        self.assertEqual({"totalPaths": "24", "totalProblems": "11", "problemPct": "45.8", "severity": "1 / 5 / 3 / 2"}, m)


class ScoringTests(unittest.TestCase):
    def assert_perfect(self, s: harness.Score):
        self.assertEqual([], [(g["id"], g["status"]) for g in s.missed])
        self.assertEqual([], [(c["id"], c["status"]) for c in s.controls if c["status"] != "confirmed"])
        self.assertTrue(s.passed)

    def test_perfect_audit_scores_every_gap_and_control(self):
        s = score(PERFECT_AUDIT_DOTNET)
        self.assert_perfect(s)
        # P-03 of RenameTodo (Partially Covered, not a seeded gap) is the only unscored problem.
        self.assertEqual(1, len(s.unscored_problems), s.unscored_problems)

    def test_python_names_and_java_names(self):
        self.assert_perfect(score(to_python(PERFECT_AUDIT_DOTNET), "python"))
        java = PERFECT_AUDIT_DOTNET.replace("Program.cs", "TodoController.java").replace(".cs", ".java")
        self.assert_perfect(score(java, "java"))

    def test_method_in_row_instead_of_heading(self):
        self.assert_perfect(score(flatten(PERFECT_AUDIT_DOTNET)))
        self.assert_perfect(score(flatten(to_python(PERFECT_AUDIT_DOTNET)), "python"))

    def test_control_classified_uncovered_is_a_false_positive(self):
        text = PERFECT_AUDIT_DOTNET.replace(
            "| `DeleteTodo_MissingItem_ThrowsNotFoundException` | Strong | Covered |", "| — | — | Uncovered |")
        s = score(text)
        self.assertEqual(["C5"], [c["id"] for c in s.false_positives])
        self.assertFalse(s.passed)

    def test_gap_classified_covered_is_missed(self):
        text = PERFECT_AUDIT_DOTNET.replace('| P-02 | priority 3 -> "medium" | — | — | Uncovered |',
                                            '| P-02 | priority 3 -> "medium" | `X` | Strong | Covered |')
        s = score(text)
        g7 = next(g for g in s.gaps if g["id"] == "G7")
        self.assertEqual("misclassified", g7["status"])
        self.assertEqual(9, len(s.found))
        self.assertTrue(s.passed)  # 9/10 = 90%

    def test_two_misses_fail_at_90_percent(self):
        text = PERFECT_AUDIT_DOTNET.replace("| P-02 | trimmed title length > 100 | — | — | Uncovered | No test with a long title |\n", "")
        text = text.replace('| P-02 | priority 3 -> "medium" | — | — | Uncovered | — |\n', "")
        s = score(text)
        self.assertEqual({"G1", "G7"}, {g["id"] for g in s.missed})
        self.assertFalse(s.passed)

    def test_api_gap_found_from_the_mapping_table(self):
        audit = PERFECT_AUDIT_DOTNET.split("### Program.cs")[0]
        mapping = ("| # | Source Unit | Test Unit(s) | Mapping Basis | Notes |\n|---|---|---|---|---|\n"
                   "| 1 | TodoApi/TodoService.cs | TodoApi.Tests/TodoServiceTests.cs | name-stem | — |\n"
                   "| 2 | TodoApi/Program.cs | — | — | No test suite found |\n")
        self.assertEqual("not located", next(g for g in score(audit).gaps if g["id"] == "G10")["status"])
        s = score(audit, mapping_rows=harness.parse_tables(mapping))
        self.assertEqual("found", next(g for g in s.gaps if g["id"] == "G10")["status"])

    def test_report_is_used_when_the_audit_lacks_a_row(self):
        audit = PERFECT_AUDIT_DOTNET.replace('| P-04 | any other value -> "unknown" (default arm) | — | — | Uncovered | — |', "")
        report = ("### TodoService.cs\n| Path | Method | Condition | Classification |\n|---|---|---|---|\n"
                  "| P-04 | PriorityLabel | default arm -> \"unknown\" | Uncovered |\n")
        self.assertEqual("not located", next(g for g in score(audit).gaps if g["id"] == "G8")["status"])
        s = score(audit, report_rows=harness.parse_tables(report))
        self.assertEqual("found", next(g for g in s.gaps if g["id"] == "G8")["status"])


    def test_layout_of_a_real_run(self):
        """Row shapes from a real Claude run (Python app, 2026-11-14) that once fooled the scorer."""
        audit = """
## `errors.py` vs `tests/test_todo_service.py`
### Method: `NotFoundError.__init__`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---|---|---|---|---|---|
| P-01 | Constructor called with any `todo_id` | `test_delete_todo_missing_item_raises_not_found_error` | Partial | Partially Covered | — |

## `todo_repository.py` vs `tests/test_todo_repository.py`
### Method: `InMemoryTodoRepository.__init__`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---|---|---|---|---|---|
| P-01 | Constructor called | — | — | Partially Covered | implied by `find_by_id` returning None in other tests |
### Method: `InMemoryTodoRepository.find_by_id`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---|---|---|---|---|---|
| P-02 | id not present | `test_find_by_id_missing_item_returns_none` | Strong | Covered | — |

## `todo_service.py` vs `tests/test_todo_service.py`
### Method: `TodoService.rename_todo`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---|---|---|---|---|---|
| P-01 | `new_title is None` | — | — | Uncovered | only `" "` is tested |
| P-03 | Title valid, `repository.find_by_id` returns `None` | — | — | Uncovered | No test combines a non-blank title with a missing id. |
### Function: `priority_label`
| Path ID | Condition | Test Case(s) | Assertion Strength | Classification | Notes |
|---|---|---|---|---|---|
| P-02 | `priority` is `3` | — | — | Uncovered | The loop `((1,"low"),(2,"low"),(4,"high"),(5,"high"))` skips `3` |
| P-03 | `priority` is `4` or `5` | `test_priority_label_returns_label` | Strong | Covered | — |
"""
        s = score(audit, "python")
        by_id = {e["id"]: e for e in s.gaps + s.controls}
        self.assertEqual("found", by_id["G7"]["status"])            # notes mention "low"/"high"
        self.assertEqual("found", by_id["G9"]["status"])
        self.assertIn("Title valid", by_id["G9"]["rows"][0]["row"])  # not the new_title-is-None row
        self.assertEqual("confirmed", by_id["C6"]["status"])         # "4 or 5" without the word "high"
        self.assertEqual("not located", by_id["C5"]["status"])       # errors.py row is not the service
        self.assertEqual("confirmed", by_id["C7"]["status"])         # constructor row is not find_by_id
        self.assertEqual(1, len(by_id["C7"]["rows"]))


class AnswerKeyTests(unittest.TestCase):
    def test_counts(self):
        for lang in harness.LANGS:
            key = harness.load_app_key(lang)
            self.assertEqual(10, len(key.gaps), lang)
            self.assertEqual(7, len(key.controls), lang)
            self.assertEqual(len({e.id for e in key.gaps + key.controls}), 17)

    def test_files_exist_and_units_and_methods_match_them(self):
        for lang in harness.LANGS:
            key = harness.load_app_key(lang)
            for unit, rel in {**key.source, **key.tests}.items():
                self.assertTrue((key.app_dir / rel).is_file(), f"{lang}: {rel}")
            for unit, rel in key.source.items():
                self.assertTrue(key.units[unit].pattern.search(harness.norm(rel)), f"{lang}: {unit} vs {rel}")
                text = harness.norm((key.app_dir / rel).read_text(encoding="utf-8"))
                for m in key.units[unit].methods:
                    self.assertIn(m, text, f"{lang}: method {m} not in {rel}")
            for e in key.gaps + key.controls:
                self.assertIn(e.unit, key.units, f"{lang} {e.id}")
                if e.method:
                    self.assertIn(e.method, key.units[e.unit].methods, f"{lang} {e.id}")

    def test_seeded_gaps_are_really_untested(self):
        """Cheap static checks that the tests never reach what G5, G7 and G8 say is untested."""
        for lang in harness.LANGS:
            key = harness.load_app_key(lang)
            tests = harness.norm((key.app_dir / key.tests["service"]).read_text(encoding="utf-8"))
            self.assertNotIn('"medium"', tests, lang)
            self.assertNotIn('"unknown"', tests, lang)
            self.assertNotIn("minpriority", tests, lang)
            self.assertNotIn(", 6", tests, lang)  # no priority-6 case


class InvocationTests(unittest.TestCase):
    def test_detect_tool(self):
        self.assertEqual("copilot", harness.detect_tool("copilot", {})[0])
        self.assertEqual("claude", harness.detect_tool("auto", {"COVERAGE_TEST_TOOL": "claude"})[0])
        self.assertEqual("claude", harness.detect_tool("auto", {"CLAUDECODE": "1", "TERM_PROGRAM": "vscode"})[0])
        self.assertEqual("copilot", harness.detect_tool("auto", {"TERM_PROGRAM": "vscode"})[0])
        self.assertEqual("claude", harness.detect_tool("auto", {})[0])
        with self.assertRaises(ValueError):
            harness.detect_tool("auto", {"COVERAGE_TEST_TOOL": "other"})

    def test_run_ids_are_unique_and_skip_existing_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = harness.new_run_id(Path(tmp))
            (Path(tmp) / f"run-{first}.md").write_text("x")
            ids = [first] + [harness.new_run_id(Path(tmp)) for _ in range(3)]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(re.fullmatch(r"\d{8}-\d{6}", i) for i in ids))

    def test_commands(self):
        key = harness.load_app_key("java")
        claude = harness.build_command("claude", key, "20261114-120000", None, [])
        self.assertIn("--allowedTools", claude)
        self.assertIn("test/apis/java", claude[2])
        self.assertIn("20261114-120000", claude[2])
        copilot = harness.build_command("copilot", key, "20261114-120000", "gpt-x", [])
        self.assertEqual(harness.AGENT_NAME, copilot[copilot.index("--agent") + 1])
        self.assertEqual("gpt-x", copilot[copilot.index("--model") + 1])

    def test_manifest_target_check(self):
        key = harness.load_app_key("python")
        self.assertTrue(harness.manifest_targets_app("- **Target root**: test\\apis\\python", key))
        self.assertFalse(harness.manifest_targets_app("- **Target root**: test/apis/java", key))

    def test_score_only_resolves_artifact_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            t, d = Path(tmp) / "transitions", Path(tmp) / "docs"
            t.mkdir()
            d.mkdir()
            (t / "03-assertion-audit-20261114-120000.md").write_text("x")
            (d / "coverage-review-20261114-120000.md").write_text("x")
            files = harness.resolve_score_only(str(t / "03-assertion-audit-20261114-120000.md"))
            self.assertEqual("20261114-120000", files.run_id)
            self.assertIsNotNone(files.audit)
            self.assertIsNotNone(files.report)


if __name__ == "__main__":
    unittest.main()
