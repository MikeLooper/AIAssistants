import tempfile
import unittest
from pathlib import Path

from tools.compliance_review.inventory import build_inventory


class InventoryTests(unittest.TestCase):
    def test_detects_csharp_and_no_iac_from_dockerfile_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.csproj").write_text("<Project />")
            (root / "Dockerfile").write_text("FROM mcr.microsoft.com/dotnet/aspnet:10.0")
            (root / "appsettings.json").write_text("{}")

            inv = build_inventory(str(root))

            self.assertIn("csharp", inv.languages)
            self.assertFalse(inv.iacFound, "a bare Dockerfile must not count as infrastructure-as-code")

    def test_iac_found_with_bicep_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.bicep").write_text("resource foo 'Microsoft.Web/sites@2022-03-01' = {}")
            inv = build_inventory(str(root))
            self.assertTrue(inv.iacFound)

    def test_api_design_not_applicable_without_spec_or_controllers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "requirements.txt").write_text("flask==3.0.0")
            inv = build_inventory(str(root))
            self.assertFalse(inv.subjects["review-api-design"].applicable)
            self.assertIn("review-api-design", inv.skippedSubjects)

    def test_batching_splits_large_subject_file_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i in range(85):
                (root / f"File{i}.cs").write_text("class C {}")
            inv = build_inventory(str(root))
            batches = inv.subjects["review-coding-standards"].batches
            self.assertGreaterEqual(len(batches), 3)
            self.assertTrue(all(len(b) <= 40 for b in batches))


if __name__ == "__main__":
    unittest.main()
