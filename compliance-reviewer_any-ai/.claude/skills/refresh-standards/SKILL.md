---
name: refresh-standards
description: "Maintainer tool for the Compliance Reviewer: check the review skills' localized standards for source drift, collect localized-standard-gap notes, and refresh a skill's standards. Use when the user asks to refresh, update, re-pin or drift-check the standards, process 'Refresh due' items, or collect gap notes. Never part of a compliance review."
argument-hint: "[<skill> ... | all] [check | gaps | full]"
---

Claude Code adapter. The full, provider-neutral instructions live in `compliance-reviewer/REFRESH.md`. Read that file now and follow it exactly.

Tool mapping for Claude Code: ask the user = `AskUserQuestion`; shell = `Bash`; fetch = `WebFetch` (approved pages only; prefer the drift script); todo list = `TodoWrite`.

Arguments passed to this skill (may be empty): $ARGUMENTS
