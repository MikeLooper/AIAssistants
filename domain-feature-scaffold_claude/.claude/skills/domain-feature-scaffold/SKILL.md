---
name: domain-feature-scaffold
description: Initializes a new domain feature across a layered application (Domain, Repository, Service and Presentation/UI projects) by interviewing the user, then creating the DTO, entity, repository and service classes and interfaces, the data-access logic, the DTO/entity mapping, the controller actions and the chained dependency-injection registrations, followed by best-guess unit tests for all new code, best-guess Bruno tests for every new API endpoint, and README updates. Use whenever the user wants to add, scaffold, initialize, stub out or wire up a new feature, domain, resource, table or CRUD endpoint end to end through the layers of an existing C#/.NET, Java/Spring or Python application, even if they only say something like "add a Supplier feature" or "I need CRUD for the Invoices table".
argument-hint: "[domain name] [optional: actions, table, controller]"
---

# Domain Feature Scaffold

Adds one new domain feature to an existing layered application, through every layer, so that a request to the controller travels down to the database and back. Then it adds best-guess unit tests and, for an API, best-guess Bruno tests, and documents the feature in the README:

```
Controller ──I<Domain>Service──▶ <Domain>Service ──I<Domain>Repository──▶ <Domain>Repository ──▶ <table>
   <Domain>Dto ◀──── ToDto / ToEntity ────▶ <Domain>Entity
```

The four layers are referred to below as **Domain**, **Repository**, **Service** and **Presentation**. In a single-project codebase they are folders or packages; in a multi-project codebase they are projects or modules.

## Step 1: Inspect the application

Do this before interviewing, so the questions can offer real choices (existing controllers, tables, the data-access technology) instead of blanks.

1. Detect the language and framework, then read the matching reference file. Only read the one you need:
   - C# / .NET (`*.sln`, `*.slnx`, `*.csproj`): [references/languages/csharp.md](references/languages/csharp.md)
   - Java / Spring Boot (`pom.xml`, `build.gradle`): [references/languages/java.md](references/languages/java.md)
   - Python (`pyproject.toml`, `requirements.txt`): [references/languages/python.md](references/languages/python.md)
   - Anything else: apply the same layer rules using that stack's own idioms, and tell the user you have no stack-specific guidance for it.
2. Locate the four layers. If one is missing, stop and ask the user whether to create it or which existing project should play its role. Creating projects is a bigger change than this skill should make on its own.
3. Find one existing feature that already goes through all the layers and use it as the model for file placement, naming, constructor style, async style, logging, documentation comments and route style. The codebase's own conventions win over the defaults in this skill, except for the four naming rules in Step 3, which the user asked for.
4. Note:
   - the data-access technology (EF Core, Dapper, ADO.NET, JPA, JDBC, SQLAlchemy and so on)
   - the existing registration method in the Repository, Service and Presentation layers, if any
   - the existing controllers
   - any table definitions you can see (DbContext mappings, migrations, `.sql` scripts, entity annotations)
   - the existing test projects, test framework and test-double library, and which layers they cover
   - a `unit-tests.instructions.md` file anywhere in the repository (usually `.github/instructions/`); if there is one, read it
   - whether the application is an API (it exposes HTTP endpoints), and any existing Bruno collection (a `bruno.json` file)
   - the README that describes the application, if any
5. If repository or project instruction files exist (`CLAUDE.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`), follow them for anything not covered by this skill.

## Step 2: Interview the user

Ask these four questions. Skip any the user already answered in their request, and don't re-ask them.

- **A. Domain name.** What is the name of the new process domain? It goes into the name of every new class and interface so they read as related. Normalize it to PascalCase singular (`purchase orders` becomes `PurchaseOrder`) and confirm the normalized form if it changed.
- **B. Actions.** Should all CRUD actions be implemented (Create, Read, Update, Delete), or only some? The user may also name one or more custom actions outside basic CRUD (for example `Archive`, `MarkDelivered`).
- **C. Table.** What is the target table name, or a placeholder name if the table does not exist yet?
- **D. Controller.** Which controller should receive the new action methods: an existing one, or a new one (default name `<Domain>Controller`)?

How to ask:

- Ask A first, in plain text, unless it was given. The other questions' suggested answers depend on it.
- Then ask B, C and D together with the AskUserQuestion tool:
  - **B:** `multiSelect: true` with options Create, Read, Update and Delete. Custom actions come in through the automatic "Other" field. Say so in the question text: "add custom action names under Other, comma-separated".
  - **C:** offer the plural of the domain name (for example `Suppliers`) and any matching table you found in Step 1. "Other" covers any other name.
  - **D:** offer "New `<Domain>Controller`" first, then up to three existing controllers that look related.
