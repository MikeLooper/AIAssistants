"""SEC-OP-05: no hardcoded secrets (API keys, connection strings, credentials)
committed to the repo. A small, dependency-free regex scan -- not a
replacement for gitleaks/trufflehog, but catches the common obvious cases.
"""
from __future__ import annotations

import re
from pathlib import Path

from ..schemas import Evidence
from .base import AnalyzerCheck

IGNORED_DIR_NAMES = {".git", "bin", "obj", "node_modules", ".venv", "venv", "__pycache__"}
SCAN_EXTENSIONS = {".json", ".yml", ".yaml", ".env", ".config", ".xml", ".properties", ".cs", ".py", ".js", ".ts"}

# (label, pattern). Deliberately excludes obvious placeholders like <password>, ${...}, {{...}}.
SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("generic API key assignment", re.compile(r'(?i)\b(api[_-]?key|apikey)\b\s*[:=]\s*["\']([A-Za-z0-9\-_]{16,})["\']')),
    ("password assignment with a real-looking value", re.compile(
        r'(?i)"password"\s*:\s*"(?!<|\$\{|\{\{)([^"\s]{6,})"'
    )),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]


def run(target_path: Path) -> list[AnalyzerCheck]:
    hits: list[Evidence] = []
    for path in target_path.rglob("*"):
        if not path.is_file() or path.suffix not in SCAN_EXTENSIONS:
            continue
        if any(part in IGNORED_DIR_NAMES for part in path.relative_to(target_path).parts[:-1]):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    hits.append(Evidence(
                        file=path.relative_to(target_path).as_posix(),
                        lineStart=line_no, lineEnd=line_no,
                        excerpt=f"{label}: {line.strip()[:120]}",
                    ))

    passed = not hits
    reason = "no likely hardcoded secret patterns found" if passed else f"{len(hits)} likely secret pattern match(es) found"
    return [
        AnalyzerCheck(
            "SEC-OP-05", "Security", "Operational", "Error", passed, reason,
            title="Possible hardcoded secret committed to the repository",
            evidence=hits[:10],
            recommendation="Move the value to a secret manager/environment variable and rotate it if it is a real credential.",
            standard="OWASP Secrets Management Cheat Sheet",
            url="https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
            confidence="Medium",
            effort="Small",
        )
    ]
