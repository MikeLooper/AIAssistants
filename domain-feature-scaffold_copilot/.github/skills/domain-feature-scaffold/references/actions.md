# Action Mapping

How each action chosen in interview question B becomes a method in every layer. `<Domain>` is the PascalCase domain name; `<domain>` is its camelCase form; `<route>` is the plural, lowercase, kebab-case resource name (for `PurchaseOrder`: `purchase-orders`).

Method names below use the C# `Async` suffix. Drop the suffix in Java; use snake_case in Python (`get_by_id`, `mark_delivered`). If the codebase already names these operations differently (for example `FindById`, `Insert`, `Remove`), follow the codebase.

## CRUD actions

| Action | Repository (works with `<Domain>Entity`) | Service (works with `<Domain>Dto`) | Controller | Success / failure |
|---|---|---|---|---|
| Create | `AddAsync(entity)` returns the saved entity | `CreateAsync(dto)` returns `<Domain>Dto` | `POST /<route>` | `201 Created` + `Location` header; `400` on invalid input |
| Read (one) | `GetByIdAsync(id)` returns entity or null | `GetByIdAsync(id)` returns DTO or null | `GET /<route>/{id}` | `200 OK`; `404 Not Found` |
| Read (list) | `GetAllAsync()` | `GetAllAsync()` | `GET /<route>` | `200 OK` (empty list is still `200`) |
| Update | `UpdateAsync(entity)` returns `true` if a row changed | `UpdateAsync(id, dto)` returns `bool` | `PUT /<route>/{id}` | `204 No Content`; `404 Not Found` |
| Delete | `DeleteAsync(id)` returns `true` if a row was removed | `DeleteAsync(id)` returns `bool` | `DELETE /<route>/{id}` | `204 No Content`; `404 Not Found` |

"Read" means both the single-item and list methods unless the user asked for only one of them. When the codebase already paginates list endpoints, follow its paging pattern for `GetAll` too.

## Custom actions

A custom action is any name the user gave that is not Create, Read, Update or Delete (for example `Archive`, `MarkDelivered`, `RecalculateTotals`).

- Convert the name to PascalCase for methods (`mark delivered` -> `MarkDeliveredAsync`) and kebab-case for the route segment (`mark-delivered`).
- Repository: `<Action>Async(...)` with the data-access statement it most plausibly needs, or a clearly marked `TODO` body if the intent is not obvious from the name. Never invent business rules silently.
- Service: `<Action>Async(...)` that calls the repository method and maps the result.
- Controller: `POST /<route>/{id}/<action>` when the action targets one item, otherwise `POST /<route>/<action>`. Return `204 No Content` (or `200 OK` with a DTO when the action returns data) and `404 Not Found` when the target item does not exist.
- Parameters: take the item `id` when the name implies one item; otherwise take a `<Domain>Dto`. Say in the final summary which signature you chose so the user can adjust it.

## Placement in an existing controller

When question D names an existing controller whose own resource is different from `<Domain>` (for example adding `CustomerNote` actions to `CustomersController`), nest the routes under that controller's route instead of creating top-level ones: `GET /customers/{customerId}/notes/{id}`. Keep the controller's existing route prefix, attributes and response style.
