---
name: compliance-reviewer
description: "Compliance review orchestrator. Use when the user asks to review, audit or assess a codebase for architecture, coding standards, security or compliance against standards like OWASP, ISO/IEC 25010, the Twelve-Factor App or REST API design guidelines, or asks to resume a previous compliance review run."
argument-hint: "<path to target repo> [subjects | resume run <id> [from step <NN>]] [--subjects …] [--advanced] [--analyzers …] [--programmatic] [--output text|file] [--out-file <path>] [--readme]"
---

Claude Code adapter. The full, provider-neutral instructions live in `compliance-reviewer/ORCHESTRATOR.md`. Read that file now and follow it exactly.

Tool mapping for Claude Code: ask the user = `AskUserQuestion`; delegate to a worker = Agent tool with `subagent_type: "compliance-subject-reviewer"` (defined in `.claude/agents/compliance-subject-reviewer.md`); shell = `Bash`; todo list = `TodoWrite`.

Arguments passed to this skill (may be empty): $ARGUMENTS
