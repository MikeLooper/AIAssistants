"""Starting and stopping child process trees.

The reviewer script starts the AI tool's CLI as its own child, so cancelling a job must stop the whole tree,
not just the Python process."""

from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path
from typing import Sequence

IS_WINDOWS = os.name == "nt"


def start(cmd: Sequence[str], cwd: Path, env: dict | None = None) -> subprocess.Popen:
    kwargs: dict = {}
    if IS_WINDOWS:
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    child_env = dict(os.environ if env is None else env)
    child_env.setdefault("PYTHONIOENCODING", "utf-8")
    return subprocess.Popen(list(cmd), cwd=str(cwd), env=child_env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True,
                            encoding="utf-8", errors="replace", bufsize=1, **kwargs)


def kill_tree(proc: subprocess.Popen) -> None:
    """Stop `proc` and every process it started. Safe to call on a process that already ended."""
    if proc.poll() is not None:
        return
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, check=False)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except (OSError, ProcessLookupError):
        pass
    if proc.poll() is None:
        try:
            proc.kill()
        except OSError:
            pass
