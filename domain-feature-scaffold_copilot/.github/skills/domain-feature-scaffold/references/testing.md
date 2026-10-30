# Tests and Documentation

What Step 4 adds after the feature code is written: unit tests for all new code, Bruno tests for every new endpoint when the application is an API, and README updates. The tests are a best guess: a reasonable starting point the user will review and finish, not a verified suite. They don't have to pass. The stack-specific test framework, project layout and commands are in the language reference.

## Unit tests

### Which guidance to follow

Search the whole repository for a file named `unit-tests.instructions.md` (it is usually in `.github/instructions/`).

- **If one exists, follow it.** Its guidance on framework, libraries, project and file layout, naming, structure (for example Arrange-Act-Assert), test doubles, what to cover and how to run the tests takes precedence over the rest of this section and over the language reference. Use this section and the language reference only for what the file doesn't cover. If the file asks for something this skill otherwise forbids, such as a real database, follow the file and say so in the summary.
- **If none exists,** follow the standard best practices for the application's language: the defaults in the rest of this section and the "Unit tests" section of the language reference, adjusted to the conventions of any existing tests.

Say in the summary which one you followed.

### What to cover

Every new class with behaviour gets tests. DTOs and entities have no behaviour of their own and are covered through the mapping tests.

| New code | Tests |
|---|---|
| Repository | One test per action against an in-memory database (see the language reference). Cover the found and not-found paths: `GetById` returns `null`, `Update` / `Delete` return `false` for a missing id, `GetAll` returns an empty list on an empty table. |
| Service | One test per action with the repository interface replaced by a test double. Check that the service calls the repository with the mapped entity and maps the result back, and that `null` / `false` from the repository comes through unchanged. |
| Mapping | `ToEntity` and `ToDto` copy every field, and a DTO survives a round trip (`ToDto(ToEntity(dto))` equals `dto`). |
| Controller | One test per action with the service interface replaced by a test double. Check the status code for each outcome in [actions.md](actions.md) (`201` + `Location`, `200`, `204`, `404`, `400` where the codebase validates input). |
| Custom actions | The same as CRUD actions in each layer. A `TODO` body gets a test that pins down the current placeholder behaviour, with a `TODO` comment in the test pointing back to it. |
| Registration | Calling the Service registration registers the new repository and service interfaces, each exactly once. |

### Rules

- Put the tests in the test project that already covers the layer under test, following the existing tests' naming, folder layout, assertion style and test-double library. If there is no test project, create one per layer, or a single one if the codebase is a single project, using the stack's defaults from the language reference. List it in the plan.
- Prefer hand-written fakes over adding a mocking library. Add a test package only when the codebase already uses it, or when nothing else will do the job (an in-memory database provider, the test framework itself), and name every added package in the plan.
- Tests must not need a real database, network or running server. They run in any order, and each test creates its own data.
- Name tests after the behaviour they check (`GetByIdAsync_ReturnsNull_WhenSupplierDoesNotExist`), following the codebase's naming pattern if it has one.

### Running them

The tests must compile, because the solution has to build; fix compile errors in them. Beyond that, run the test suite once and report the passed / failed / skipped counts, with a one-line likely cause for each failing new test (for example "the in-memory database does not enforce the max length"). Don't iterate on failures, and don't change the feature code to make a test pass. A failure may point to a bug the user should look at, so list it rather than hiding it. If the tests can't run (missing SDK, no network for package restore), say so.

## Bruno tests (API applications only)

The application is an API when the Presentation layer exposes HTTP endpoints (ASP.NET Core controllers or minimal APIs, Spring `@RestController`, FastAPI / Flask routes). For an MVC or Razor application that only returns views, skip this section and say so in the summary.

### The collection

1. Look for an existing Bruno collection: a `bruno.json` file anywhere in the repository. Use it, and follow its folder layout, environment names, variable names and file format. Bruno collections are either `.bru` files or YAML (OpenCollection) files; write the new requests in the format the collection already uses.
2. If there is none, create one at `bruno/` in the repository root:

```
bruno/
├── bruno.json
├── environments/
│   └── Local.bru
└── <Domain>/
    ├── folder.bru
    ├── 01-create-<domain>.bru
    └── ...
```

`bruno.json`:

```json
{
  "version": "1",
  "name": "<Product> API",
  "type": "collection",
  "ignore": ["node_modules", ".git"]
}
```

`environments/Local.bru`, with the URL the API listens on locally (from `launchSettings.json`, `application.properties` / `application.yml`, or the uvicorn / Flask run command):

```
vars {
  baseUrl: http://localhost:5000
}
```

### The requests

Add one folder per domain (named `<Domain>`), with one request per endpoint, ordered with `seq` so the folder runs as a lifecycle against a clean or shared database:

| seq | Request | Asserts |
|---|---|---|
| 1 | Create | `201`, a `Location` header, the response body echoes the sent fields; saves the new id with `bru.setVar("<domain>Id", ...)` |
| 2 | Read one | `200` and the fields sent in step 1 |
| 3 | Read list | `200`, an array that contains the item created in step 1 |
| 4 | Update | `204`, then (in a `script:post-response` or a follow-up request) the changed field reads back |
| 5 | Custom actions | the status code from [actions.md](actions.md) |
| 6 | Delete | `204` |
| 7 | Read one after delete | `404` |
| 8 | Update / Delete a missing id | `404` (use an id that cannot exist, such as `0` or `-1`) |

Include only the requests for the actions the user asked for, plus the `404` checks that apply to them. If Create was not requested, take an existing id from an environment variable (`<domain>ExistingId`) and leave a `TODO` in the environment file to set it.

Example request:

```
meta {
  name: Create Supplier
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/api/suppliers
  body: json
  auth: none
}

body:json {
  {
    "companyName": "Bruno Test Supplier"
  }
}

script:post-response {
  bru.setVar("supplierId", res.getBody().id);
}

tests {
  test("returns 201 Created", function () {
    expect(res.getStatus()).to.equal(201);
  });

  test("returns a Location header", function () {
    expect(res.getHeader("location")).to.be.a("string");
  });

  test("echoes the company name", function () {
    expect(res.getBody().companyName).to.equal("Bruno Test Supplier");
  });
}
```

Match the JSON property casing the API actually emits (camelCase by default in ASP.NET Core and FastAPI, as declared in Spring). Use test data that is clearly marked as test data, and make the lifecycle delete what it created when Delete is one of the actions.

### Running them

Write the requests from the routes, DTO fields and status codes in the code; don't start the API or run them. Bruno tests need a running API and a database that has the table, which often isn't available yet (a placeholder table, a migration still to run).

In the summary, give the user the command to run them once the API is up, from the collection folder: `npx --yes --package @usebruno/cli bru run <Domain> --env Local` (or `bru run <Domain> --env Local` if the Bruno CLI is installed). Note anything you were unsure of, such as the JSON casing or the id property name.

## README updates

Update the README that describes the application the feature was added to: the one in the root of the repository, or the one next to the Presentation project if the projects have their own. Follow its existing sections and tone; add to them rather than adding a parallel structure.

Add or update, where the README has a place for it:

- the new feature or domain, in a list of features or domains
- the new endpoints (method, route, success status), in an API or endpoints section
- the table the feature uses, and any `TODO` it leaves (placeholder table, missing columns, a migration to run)
- how to run the unit tests and the Bruno collection, if the README doesn't already explain it (including a new Bruno collection or test project)

If the repository has no README, create a short `README.md` in its root with a description, how to build and run the application, how to run the tests, and the new feature's endpoints. Don't rewrite or reorganize unrelated parts of an existing README.
