"""Deterministic (non-LLM) subset of the compliance-reviewer pipeline.

Implements Phase 1 (inventory, scoring, aggregate, report, transition/state
handling) and Phase 2 (tool-backed analyzer checks) from
docs/compliance-review-agent-plan.md's Python-conversion plan. Checks that
require reading code semantically are left as `N/A` with a
"requires semantic review" reason — see cli.py's `--list-unevaluated`.

Usage:
    python -m compliance_review <target-path> [--subjects a,b,c] [--run-analyzers]
"""

__all__ = ["schemas", "state", "inventory", "scoring", "analyzers", "aggregate", "report", "cli"]
