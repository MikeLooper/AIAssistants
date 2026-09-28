import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from tools.compliance_review.state import (
    RunPaths,
    StateFile,
    make_run_id,
    resume_from_step,
)


class RunIdTests(unittest.TestCase):
    def test_format(self):
        run_id = make_run_id("C:/repos/My-App!!", now=datetime(2026, 9, 26, 22, 25))
        self.assertRegex(run_id, r"^2026-09-26_2225-myapp$")

    def test_falls_back_when_name_has_no_alnum_chars(self):
        run_id = make_run_id("C:/repos/---", now=datetime(2026, 1, 1, 0, 0))
        self.assertTrue(run_id.endswith("-target"))


class StateFileRoundTripTests(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            state = StateFile(runId="r1", targetPath="/x", subjects=["a", "b"])
            state.steps["00-init"] = "completed"
            state.save(path)

            loaded = StateFile.load(path)
            self.assertEqual(loaded.runId, "r1")
            self.assertEqual(loaded.subjects, ["a", "b"])
            self.assertEqual(loaded.steps["00-init"], "completed")


class ResumeTests(unittest.TestCase):
    def test_resume_from_step_moves_later_files_and_resets_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = RunPaths(root, "r1")
            paths.ensure_dirs()
            ordered = ["00-init", "01-inventory", "02-analyzers", "90-aggregate"]
            for step in ordered:
                paths.step_path(step).write_text("{}")

            state = StateFile(runId="r1", targetPath="/x", subjects=[])
            for step in ordered:
                state.steps[step] = "completed"

            resume_from_step(paths, state, ordered, "02-analyzers")

            self.assertFalse(paths.step_path("02-analyzers").exists())
            self.assertTrue((paths.superseded / "02-analyzers.json").exists())
            self.assertTrue((paths.superseded / "90-aggregate.json").exists())
            self.assertTrue(paths.step_path("00-init").exists(), "steps before the resume point are untouched")
            self.assertEqual(state.steps["00-init"], "completed")
            self.assertEqual(state.steps["02-analyzers"], "not-started")
            self.assertEqual(state.steps["90-aggregate"], "not-started")


if __name__ == "__main__":
    unittest.main()