- If no data-access technology was found in Step 1, add a fourth question asking which to use, with the stack's usual default first. Choosing it yourself would add a dependency the user didn't ask for.

Then work out the entity's columns:

- **Table defined in the codebase:** map its columns.
- **Table that exists only in a database you can't see:** ask the user for the columns, or offer to create an `Id` key with a `TODO` for the rest.
- **Placeholder table:** create an `Id` key plus a `TODO` comment listing what still needs filling in, and keep the table name in one constant or mapping so it is a one-line change later.

Don't guess column lists. A plausible-looking but wrong schema is worse than a visible `TODO`.

Before writing any files, show a short plan: the normalized names, the actions, the table, the controller, and the list of files you will create or modify, including the test files, any new test project and the packages it adds, the Bruno requests (or why there are none), and the README. If the user already gave all four answers up front and nothing was ambiguous, go straight on after the plan. Otherwise wait for a go-ahead.

## Step 3: Create the feature

Four naming rules come from the user's specification, and every other choice bends around them:

1. The DTO class name ends in `Dto`.
2. The entity class name ends in `Entity`.
3. The repository class name ends in `Repository`.
4. The service class name ends in `Service`.

The domain name is part of the name of the DTO, the repository class and interface, and the service class and interface. The language reference gives the exact default names for each stack.

For the method names, signatures, routes and status codes that each action becomes, see [references/actions.md](references/actions.md).

### Domain
- Create `<Domain>Dto` with the fields from the column list. It must not depend on persistence or web frameworks, because every other layer references it.

### Repository
- Create `<Domain>Entity`, mapped to the table from question C.
- Create the repository interface and the `<Domain>Repository` class. Add one method per action from question B, working with `<Domain>Entity`, and implement each with the data-access technology already in use against the table from question C. Use parameterized queries only.
- Register the interface and class in this layer's common registration method. Create the method if none exists.

### Service
- Create the service interface and the `<Domain>Service` class. Add one method per action from question B, working with `<Domain>Dto`.
- Take the repository interface as a constructor parameter.
- Add the two mapping methods to the service class:
  - `ToEntity(<Domain>Dto)` is used on the way down, when a controller passes domain data toward the repository.
  - `ToDto(<Domain>Entity)` is used on the way up, when the repository returns data for a controller.

  Keep both off the service interface, because controllers should never see entities.
- Register the interface and class in this layer's common registration method. Create the method if none exists.
- Make sure the Service registration calls the Repository registration, so the Presentation layer only has to know about the Service layer.

### Presentation
- Add the action methods to the controller from question D, or create that controller.
- Take the service interface as a constructor parameter. In an existing controller, keep its current parameters and add this one.
- Make sure the Presentation startup (`Program.cs`, the Spring application class, `main.py`) calls the Service registration. If it also calls the Repository registration directly, remove that direct call now that the Service registration makes it, and mention the change.

Keep changes scoped to these files. Don't refactor neighbouring code, rename existing members, or add packages without asking (other than the test packages listed in the plan).

## Step 4: Test and document

After the feature code builds, add the following. [references/testing.md](references/testing.md) has the details, and the language reference has the stack's test framework and commands.

1. **Unit tests, best guess.** If the repository has a `unit-tests.instructions.md` file, follow its guidance. Otherwise follow the standard best practices for the application's language, as described in the language reference. Cover all new code: repository, service, mapping methods, controller actions and registration. The tests must compile, so the solution still builds, but they don't have to pass. Run them once and report the result; don't iterate on failures or change the feature code to satisfy a test.
2. **Bruno tests, best guess, if the application is an API.** Add one request per new endpoint, with `tests` assertions on the status codes from [references/actions.md](references/actions.md), to the existing Bruno collection or a new one. Write them from the routes and DTOs; don't start the API or run them.
3. **README.** Add the new feature, its endpoints, its table and any `TODO`s to the application's README, along with how to run the tests if it doesn't already say.

## Step 5: Verify and report

1. Build or compile, and run the whole test suite, using the commands in the language reference. Fix anything this change broke. If the build can't run (missing SDK, no network for package restore), say so plainly rather than claiming success.
2. Report the unit test result from the real output of the run. Don't describe failing tests as passing, or the Bruno tests as verified.
3. Check the dependency chain: Presentation calls the Service registration, the Service registration calls the Repository registration, and each new interface is registered exactly once.
4. Finish with a short summary:
   - the files created and modified, grouped by layer, then the test files, Bruno requests and README
   - the routes added
   - the unit test result (passed / failed / skipped counts, with a one-line likely cause for each failure), and the command to run the Bruno tests
   - every `TODO` left behind and why
   - next steps the user probably needs, such as a database migration or real column definitions for a placeholder table
