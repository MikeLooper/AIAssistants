# MCP Server Usage Demo

This directory contains a repository custom agent, `northwind-reporting`, that demonstrates how to use an MCP server from Copilot Chat to run a multi-step workflow.  The specific MCP server used in this demo can be found in the `../../PilotMcpServer` directory.

## Agent included in this demo

- Agent file: `agents/northwind-reporting.agent.md`
- Purpose: run Northwind exercises (parts 1-4) against a live Northwind API exposed through the `pilot` MCP server.
- Output:
  - Per-part reports in `docs/northwind-part-<N>-report-<yyyyMMdd>-<HHmmss>.md`
  - Cost summary in `docs/northwind-exercise-cost-summary-<yyyyMMdd>-<HHmmss>.md`
- Behavior highlights:
  - Defaults to all 4 parts, or accepts specific part numbers.
  - Reads all needed data with MCP tools, computes joins/aggregations client-side.
  - Allows only the two exercise writes defined in the workflow (add shipper, rename shipper).
  - Stops immediately on MCP/API failures and reports diagnostics.

## Required skills for this agent

The agent depends on these skill definitions:

- `skills/northwind-data-access/SKILL.md`
- `skills/northwind-report-writing/SKILL.md`
- `skills/northwind-exercises/SKILL.md`
- `skills/northwind-exercises/references/part-1.md`
- `skills/northwind-exercises/references/part-2.md`
- `skills/northwind-exercises/references/part-3.md`
- `skills/northwind-exercises/references/part-4.md`

## Install in another repository

To install this demo agent in a different repository, copy the agent and its skills into that repo's `.github` folder.

Target structure in the destination repository:

```text
.github/
  agents/
    northwind-reporting.agent.md
  skills/
    northwind-data-access/
      SKILL.md
    northwind-report-writing/
      SKILL.md
    northwind-exercises/
      SKILL.md
      references/
        part-1.md
        part-2.md
        part-3.md
        part-4.md
```

Optional but recommended:

- Ensure the destination repository has a `docs/` folder, because the agent writes report files there.

## MCP server prerequisites in the destination repository

This agent requires a registered MCP server named `pilot` in workspace configuration:

- File: `.vscode/mcp.json`
- Server name: `pilot`
- Must expose tools such as `list_apis`, `select_api`, and the Northwind `get_all_*` tools.

Example configuration (adjust paths for your machine):

```json
{
  "servers": {
    "pilot": {
      "type": "stdio",
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "C:/path/to/PilotMcpServer/src/PilotMcpServer"
      ]
    }
  }
}
```

Start the server from VS Code Command Palette using `MCP: List Servers`, then start `pilot`.

## Execute the agent

1. Open the destination repository in VS Code.
2. Confirm MCP server `pilot` is running and tools are available.
3. Open Copilot Chat in agent mode.
4. Select `northwind-reporting` from the agent picker.
5. Run with one of these prompts:
   - `Run all Northwind parts`
   - `Run parts 2 and 3 only`
   - `Run part 1 using Python with PostgreSQL`

The agent will generate report files in `docs/` and then return a short completion summary with created files and write verification.

## Related documentation

- Agent details: `agents/README.md`
- Agent definition: `agents/northwind-reporting.agent.md`
