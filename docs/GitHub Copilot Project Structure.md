# GitHub Copilot Project Structure

```
your-project-repository/
├── .github/
│   ├── agents/                       # Specialized AI role configurations
│   │   ├── example-terraform-expert.agent.md
│   │   └── example-api-reviewer.agent.md
│   │
│   ├── hooks/                        # Lifecycle automation and security policies
│   │   ├── hooks.json
│   │   ├── README.md
│   │   └── scripts/
│   │       └── example-validate.sh
│   │
│   ├── instructions/                 # Path-specific constraints
│   │   ├── example-typescript.instructions.md
│   │   └── example-api-design.instructions.md
│   │
│   ├── prompts/                      # Reusable chat templates & shortcut prompts
│   │   ├── example-code-review.prompt.md
│   │   └── README.md
│   │
│   ├── skills/                       # Reusable operational capabilities for agents
│   │   ├── example-generate-tests/
│   │   │   ├── SKILL.md
│   │   │   ├── README.md
│   │   │   ├── references/
│   │   │   │   └── example-testing-patterns.md
│   │   │   ├── templates/
│   │   │   │   └── example-test-template.ts
│   │   │   └── scripts/
│   │   │   	└── example-setup-test-env.sh
│   │   └── example-refactor-component/
│   │       ├── SKILL.md
│   │       └── README.md
│   │
│   └── copilot-instructions.md       # Global repository-wide rules & coding standards
│    
├── docs/
│   └── architecture.md
│    
├── src/
│   ├── backend/
│   │   ├── agents.md                 # Context-local agent file (takes directory precedence)
│   │   └── copilot-instructions.md   # Context-local intruction file (takes directory precedence)
│   └── frontend/
│    
└── README.md
```

## Notes
#### 1. Folder and File Naming:
| Type | Folder | Arrangement | Naming Pattern |
| --- | --- | --- | --- |
| Agent | agents | File | *.agent.md |
| Instruction | instructions | File | *.instructions.md |
| Skill | skills | Folder+File | skill-name/SKILL.md |
| Prompt | prompts | File | *.prompt.md |
#### 2. MCP Servers are not part of this structure - they are separately maintained applications.
