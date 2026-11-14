# AI Assistants

AI Assistants to accomplish a multitude of tasks.

## Notable AI Assistants

`claude_instructions` - Rules to use with Claude.  Topic-specific guidance that loads when you work on matching files.

`compliance-reviewer_any-ai` - An agent for determining how well application source code is complying with standards and best-practices.  This assistant uses only agents, skills, and related AI tooling.  This assistant is designed to work with any AI provider.
- [README](compliance-reviewer_any-ai\compliance-reviewer\README.md)

`copilot-instructions` - Rules to use with Copilot.  Topic-specific guidance that loads when you work on matching files.
- [Instructions](copilot-instructions\copilot-instructions.md)

`domain-feature-scaffold_claude` / `domain-feature-scaffold_copilot` - A skill (one version for Claude Code, one for GitHub Copilot) that interviews you, then adds a new domain feature through every layer of a layered application: DTO, entity, repository, service, controller actions and chained dependency-injection registration.
- [README (Claude)](domain-feature-scaffold_claude/README.md)
- [README (Copilot)](domain-feature-scaffold_copilot/README.md)

`job-search-agent` - A Job Search tool will read job boards and present a display of how well listed jobs match some specified search criteria.
- [README](job-search-agent/README.md)

`mcp-server-usage-demo` - A demo of how to use a MCP server in an agent.
- [README](mcp-server-usage-demo/README.md)

`unit-tests-logic-assessment-agent` - An agent-driven AI agent that evaluates unit tests based on code logic and element coverage, not line coverage.
- [README](unit-tests-logic-assessment-agent\README.md)

`unit-tests-logic-assessment-prompt` - A prompt-driven AI agent that evaluates unit tests based on code logic and element coverage, not line coverage.
- [README](unit-tests-logic-assessment-prompt\README.md)
