"""Settings for comp-review-api.

Values come from three layers; later layers win:

1. the defaults in :class:`Settings`,
2. a JSON file (``api/appsettings.json`` by default, or the path in ``COMP_REVIEW_API_CONFIG``), keyed in
   PascalCase (``Environment``, ``Port``, ``DefaultModel`` ...),
3. environment variables named ``COMP_REVIEW_API_<UPPER_SNAKE_KEY>`` (``COMP_REVIEW_API_ENVIRONMENT``,
   ``COMP_REVIEW_API_PORT`` ...). List values are comma-separated; ``AvailableModels`` is JSON.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any, Mapping

API_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_FILE = API_DIR / "appsettings.json"
DEFAULT_REVIEWER_ROOT = API_DIR.parent  # compliance-reviewer_any-ai
ENV_PREFIX = "COMP_REVIEW_API_"
CONFIG_PATH_ENV = ENV_PREFIX + "CONFIG"

ENVIRONMENTS = ("development", "production")
TOOLS = ("auto", "claude", "copilot")


class SettingsError(ValueError):
    """A configuration value is missing or invalid."""


def _default_models() -> dict[str, list[str]]:
    return {
        "claude": ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-fable-5-2"],
        "copilot": ["claude-sonnet-4.5", "claude-opus-4.5", "gpt-5"],
    }


@dataclass
class Settings:
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 12001
    default_tool: str = "auto"
    default_model: str | None = None
    available_models: dict[str, list[str]] = field(default_factory=_default_models)
    cors_origins: list[str] = field(default_factory=lambda: ["http://localhost:12101", "http://127.0.0.1:12101"])
    max_upload_mb: int = 200
    max_extracted_mb: int = 1000
    max_extracted_files: int = 50000
    max_concurrent_jobs: int = 1
    max_retained_jobs: int = 50
    review_timeout_min: float = 60
    test_timeout_min: float = 60
    keep_sources: bool = False
    work_dir: str | None = None
    reviewer_root: str | None = None

    # ------------------------------------------------------------------ derived values

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def root(self) -> Path:
        return Path(self.reviewer_root).expanduser().resolve() if self.reviewer_root else DEFAULT_REVIEWER_ROOT

    @property
    def reviewer_script(self) -> Path:
        return self.root / "scripts" / "run_review.py"

    @property
    def tests_dir(self) -> Path:
        return self.root / "test" / "logic"

    @property
    def skills_dir(self) -> Path:
        return self.root / "compliance-reviewer" / "skills"

    @property
    def version_file(self) -> Path:
        return self.root / "VERSION"

    @property
    def work_path(self) -> Path:
        base = Path(self.work_dir).expanduser() if self.work_dir else Path(tempfile.gettempdir()) / "comp-review-api"
        return base.resolve()

    def public_dict(self) -> dict[str, Any]:
        """Every setting, PascalCase-keyed like appsettings.json, plus the resolved paths."""
        data = {_pascal(k): v for k, v in asdict(self).items()}
        data["ReviewerRoot"] = str(self.root)
        data["WorkDir"] = str(self.work_path)
        return data

    # ------------------------------------------------------------------ validation

    def validate(self) -> "Settings":
        self.environment = (self.environment or "").strip().lower()
        if self.environment not in ENVIRONMENTS:
            raise SettingsError(f"Environment must be one of {ENVIRONMENTS}, got {self.environment!r}")
        self.default_tool = (self.default_tool or "auto").strip().lower()
        if self.default_tool not in TOOLS:
            raise SettingsError(f"DefaultTool must be one of {TOOLS}, got {self.default_tool!r}")
        if not 1 <= self.port <= 65535:
            raise SettingsError(f"Port must be between 1 and 65535, got {self.port}")
        for name in ("max_upload_mb", "max_extracted_mb", "max_extracted_files", "max_concurrent_jobs",
                     "max_retained_jobs", "review_timeout_min", "test_timeout_min"):
            if getattr(self, name) <= 0:
                raise SettingsError(f"{_pascal(name)} must be greater than 0")
        if self.default_model:
            from .commands import validate_model  # local import: commands imports config

            try:
                self.default_model = validate_model(self.default_model)
            except ValueError as e:
                raise SettingsError(f"DefaultModel: {e}") from None
        if not isinstance(self.available_models, dict):
            raise SettingsError("AvailableModels must be an object of tool name -> list of model names")
        return self


# ---------------------------------------------------------------------- loading


def _pascal(snake: str) -> str:
    return "".join(part.capitalize() for part in snake.split("_"))


def _snake(pascal: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", pascal).lower()


_FIELDS = {f.name: f for f in fields(Settings)}


def _coerce(name: str, value: Any) -> Any:
    """Convert a raw value (from JSON or an environment string) to the field's type."""
    kind = _FIELDS[name].type
    if value is None:
        return None
    if "bool" in kind:
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in ("1", "true", "yes", "on"):
            return True
        if text in ("0", "false", "no", "off"):
            return False
        raise SettingsError(f"{_pascal(name)} must be true or false, got {value!r}")
    if kind.startswith("int"):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise SettingsError(f"{_pascal(name)} must be an integer, got {value!r}") from None
    if kind.startswith("float"):
        try:
            return float(value)
        except (TypeError, ValueError):
            raise SettingsError(f"{_pascal(name)} must be a number, got {value!r}") from None
    if kind.startswith("dict"):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as e:
                raise SettingsError(f"{_pascal(name)} must be JSON: {e}") from None
        if not isinstance(value, dict):
            raise SettingsError(f"{_pascal(name)} must be an object")
        return {str(k).lower(): [str(m) for m in (v or [])] for k, v in value.items()}
    if kind.startswith("list"):
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return [str(v) for v in value]
    text = str(value).strip()
    return text or None if "None" in kind else text


def load_settings(path: str | os.PathLike | None = None, env: Mapping[str, str] | None = None) -> Settings:
    env = os.environ if env is None else env
    path = Path(path or env.get(CONFIG_PATH_ENV) or DEFAULT_CONFIG_FILE)
    values: dict[str, Any] = {}
    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as e:
            raise SettingsError(f"{path} is not valid JSON: {e}") from None
        if not isinstance(raw, dict):
            raise SettingsError(f"{path} must hold a JSON object")
        for key, value in raw.items():
            if key.startswith("$") or key.startswith("_"):
                continue  # comments / schema hints
            name = _snake(key)
            if name not in _FIELDS:
                raise SettingsError(f"unknown setting {key!r} in {path}")
            values[name] = _coerce(name, value)
    elif path != DEFAULT_CONFIG_FILE:
        raise SettingsError(f"config file not found: {path}")
    for name in _FIELDS:
        env_key = ENV_PREFIX + name.upper()
        if env_key in env:
            values[name] = _coerce(name, env[env_key])
    return Settings(**values).validate()
