# Copilot Instructions

## Repository & Environment

- **Environment**: Windows with PowerShell (`pwsh`).
- **Configuration**:
  - Auto-approved terminal commands for file discovery and inspection are defined in [.vscode/settings.json](.vscode/settings.json).
  - Configured Model Context Protocol (MCP) servers (such as `pilot`) are specified in [.vscode/mcp.json](.vscode/mcp.json).
- Inspect the workspace and repository before assuming a specific language, framework, build command, test runner, or deployment target.

## MCP Server & Tool Handling

- When invoking MCP tools (e.g., Pilot MCP server endpoints), immediately inspect returned responses for error messages or non-success statuses.
- If an MCP tool call fails or returns an API error status, stop further automated processing and report full diagnostic details (status code, description, endpoint) to prevent wasted resources.

## Working Conventions

- Keep edits focused on the requested behavior. Do not reformat or refactor unrelated code.
- Follow existing project conventions once source code and configuration are present.
- Prefer existing dependencies and standard-library features before adding packages.
- Do not add secrets, credentials, generated artifacts, or local environment files to source control.
- Run the narrowest available validation after each change, then report any checks that could not be run.

## Documentation

Keep documentation in `docs/` and project configuration guidance current when introducing build systems, prerequisites, environment variables, or workflows.

