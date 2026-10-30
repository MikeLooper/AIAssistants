# Domain Feature Scaffold (Claude Code)

A Claude Code skill that adds a new domain feature through every layer of an existing layered application (Domain, Repository, Service, Presentation). It interviews you first, then creates the classes, data access, mapping, controller actions and dependency-injection registrations. After the code, it adds best-guess unit tests for all new code, best-guess [Bruno](https://www.usebruno.com/) tests for every new endpoint when the application is an API, and README updates. The tests are a starting point to review; they aren't required to pass. The same skill for GitHub Copilot is in [`domain-feature-scaffold_copilot`](../domain-feature-scaffold_copilot/README.md).

## What It Creates

| Layer | Created or changed |
|---|---|
| Domain | `<Domain>Dto` |
| Repository | `<Domain>Entity` mapped to the chosen table, the repository interface and `<Domain>Repository` class with data-access logic for the chosen actions, and a registration line in the layer's common registration method |
| Service | The service interface and `<Domain>Service` class (takes the repository interface in its constructor), `ToEntity` / `ToDto` mapping methods, and a registration line. The Service registration calls the Repository registration. |
| Presentation | Action methods on a new or existing controller (takes the service interface in its constructor), and a startup call to the Service registration |
| Unit tests | Tests for the new repository (against an in-memory database), service, mapping methods, controller actions and registration, in the existing test projects or a new one. They follow the repository's `unit-tests.instructions.md` if there is one, and otherwise the standard best practices for the language. They must compile; the skill runs them once and reports the results, with a likely cause for each failure, but doesn't fix failures. |
| Bruno tests | API applications only: one request per new endpoint, with status-code assertions, in the existing Bruno collection or a new `bruno/` collection. Written from the code without running them; the final message gives the command to run them once the API and database are up. |
| README | The application's README gains the new feature, its endpoints, its table, any `TODO`s, and how to run the tests |

C#/.NET is the primary target. Java (Spring Boot) and Python (FastAPI/Flask) are supported through per-language reference files. The codebase's existing conventions are followed wherever they don't conflict with the four required class-name suffixes (`Dto`, `Entity`, `Repository`, `Service`).

## The Interview

| # | Question |
|---|---|
| A | What is the name of the new process domain? (used in every class and interface name) |
| B | All CRUD actions, or only some? Custom actions can be added by name. |
| C | What is the target (or placeholder) table name? |
| D | Which controller should receive the new methods? An existing one, or a new one. |

Answers you include in your request are not asked again, so `/domain-feature-scaffold Supplier, all CRUD, table Suppliers, new controller` runs without questions. Before writing files, the skill shows the plan.

## Files

| Path | Role |
|---|---|
| `.claude/skills/domain-feature-scaffold/SKILL.md` | Workflow: inspect, interview, create, test and document, verify |
| `.claude/skills/domain-feature-scaffold/references/actions.md` | How each CRUD or custom action maps to methods, routes and status codes |
| `.claude/skills/domain-feature-scaffold/references/testing.md` | What the unit tests cover, the Bruno collection and requests, and the README updates |
| `.claude/skills/domain-feature-scaffold/references/languages/` | `csharp.md`, `java.md`, `python.md`: layer detection, naming, data access, registration, unit test setup and how to start the API per stack |
| `.claude/skills/domain-feature-scaffold/evals/` | Test cases, each with a small .NET `Pilot` solution under `files/` |

## Usage

1. Copy `.claude/skills/domain-feature-scaffold/` into the target repository's `.claude/skills/`, or into `~/.claude/skills/` to use it in every project.
2. In Claude Code, run `/domain-feature-scaffold`, or ask something like "add a Supplier feature through all the layers".
3. Answer the interview, review the plan, and let it build. The final message lists the files changed, the routes added, the unit test and Bruno results, any `TODO`s left behind, and next steps such as a database migration.

## Tests

`evals/` holds three test cases in the `claude plugin eval` format:

- `full-crud-new-controller`: all answers are given up front. Also checks that the unit tests and Bruno requests are written, the unit test result is reported honestly, and the README is updated.
- `partial-crud-custom-action-placeholder`: a subset of CRUD, a custom action, a placeholder table and an existing controller. Also checks that the unit tests and Bruno requests are written, for the requested actions only.
- `interviews-before-writing`: only the domain name is given, so the skill must ask questions before writing anything.

To run them from the skill folder: `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`. These are billed model runs.
