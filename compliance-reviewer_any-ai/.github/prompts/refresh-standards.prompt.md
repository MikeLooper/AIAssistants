---
description: "Maintainer tool: drift-check or refresh the Compliance Reviewer's localized standards (never part of a review)."
argument-hint: "[<skill> ... | all] [check | gaps | full]"
agent: agent
tools: ['read', 'search', 'edit', 'execute', 'todo', 'fetch']
---

GitHub Copilot adapter. Read `compliance-reviewer/REFRESH.md` and follow it exactly.

Tool mapping for Copilot: ask the user = ask-questions tool; shell = terminal; fetch = `fetch` (approved pages only; prefer the drift script); todo list = `todo`.

User input: ${input:request:[<skill> ... | all] [check | gaps | full]}
