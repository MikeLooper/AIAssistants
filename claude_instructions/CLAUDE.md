# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<repository description>.

## Commands

```bash
dotnet build <application name>.sln
dotnet test <application name>.sln
dotnet test <application name>.sln --settings .runsettings --collect "Code Coverage"
dotnet run --project src/<application name>.Web
```

All tests, integration tests included, run without a database.

## Layout

<description of project layout/structure>.

## Code style

Match existing code over the generic rules in `.github/instructions/coding.instructions.md`: block-scoped namespaces, tabs, `this.`-qualified members, dependencies as protected get-only properties (no `_camelCase` fields), XML docs on all public/protected members. Every database or external operation must be logged and carry the CorrelationId.

Topic-specific guidance lives in `.claude/rules/` and loads when you work on matching files.
