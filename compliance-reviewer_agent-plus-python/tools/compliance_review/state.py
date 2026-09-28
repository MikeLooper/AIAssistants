"""Transition-file and state.json handling per
.github/skills/compliance-review-core/references/transition-schema.md

Handles run-id generation, step-file naming (including .part-K batches),
state.json read/write, and the three resume rules:
  1. list runs whose state.json status != completed
  2. `resume run <id>`: continue from the first non-completed step
  3. `resume run <id> from step <NN>`: move NN.. onward to superseded/, re-run
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def make_run_id(target_path: str, now: Optional[datetime] = None) -> str:
    now = now or datetime.now()
    short_name = re.sub(r"[^a-z0-9]+", "", Path(target_path).name.lower()) or "target"
    return f"{now:%Y-%m-%d_%H%M}-{short_name}"


def compute_inputs_hash(
    target_path: str,
    target_git_head: Optional[str],
    subjects: list[str],
    analyzer_approval: str,
) -> str:
    payload = json.dumps(
        {
            "targetPath": target_path,
            "targetGitHead": target_git_head,
            "subjects": sorted(subjects),
            "analyzerApproval": analyzer_approval,
        },
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


@dataclass
class StateFile:
    runId: str
    targetPath: str
    subjects: list[str]
    targetGitHead: Optional[str] = None
    inputsHash: Optional[str] = None
    startedAt: str = field(default_factory=now_iso)
    updatedAt: str = field(default_factory=now_iso)
    status: str = "in-progress"
    analyzerApproval: str = "none"
    linkApprovals: dict[str, str] = field(default_factory=dict)
    steps: dict[str, str] = field(default_factory=dict)
    reportPath: Optional[str] = None
    schemaVersion: int = 1

    @classmethod
    def load(cls, path: Path) -> "StateFile":
        data = json.loads(path.read_text(encoding="utf-8"))
        data.pop("schemaVersion", None)
        return cls(**data)

    def save(self, path: Path) -> None:
        self.updatedAt = now_iso()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schemaVersion": self.schemaVersion,
            "runId": self.runId,
            "targetPath": self.targetPath,
            "targetGitHead": self.targetGitHead,
            "inputsHash": self.inputsHash,
            "startedAt": self.startedAt,
            "updatedAt": self.updatedAt,
            "status": self.status,
            "subjects": self.subjects,
            "analyzerApproval": self.analyzerApproval,
            "linkApprovals": self.linkApprovals,
            "steps": self.steps,
            "reportPath": self.reportPath,
        }
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class RunPaths:
    """Resolves file paths for one run under `transitions_root/<runId>/`."""

    def __init__(self, transitions_root: Path, run_id: str):
        self.root = transitions_root / run_id
        self.superseded = self.root / "superseded"

    def state_path(self) -> Path:
        return self.root / "state.json"

    def step_path(self, step_id: str, batch_index: Optional[int] = None) -> Path:
        name = f"{step_id}.part-{batch_index}.json" if batch_index else f"{step_id}.json"
        return self.root / name

    def ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)


def list_resumable_runs(transitions_root: Path) -> list[str]:
    """Run ids whose state.json exists and status != completed, newest first."""
    if not transitions_root.exists():
        return []
    candidates: list[tuple[float, str]] = []
    for run_dir in transitions_root.iterdir():
        state_path = run_dir / "state.json"
        if not state_path.is_file():
            continue
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if state.get("status") != "completed":
            candidates.append((state_path.stat().st_mtime, run_dir.name))
    candidates.sort(reverse=True)
    return [run_id for _, run_id in candidates]


def first_incomplete_step(state: StateFile, ordered_step_ids: list[str]) -> Optional[str]:
    for step_id in ordered_step_ids:
        if state.steps.get(step_id) != "completed":
            return step_id
    return None


def resume_from_step(paths: RunPaths, state: StateFile, ordered_step_ids: list[str], from_step: str) -> None:
    """Moves `from_step` and every later step's transition file(s) to superseded/,
    and resets their status to not-started, per resume rule 3."""
    if from_step not in ordered_step_ids:
        raise ValueError(f"Unknown step id: {from_step}")
    paths.superseded.mkdir(parents=True, exist_ok=True)
    idx = ordered_step_ids.index(from_step)
    for step_id in ordered_step_ids[idx:]:
        for f in paths.root.glob(f"{step_id}*.json"):
            f.rename(paths.superseded / f.name)
        state.steps[step_id] = "not-started"
