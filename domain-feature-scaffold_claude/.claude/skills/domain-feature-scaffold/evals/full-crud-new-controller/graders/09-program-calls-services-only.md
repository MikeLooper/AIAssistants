---
type: llm
focus: trace
weight: 1
---

Program.cs calls AddPilotServices and no longer calls AddPilotRepositories directly, so the repository registration runs once.
