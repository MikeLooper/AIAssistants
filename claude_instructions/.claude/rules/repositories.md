---
paths:
  - "src/PilotApi.Repositories/**"
  - "src/PilotApi.Shared/Builders/**"
  - "src/PilotApi.Shared/Utilities/DataSourceUtilities.cs"
---

# Repositories and data access

- `RepositoryBase<TEntity>` holds all Dapper CRUD logic. Concrete repositories only supply metadata: `TableName`, `ColumnNames`, `EntityColumns`, `KeyColumnNames`, and optionally `KeyColumnDataTypes`/`CreateKey`.
- Each metadata property switches on `DataSourceContext.DataSourceConfiguration.DataSourceEnum`, because SQL Server (PascalCase) and PostgreSQL (lowercase) table and column names differ. `ColumnNames` and `EntityColumns` must map one-to-one. `Validate()` checks the metadata.
- SQL text comes from `ISqlBuilder`. For PostgreSQL inserts with `CreateKey`, `GetNextIdsAsync` pre-fetches key values, which `EntityUpdateHandler` writes onto the entity.
- `DataSourceContext` owns the connection and transaction. Each method commits on success, rolls back on failure or zero affected rows, and closes the connection in `finally`.
- Each database call is wrapped with `LogDatabaseCallStart`/`LogDatabaseCallEnd`, with the end logged in `finally`. New database methods must do the same. The correlation ID, request ID and caller name come from the request log context, not from the repository.
- The active data source is chosen by config: exactly one `Application.DataConnections` entry is `Active`, and its `DataSourceName` selects a `DataSources` entry, whose `DataSourceType` is `SqlServer` or `PostgreSQL`.
- `UserRolesRepository` is an in-memory lookup, not a database repository.
