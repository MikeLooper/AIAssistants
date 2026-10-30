# C# / .NET (ASP.NET Core)

## Recognizing the layers

| Layer | Typical project names | Contains |
|---|---|---|
| Domain | `*.Domain`, `*.Core`, `*.Models` | `<Domain>Dto` |
| Repository | `*.Repositories`, `*.Repository`, `*.Data`, `*.Infrastructure`, `*.Persistence` | `<Domain>Entity`, `I<Domain>Repository`, `<Domain>Repository`, repository registration |
| Service | `*.Services`, `*.Service`, `*.Application`, `*.Business` | `I<Domain>Service`, `<Domain>Service`, service registration |
| Presentation | `*.Api`, `*.Web`, `*.UI`, `*.Mvc` | Controller, `Program.cs` |

Check the project references (`<ProjectReference>` in each `.csproj`). The Service project must reference the Domain and Repository projects, and the Presentation project must reference the Service project. If a reference is missing, add it rather than working around it, and mention it in the summary.

## Files and names

Put new files in a feature folder named after the domain inside each project (for example `Pilot.Services/Suppliers/`) unless the codebase groups by technical role (`Services/`, `Interfaces/`), in which case follow it. Use file-scoped namespaces that match the folder, and one top-level type per file.

- `<Domain>Dto`: a `sealed record` (or a class, if existing DTOs are classes) in the Domain project. The Domain project must not reference EF Core or ASP.NET Core.
- `<Domain>Entity`: a class with settable properties in the Repository project. When EF Core is used, map the table in the `DbContext` (or an `IEntityTypeConfiguration<T>`, if the codebase uses them), not with attributes, unless the codebase uses attributes.
- `I<Domain>Repository` and `<Domain>Repository`: the interface takes and returns `<Domain>Entity`, never DTOs.
- `I<Domain>Service` and `<Domain>Service`: the interface takes and returns `<Domain>Dto`, never entities.

Use `async`/`await` with a `CancellationToken cancellationToken = default` parameter on every I/O method, and inject `ILogger<T>` where the existing classes do.

## Data access by technology

**EF Core** (a `DbContext` exists):
- Add `public DbSet<<Domain>Entity> <Domain>s => Set<<Domain>Entity>();` to the existing context (match the style of the other `DbSet` properties).
- In `OnModelCreating` (or a new `<Domain>EntityConfiguration`): `builder.Entity<<Domain>Entity>(e => { e.ToTable("<table>"); e.HasKey(x => x.Id); ... });`
- Reads use `AsNoTracking()`. Update loads the row, copies fields, and saves; return `false` if not found. Delete uses `ExecuteDeleteAsync` (EF Core 7+) or find-then-remove, matching what the codebase does.
- Do not create a migration unless the user asks; list it as a next step.

**Dapper** or **ADO.NET** (`IDbConnection`, `SqlConnection`, a connection factory):
- Keep the table name in one `private const string TableName = "<table>";`.
- Write explicit column lists and parameterized SQL only (`@Id`, `@Name`). Never concatenate values into SQL.
- Obtain connections the way the existing repositories do (factory, injected connection, connection string option).

## Registration

Look for an `IServiceCollection` extension method in each project (names like `AddRepositories`, `AddPilotRepositories`, `AddInfrastructure`, `AddServices`, `AddApplication`, often in `DependencyInjection.cs`, `ServiceCollectionExtensions.cs` or `*Registration.cs`).

- If one exists, add the new line to it: `services.AddScoped<I<Domain>Repository, <Domain>Repository>();`
- If none exists, create a `public static class` with `public static IServiceCollection Add<Product>Repositories(this IServiceCollection services)` (or `...Services`) and return `services`. Move nothing else into it unless the user agrees.
- Scoped is the right lifetime for repositories and services that use a scoped `DbContext` or connection; follow the codebase if it uses something else deliberately.

The chain the feature must leave in place:

```csharp
// Pilot.Services/ServiceRegistration.cs
public static IServiceCollection AddPilotServices(this IServiceCollection services, IConfiguration configuration)
{
    services.AddPilotRepositories(configuration);   // Service registration calls Repository registration
    services.AddScoped<ISupplierService, SupplierService>();
    return services;
}

// Pilot.Api/Program.cs
builder.Services.AddPilotServices(builder.Configuration);   // Presentation calls Service registration
```

