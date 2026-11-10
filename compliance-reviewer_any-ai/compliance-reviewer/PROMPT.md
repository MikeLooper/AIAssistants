# Compliance review prompt (paste into any AI chat)

Use this when your AI tool cannot read repository instruction files automatically (e.g. ChatGPT web, other chat UIs). Attach or upload the `compliance-reviewer/` folder (and the target code, or give file access), then paste:

```text
You are a compliance review orchestrator. Read compliance-reviewer/ORCHESTRATOR.md and follow it exactly.
You have no subagents, so use its "Fallback (no subagents)" section: for each file batch, read
compliance-reviewer/WORKER.md and perform that procedure yourself.
All skills are in compliance-reviewer/skills/<name>/SKILL.md. Never modify the target code.
Write transition files under transitions/<runId>/ and the report under docs/reports/.
If you cannot write files or run Python, return each transition file as a JSON code block with its
intended path, and give me the commands to run
compliance-reviewer/skills/compliance-report/scripts/compliance_report.py (validate, aggregate, render).

Target: <path or description of the code to review>
Flags: (optional, e.g. --subjects all --advanced; leave empty to be interviewed)
```

The flags are described under "Operational flags" in `compliance-reviewer/README.md`. `--programmatic` is meant for unattended tools, not chat.
