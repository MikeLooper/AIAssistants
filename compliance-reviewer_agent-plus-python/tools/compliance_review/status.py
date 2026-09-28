"""Status line formatting per
.github/skills/compliance-review-core/references/status-format.md
"""
from __future__ import annotations


def format_status_line(
    step_index: int,
    total_steps: int,
    step_name: str,
    next_name: str,
    remaining_names: list[str],
    severity_counts: dict[str, int],
    report_path: str | None = None,
) -> str:
    remaining = "none" if not remaining_names else ", ".join(remaining_names)
    if report_path is not None:
        line1 = f"Step {step_index}/{total_steps}: {step_name} done. Next: done. Report: {report_path}"
    else:
        line1 = f"Step {step_index}/{total_steps}: {step_name} done. Next: {next_name}. Remaining: {remaining}"
    line2 = (
        "Findings so far — "
        f"Error: {severity_counts.get('Error', 0)}, "
        f"Warning: {severity_counts.get('Warning', 0)}, "
        f"Information: {severity_counts.get('Information', 0)}"
    )
    return f"{line1}\n{line2}"