If `Program.cs` currently calls the repository registration directly, remove that direct call once the service registration calls it, so each registration runs once. Pass through any arguments the repository registration needs (usually `IConfiguration`).

## Service skeleton

```csharp
namespace Pilot.Services.Suppliers;

/// <summary>Coordinates supplier operations between the API and the supplier repository.</summary>
public sealed class SupplierService(ISupplierRepository supplierRepository) : ISupplierService
{
    /// <inheritdoc />
    public async Task<SupplierDto?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        var entity = await supplierRepository.GetByIdAsync(id, cancellationToken);
        return entity is null ? null : ToDto(entity);
    }

    /// <summary>Maps a DTO received from a controller to the entity the repository stores.</summary>
    internal static SupplierEntity ToEntity(SupplierDto dto) => new()
    {
        Id = dto.Id,
        Name = dto.Name,
    };

    /// <summary>Maps an entity returned by the repository to the DTO sent back to a controller.</summary>
    internal static SupplierDto ToDto(SupplierEntity entity) => new(entity.Id, entity.Name);
}
```

Use a primary constructor or a classic constructor with a `private readonly` field, whichever the existing services use.

## Controller

- New controller: `[ApiController]`, `[Route("api/<route>")]` (or the route pattern the existing controllers use), derives from `ControllerBase`, named `<Domain>Controller` unless the user gave another name, and takes `I<Domain>Service` in its constructor.
- Existing controller: add `I<Domain>Service` as an additional constructor parameter alongside the existing ones; do not remove or reorder existing parameters.
- Return `ActionResult<T>` / `IActionResult` with the status codes in [actions.md](../actions.md), and add `[ProducesResponseType]` attributes where the existing controllers have them.

## Unit tests

These are the standard best practices for this stack. A `unit-tests.instructions.md` file in the repository takes precedence over them (see [testing.md](../testing.md)).

Test projects are named after the project they test (`Pilot.Services.Tests`, `Pilot.Api.Tests`) or are a single `*.Tests` / `*.UnitTests` project; they are usually under `tests/`. Follow the framework (xUnit, NUnit, MSTest), assertion library and test-double library they already use.

When there is no test project, create one per tested project under `tests/` with `dotnet new xunit`, add it to the solution (`dotnet sln add`, which also handles `.slnx`), and reference the project under test. Packages it needs beyond the xUnit template:

- Repository tests with EF Core: `Microsoft.EntityFrameworkCore.Sqlite`, at the same version as the EF Core package the Repository project uses. Open a `SqliteConnection("DataSource=:memory:")`, keep it open for the test, build the `DbContext` with `UseSqlite(connection)` and call `Database.EnsureCreated()`. Prefer SQLite to the EF Core InMemory provider, which does not support `ExecuteDeleteAsync` / `ExecuteUpdateAsync` or relational constraints.
- Repository tests with Dapper or ADO.NET: `Microsoft.Data.Sqlite`, if the SQL is portable to SQLite. If it uses SQL Server-only syntax, test the service and controller layers only and list the repository as covered by the Bruno tests.
- Controller tests: none; the test project references the Api project, and controllers are created directly with a fake service.

`ToEntity` / `ToDto` are `internal`, so add `[assembly: InternalsVisibleTo("<Product>.Services.Tests")]` (or an `<InternalsVisibleTo Include="..." />` item in the `.csproj`) to the Services project, matching how the codebase already does it. Write fakes as small classes implementing `I<Domain>Repository` / `I<Domain>Service`, unless the tests already use Moq or NSubstitute.

For the registration test, call `new ServiceCollection().Add<Product>Services(configuration)` with an in-memory `IConfiguration` (`new ConfigurationBuilder().AddInMemoryCollection(...)`) and assert on the `ServiceDescriptor`s rather than resolving services, so no database is needed.

Run `dotnet test` on the solution.

## Bruno base URL

Use the `http` URL from `Properties/launchSettings.json` of the Presentation project as `baseUrl`.

## Verify

Run `dotnet build` on the solution. Fix any error or new warning the change introduced. Run `dotnet test` once and report the result; failing new tests are reported, not fixed (see [testing.md](../testing.md)).
