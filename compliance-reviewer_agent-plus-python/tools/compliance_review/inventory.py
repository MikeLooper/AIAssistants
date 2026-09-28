"""Repo mapping per .github/skills/compliance-inventory/SKILL.md.

This is a deterministic, glob/keyword-based approximation of the same
mechanical steps that skill's procedure describes (it detects signals and
markers, not semantic meaning -- the actual judgment still happens in
Phase 3 / the LLM worker). Produces the same shape as `01-inventory.json`.
"""
from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path

MAX_FILES_PER_SUBJECT_BATCH = 40
MAX_SAMPLED_SOURCE_FILES = 300

# .github/skills/compliance-review-core/references/languages.md
LANGUAGE_SIGNALS: dict[str, list[str]] = {
    "csharp": ["*.csproj", "*.sln"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "python": ["pyproject.toml", "requirements.txt", "setup.py"],
}

SOURCE_EXTENSIONS = {
    ".cs", ".java", ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rb", ".php", ".kt",
}

IAC_PATTERNS = ["*.bicep", "*.tf", "*/k8s/*.yaml", "*/k8s/*.yml", "*/helm/*.yaml", "*/helm/*.yml"]
IGNORED_DIR_NAMES = {".git", "bin", "obj", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}


def _walk_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIR_NAMES for part in path.relative_to(root).parts[:-1]):
            continue
        files.append(path)
    return files


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _match_any(rel_path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(f"/{rel_path}", f"*/{p}") for p in patterns)


def detect_languages(all_rel_files: list[str]) -> list[str]:
    found = []
    for lang, patterns in LANGUAGE_SIGNALS.items():
        if any(_match_any(f, patterns) for f in all_rel_files):
            found.append(lang)
    return found


def detect_frameworks(all_rel_files: list[str], read_text) -> list[str]:
    frameworks: set[str] = set()
    for f in all_rel_files:
        name = Path(f).name
        if name in ("Program.cs", "Startup.cs"):
            frameworks.add("ASP.NET Core")
        elif name == "manage.py":
            frameworks.add("Django")
        elif name.endswith(".csproj"):
            frameworks.add(".NET")
    for f in all_rel_files:
        if Path(f).suffix != ".py":
            continue
        text = read_text(f)
        if text is None:
            continue
        if "FastAPI" in text:
            frameworks.add("FastAPI")
        if "Flask(" in text:
            frameworks.add("Flask")
    for f in all_rel_files:
        if Path(f).suffix == ".java" and (text := read_text(f)) and "@SpringBootApplication" in text:
            frameworks.add("Spring Boot")
    return sorted(frameworks)


def find_api_specs(all_rel_files: list[str]) -> bool:
    spec_patterns = ["*openapi*.json", "*openapi*.yaml", "*openapi*.yml", "*swagger*.json", "*swagger*.yaml"]
    if any(_match_any(f, spec_patterns) for f in all_rel_files):
        return True
    controller_markers = ["Controllers/", "/controllers/", "/routers/"]
    return any(marker in f for f in all_rel_files for marker in controller_markers)


def find_iac(all_rel_files: list[str]) -> bool:
    return any(_match_any(f, IAC_PATTERNS) for f in all_rel_files)


# Approximates .github/skills/compliance-inventory/references/subject-file-map.md.
# Each entry: (glob patterns, optional content keywords to further filter matches).
SUBJECT_GLOBS: dict[str, list[str]] = {
    "review-software-lifecycle": [
        ".github/workflows/*", "azure-pipelines.yml", "Jenkinsfile", "CHANGELOG*", "SECURITY.md",
    ],
    "review-twelve-factor": [
        "**/appsettings*.json", "**/application*.properties", "**/application*.yml",
        "Dockerfile", "docker-compose*.yml", ".env.example", "**/*.csproj", "pom.xml",
        "requirements.txt", "pyproject.toml",
    ],
    "review-api-design": ["*openapi*.json", "*openapi*.yaml", "*swagger*.json", "**/Controllers/*", "**/routers/*"],
    "review-testing": ["**/test/**", "**/tests/**", "**/*Test.java", "**/test_*.py", "**/*.Tests/**"],
    "review-dependency-management": [
        "Directory.Packages.props", "**/*.csproj", "pom.xml", "build.gradle*", "requirements.txt",
        "package.json", "packages.lock.json", "poetry.lock", "**/*.lock",
    ],
    "review-maintainability": ["README*", "CONTRIBUTING*", "docs/**"],
}

# Subjects whose scope is "all source files, sampled".
ALL_SOURCE_SUBJECTS = ["review-software-quality", "review-coding-standards"]

