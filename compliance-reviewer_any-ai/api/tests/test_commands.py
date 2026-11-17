import sys
from pathlib import Path

import pytest

from comp_review_api import commands
from comp_review_api.commands import ReviewOptions, TesterOptions


@pytest.mark.parametrize("model", ["claude-opus-5-5", "claude-sonnet-4.5", "gpt-5", "claude-opus-4-8[1m]",
                                   "us.anthropic.claude-haiku-4-5", "org/model:tag"])
def test_valid_models(model):
    assert commands.validate_model(f"  {model} ") == model


@pytest.mark.parametrize("model", ["--dangerously-skip-permissions", "-m", "a b", "a;b", "x" * 200, "$(x)"])
def test_invalid_models(model):
    with pytest.raises(ValueError, match="invalid model"):
        commands.validate_model(model)


def test_blank_model_means_none():
    assert commands.validate_model(None) is None
    assert commands.validate_model("   ") is None


def test_validate_tool():
    assert commands.validate_tool(None, "claude") == "claude"
    assert commands.validate_tool("Copilot", "auto") == "copilot"
    with pytest.raises(ValueError):
        commands.validate_tool("gemini", "auto")


def test_validate_subjects():
    known = ["review-testing", "review-maintainability"]
    assert commands.validate_subjects(None, known) == "all"
    assert commands.validate_subjects(" ALL ", known) == "all"
    assert commands.validate_subjects(" , ", known) == "all"
    assert commands.validate_subjects("review-testing, review-maintainability,review-testing", known) == \
        "review-testing,review-maintainability"
    with pytest.raises(ValueError, match="unknown subject"):
        commands.validate_subjects("review-nope", known)
    with pytest.raises(ValueError, match="invalid subject"):
        commands.validate_subjects("--advanced", known)
    assert commands.validate_subjects("review-anything", []) == "review-anything"  # nothing to check against


def test_validate_analyzers():
    assert commands.validate_analyzers(None) == "auto"
    assert commands.validate_analyzers("pip-audit, dotnet-list") == "pip-audit,dotnet-list"
    with pytest.raises(ValueError):
        commands.validate_analyzers("-x")


def test_validate_timeout():
    assert commands.validate_timeout(None, 60, 1440) == 60
    assert commands.validate_timeout(5, 60, 1440) == 5
    for bad in (0, -1, 2000):
        with pytest.raises(ValueError):
            commands.validate_timeout(bad, 60, 1440)


def test_tester_definitions_cover_the_nine_scripts():
    names = [t.name for t in commands.TESTER_DEFINITIONS]
    assert len(names) == 9
    assert names[:3] == ["api-dotnet", "api-java", "api-python"]
    t = commands.TESTERS_BY_NAME["mcp-dotnet"]
    assert (t.kind, t.lang, t.script, t.app, t.title) == ("mcps", "dotNET", "test_mcp_dotnet.py", "mcps-dotNET",
                                                           "C# MCP server")
    assert commands.TESTERS_BY_NAME["ui-python"].script == "test_ui_python.py"


def test_real_tester_scripts_exist():
    """Every catalogued tester matches a real script in the reviewer workspace."""
    from comp_review_api.config import Settings

    s = Settings().validate()
    assert [t.name for t in commands.available_testers(s)] == [t.name for t in commands.TESTER_DEFINITIONS]
    assert s.reviewer_script.is_file()


def test_workspace_helpers(settings, fake_root):
    assert commands.list_subjects(settings) == ["review-maintainability", "review-testing"]
    assert commands.reviewer_version(settings) == "1.0.0"
    (fake_root / "test" / "logic" / "test_ui_java.py").unlink()
    assert "ui-java" not in [t.name for t in commands.available_testers(settings)]
    (fake_root / "VERSION").unlink()
    assert commands.reviewer_version(settings) is None


def test_review_command(settings):
    opts = ReviewOptions(tool="claude", model="claude-sonnet-5-5", subjects="all", advanced=True,
                         analyzers="pip-audit", timeout_min=30)
    cmd = commands.review_command(settings, Path("/t/app"), Path("/w/r.md"), Path("/w/s.json"), opts)
    assert cmd[:3] == [sys.executable, "-u", str(settings.reviewer_script)]
    assert cmd[3] == str(Path("/t/app"))
    joined = " ".join(cmd)
    for part in ("--tool claude", "--subjects all", "--no-report", "--timeout 30", "--model claude-sonnet-5-5",
                 "--advanced --analyzers pip-audit", f"--summary-json {Path('/w/s.json')}"):
        assert part in joined


def test_review_command_without_optional_flags(settings):
    opts = ReviewOptions(tool="auto", model=None, subjects="review-testing", advanced=False, analyzers="auto",
                         timeout_min=60)
    cmd = commands.review_command(settings, Path("/t"), Path("/r.md"), Path("/s.json"), opts)
    assert "--model" not in cmd and "--advanced" not in cmd and "--analyzers" not in cmd


def test_tester_command(settings):
    t = commands.TESTERS_BY_NAME["api-java"]
    opts = TesterOptions(tool="copilot", model="gpt-5", min_found=75, no_build=True, timeout_min=45)
    cmd = commands.tester_command(settings, t, Path("/w/results"), opts)
    assert cmd[2] == str(settings.tests_dir / "test_api_java.py")
    joined = " ".join(cmd)
    for part in ("--tool copilot", "--min-found 75", "--timeout 45", "--model gpt-5", "--no-build",
                 f"--results-dir {Path('/w/results')}"):
        assert part in joined
    opts.no_build, opts.model = False, None
    cmd = commands.tester_command(settings, t, Path("/w/results"), opts)
    assert "--no-build" not in cmd and "--model" not in cmd
