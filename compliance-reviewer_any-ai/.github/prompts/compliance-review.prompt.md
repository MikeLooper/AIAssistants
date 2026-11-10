---
description: "Run a scored compliance review of a codebase (or resume a previous run)."
argument-hint: "<path to target repo> [subjects | resume run <id> [from step <NN>]] [--subjects …] [--advanced] [--analyzers …] [--programmatic] [--output text|file] [--out-file <path>] [--readme]"
agent: agent
tools: ['agent', 'read', 'search', 'edit', 'execute', 'todo']
---

GitHub Copilot adapter. Read `compliance-reviewer/ORCHESTRATOR.md` and follow it exactly.

Tool mapping for Copilot: ask the user = ask-questions tool; delegate to a worker = subagent `compliance-subject-reviewer` (`.github/agents/compliance-subject-reviewer.agent.md`); shell = terminal; todo list = `todo`.

User input: ${input:request:<path to target repo> [subjects | resume run <id>] [flags]}