# Content-keyword-filtered subjects: glob to a broad candidate set, then keep files
# whose text matches at least one keyword (case-insensitive).
KEYWORD_SUBJECTS: dict[str, list[str]] = {
    "review-security-identity-access": ["authoriz", "authentic", "jwt", "oauth", "session", "[allowanonymous]"],
    "review-security-input-injection": ["controller", "request", "sql", "query", "upload", "xml"],
    "review-security-web-api": ["cors", "httpsredirect", "hsts", "securityheader", "controller"],
    "review-security-operational": ["catch (exception", "except ", "logger", "log.", "secret", "password"],
    "review-observability": ["opentelemetry", "activitysource", "ilogger", "logging", "healthcheck", "metrics"],
    "review-reliability": ["retry", "circuitbreaker", "polly", "timeout", "healthcheck"],
    "review-performance": ["cache", "async ", "await ", "connectionpool", "memorycache"],
}

# IaC-gated subjects: N/A entirely (no subagent/analysis) when iacFound is False.
IAC_GATED_SUBJECTS = ["review-disaster-recovery", "review-monitoring", "review-cost-sustainability"]

ALL_SUBJECTS = [
    "review-software-quality", "review-software-lifecycle", "review-twelve-factor", "review-api-design",
    "review-security-identity-access", "review-security-input-injection", "review-security-web-api",
    "review-security-operational", "review-coding-standards", "review-testing", "review-observability",
    "review-dependency-management", "review-reliability", "review-performance",
    "review-disaster-recovery", "review-monitoring", "review-cost-sustainability", "review-maintainability",
]


def _batch(files: list[str]) -> list[list[str]]:
    if not files:
        return []
    return [files[i:i + MAX_FILES_PER_SUBJECT_BATCH] for i in range(0, len(files), MAX_FILES_PER_SUBJECT_BATCH)]


@dataclass
class SubjectFiles:
    files: list[str] = field(default_factory=list)
    batches: list[list[str]] = field(default_factory=list)
    applicable: bool = True


@dataclass
class InventoryResult:
    languages: list[str]
    frameworks: list[str]
    apiSpecsFound: bool
    iacFound: bool
    subjects: dict[str, SubjectFiles]
    skippedSubjects: dict[str, str]

    def to_dict(self) -> dict:
        return {
            "languages": self.languages,
            "frameworks": self.frameworks,
            "apiSpecsFound": self.apiSpecsFound,
            "iacFound": self.iacFound,
            "subjects": {
                k: {"files": v.files, "batches": v.batches, "applicable": v.applicable}
                for k, v in self.subjects.items()
            },
            "skippedSubjects": self.skippedSubjects,
        }


def build_inventory(target_path: str) -> InventoryResult:
    root = Path(target_path)
    all_files = _walk_files(root)
    all_rel_files = [_rel(root, p) for p in all_files]

    def read_text(rel_path: str) -> str | None:
        try:
            return (root / rel_path).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None

    languages = detect_languages(all_rel_files)
    frameworks = detect_frameworks(all_rel_files, read_text)
    api_specs_found = find_api_specs(all_rel_files)
    iac_found = find_iac(all_rel_files)

    subjects: dict[str, SubjectFiles] = {}
    skipped: dict[str, str] = {}

    source_files = sorted(f for f in all_rel_files if Path(f).suffix in SOURCE_EXTENSIONS)
    for subject in ALL_SOURCE_SUBJECTS:
        files = source_files[:MAX_SAMPLED_SOURCE_FILES]
        subjects[subject] = SubjectFiles(files=files, batches=_batch(files), applicable=True)

    for subject, patterns in SUBJECT_GLOBS.items():
        files = sorted({f for f in all_rel_files if _match_any(f, patterns)})
        applicable = True
        if subject == "review-api-design" and not api_specs_found:
            applicable = False
            skipped[subject] = "no OpenAPI/Swagger spec or controller/router files found"
        subjects[subject] = SubjectFiles(files=files, batches=_batch(files), applicable=applicable)

    for subject, keywords in KEYWORD_SUBJECTS.items():
        candidates = source_files
        matched = []
        for f in candidates:
            text = read_text(f)
            if text is None:
                continue
            lower = text.lower()
            if any(k in lower for k in keywords):
                matched.append(f)
        subjects[subject] = SubjectFiles(files=matched, batches=_batch(matched), applicable=True)

    for subject in IAC_GATED_SUBJECTS:
        applicable = iac_found
        files = [f for f in all_rel_files if _match_any(f, IAC_PATTERNS)] if iac_found else []
        subjects[subject] = SubjectFiles(files=files, batches=_batch(files), applicable=applicable)
        if not applicable:
            skipped[subject] = "no infrastructure-as-code found"

    for subject in ALL_SUBJECTS:
        subjects.setdefault(subject, SubjectFiles(files=[], batches=[], applicable=False))

    return InventoryResult(
        languages=languages,
        frameworks=frameworks,
        apiSpecsFound=api_specs_found,
        iacFound=iac_found,
        subjects=subjects,
        skippedSubjects=skipped,
    )
