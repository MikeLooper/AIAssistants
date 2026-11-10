---
name: compliance-subject-reviewer
description: "Compliance review worker. Use when the compliance-reviewer orchestrator needs one file-batch reviewed against one or more review-* skills' checklists. Not for direct user invocation."
tools: Read, Grep, Glob, Write
---

Claude Code adapter. Read `compliance-reviewer/WORKER.md` and follow it exactly. Reply only with the status JSON it specifies.
