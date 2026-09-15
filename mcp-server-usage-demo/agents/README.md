# Northwind Reporting Agent

A workspace custom agent that runs the Northwind exercises from the
`northwind-exercises` skill against a live Northwind database through the `pilot`
MCP server, and writes one timestamped Markdown report per exercise part into
`docs/`.

## What it does

- Connects to a Pilot API deployment via the `pilot` MCP server (six equivalent
  Northwind deployments; the default is .NET Core with SQL Server).
- Executes the exercises in Parts 1-4: 30 read-only reports plus 2 small writes
  (add shipper `Amazon`, then rename it to `Amazon Prime Shipping`).
- Writes `docs/northwind-part-<N>-report-<yyyyMMdd>-<HHmmss>.md` for each part.
- Writes a separate `docs/northwind-exercise-cost-summary-<yyyyMMdd>-<HHmmss>.md`
  containing credits per exercise and the overall credits total.
- Ends with a chat summary: report files created, empty result sets, and write
  verification.

## Prerequisites

1. The MCP server source checked out at
   `C:\Working\Storage\Dev\GitHub\PilotMcpServer` (with its
   `shared/PilotSharedSource` submodule initialized) and the .NET 10 SDK on PATH.
2. At least one Pilot API deployment running, such as
   `pilot-api-dotnet-mssql` (localhost:55101). Check with `docker ps`.
3. The server registered for this workspace in `.vscode/mcp.json`:
- Pointing to the source code to be built as-needed:
   ```json
   {
     "servers": {
       "pilot": {
         "type": "stdio",
         "command": "dotnet",
         "args": ["run", "--project", "C:/Working/Storage/Dev/GitHub/PilotMcpServer/src/PilotMcpServer"]
       }
     }
   }
   ```
- Pointing to a built/published `PilotMcpServer.exe` directly for a faster startup than `dotnet run`.  If the MCP Server has not been built, refer to the MCP Server [README](..\..\..\PilotMcpServer\README.md) for directions on building the MCP Server.
```json
{
  "servers": {
    "pilot": {
      "type": "stdio",
      "command": "C:/Working/Storage/Dev/GitHub/PilotMcpServer/src/PilotMcpServer/bin/Debug/net10.0/PilotMcpServer.exe",
      "args": []
    }
  }
}
```

4. Start the server from Command Palette -> `MCP: List Servers` -> `pilot` so
   its tools are available to the agent.

## How to run

The agent lives at
[.github/agents/northwind-reporting.agent.md](../agents/northwind-reporting.agent.md).
Use it from the Agents picker in Copilot Chat, or invoke it by name in agent mode.

The agent accepts optional natural-language arguments, such as `run parts 2 and 3
only` or `use Python with PostgreSQL`.

## Outputs

One file per part per run, for example
`docs/northwind-part-2-report-20260906-143210.md`. Each report contains a header
(timestamp, deployment, table row counts) and one section per exercise with goal,
data used, logic, a result table with row count, and notes. The exact format is
defined by the `northwind-report-writing` skill.

## Supporting skills

The agent uses these workspace skills:

- [northwind-data-access](../skills/northwind-data-access/SKILL.md) - MCP tool
  inventory, record fields, join keys, revenue math, snapshot strategy, and
  write-safety rules.
- [northwind-report-writing](../skills/northwind-report-writing/SKILL.md) -
  report file naming, section structure, formatting rules, and credit summaries.
- [northwind-exercises](../skills/northwind-exercises/SKILL.md) - the four
  exercise reference files and credit-summary workflow.

## Caveats

- The Northwind databases behind the Pilot APIs are shared, mutable state.
  Exercise 1.9 inserts a row and 2.1 updates it. The agent skips the insert if
  `Amazon` already exists, but data changed by other users can shift report
  numbers between runs.
- The agent never deletes data. If test shippers pile up, remove them manually;
  `delete_shipper` exists in the MCP server but is not used by the agent.

## Troubleshooting

- **`pilot` tools missing in chat** - confirm `.vscode/mcp.json`, then start
  `pilot` from `MCP: List Servers`; verify `dotnet --version` works in a terminal.
- **`list_apis` shows everything offline** - start the API containers with
  `docker ps -a` and `docker start <container>`.
- **First call is slow** - `dotnet run` builds the server on first launch; point
  `command` at a prebuilt `PilotMcpServer.exe` to remove the delay.
