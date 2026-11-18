"""Builds the command lines for the reviewer script and the validation test scripts, and validates the
values a caller passes into them. Commands are argument lists (never a shell string), and every free-text
value is checked so it can't be read as another option."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .config import TOOLS, Settings

_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/\[\]-]{0,127}$")
_SUBJECT_RE = re.compile(r"^review-[a-z0-9-]+$")
_ANALYZER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")

PROGRESS_SECONDS = 15


@dataclass(frozen=True)
class TesterDefinition:
    __test__ = False  # not a pytest test class
    name: str      # URL name, e.g. "api-dotnet"
    kind: str      # harness kind: apis | uis | mcps
    lang: str      # harness language: dotNET | java | python
    script: str    # file name under test/logic
    title: str

    @property
    def app(self) -> str:
        """The harness's own name for the app, used in its result file names (e.g. apis-dotNET)."""
        return f"{self.kind}-{self.lang}"


_KIND_TITLES = {"apis": "API", "uis": "UI", "mcps": "MCP server"}
_LANG_TITLES = {"dotNET": "C#", "java": "Java", "python": "Python"}

TESTER_DEFINITIONS: tuple[TesterDefinition, ...] = tuple(
    TesterDefinition(f"{kind[:-1]}-{lang.lower()}", kind, lang, f"test_{kind[:-1]}_{lang.lower()}.py",
                   f"{_LANG_TITLES[lang]} {_KIND_TITLES[kind]}")
    for kind in ("apis", "uis", "mcps") for lang in ("dotNET", "java", "python")
)
TESTERS_BY_NAME = {t.name: t for t in TESTER_DEFINITIONS}


# ---------------------------------------------------------------------- validation


def validate_model(model: str | None) -> str | None:
    model = (model or "").strip()
    if not model:
        return None
    if not _MODEL_RE.match(model):
        raise ValueError(f"invalid model name {model!r}: use letters, digits and . _ : / [ ] - "
                         "(not starting with '-'), at most 128 characters")
    return model


def validate_tool(tool: str | None, default: str) -> str:
    tool = (tool or default or "auto").strip().lower()
    if tool not in TOOLS:
        raise ValueError(f"tool must be one of {', '.join(TOOLS)}, got {tool!r}")
    return tool


def validate_subjects(subjects: str | None, known: list[str]) -> str:
    """'all', or a comma-separated list of review-* skill names that exist."""
    text = (subjects or "all").strip()
    if text.lower() == "all":
        return "all"
    names = [s.strip() for s in text.split(",") if s.strip()]
    if not names:
        return "all"
    bad = [n for n in names if not _SUBJECT_RE.match(n)]
    if bad:
        raise ValueError(f"invalid subject name(s): {', '.join(bad)}")
    if known:
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"unknown subject(s): {', '.join(unknown)}")
    return ",".join(dict.fromkeys(names))


def validate_analyzers(analyzers: str | None) -> str:
    text = (analyzers or "auto").strip()
    names = [a.strip() for a in text.split(",") if a.strip()] or ["auto"]
    bad = [n for n in names if not _ANALYZER_RE.match(n)]
    if bad:
        raise ValueError(f"invalid analyzer name(s): {', '.join(bad)}")
    return ",".join(names)


def validate_timeout(minutes: float | None, default: float, limit: float) -> float:
    value = default if minutes is None else float(minutes)
    if not 0 < value <= limit:
        raise ValueError(f"timeout must be greater than 0 and at most {limit:g} minutes")
    return value


def list_subjects(settings: Settings) -> list[str]:
    if not settings.skills_dir.is_dir():
        return []
    return sorted(p.name for p in settings.skills_dir.iterdir() if p.is_dir() and _SUBJECT_RE.match(p.name))


def available_testers(settings: Settings) -> list[TesterDefinition]:
    return [t for t in TESTER_DEFINITIONS if (settings.tests_dir / t.script).is_file()]


def reviewer_version(settings: Settings) -> str | None:
    try:
        return settings.version_file.read_text(encoding="utf-8-sig").strip() or None
    except OSError:
        return None


# ---------------------------------------------------------------------- commands


@dataclass
class ReviewOptions:
    tool: str
    model: str | None
    subjects: str
    advanced: bool
    analyzers: str
    timeout_min: float


@dataclass
class TesterOptions:
    __test__ = False
    tool: str
    model: str | None
    min_found: float
    no_build: bool
    timeout_min: float


def review_command(settings: Settings, target: Path, out_file: Path, summary_file: Path,
                   opts: ReviewOptions) -> list[str]:
    cmd = [sys.executable, "-u", str(settings.reviewer_script), str(target),
           "--tool", opts.tool, "--subjects", opts.subjects,
           "--out-file", str(out_file), "--summary-json", str(summary_file), "--no-report",
           "--timeout", f"{opts.timeout_min:g}", "--progress", str(PROGRESS_SECONDS)]
    if opts.model:
        cmd += ["--model", opts.model]
    if opts.advanced:
        cmd += ["--advanced", "--analyzers", opts.analyzers]
    return cmd


def tester_command(settings: Settings, test: TesterDefinition, results_dir: Path, opts: TesterOptions) -> list[str]:
    cmd = [sys.executable, "-u", str(settings.tests_dir / test.script),
           "--tool", opts.tool, "--min-found", f"{opts.min_found:g}",
           "--timeout", f"{opts.timeout_min:g}", "--results-dir", str(results_dir),
           "--progress", str(PROGRESS_SECONDS)]
    if opts.model:
        cmd += ["--model", opts.model]
    if opts.no_build:
        cmd.append("--no-build")
    return cmd
