---
name: northwind-data-access
description: How to read and write Northwind data through the pilot MCP server — tool inventory, DTO field names, join keys, revenue math, and client-side aggregation patterns. Use when running Northwind reporting exercises or any task that queries a Pilot API deployment via the pilot MCP server.
---

# Northwind Data Access via the `pilot` MCP Server

Northwind data is not queried with SQL. It is exposed through the `pilot` MCP server,
which wraps one of six equivalent Pilot API deployments (same OpenAPI contract, same
seed data, different language/database flavors). The host prefixes tool names with the
server name (e.g. `mcp_pilot_get_all_categories`).

## Discovery / system tools

| Tool | Purpose |
| --- | --- |
| `list_apis` | Lists all six deployments with live availability, version, deploy date; flags the current selection. |
| `select_api` | Sets which deployment subsequent calls use by default. |
| `list_endpoints` | Summarizes the logical endpoints of the shared API contract (same for all deployments). |

Every data tool also accepts an optional `apiName` argument (a Description string from
`list_apis`, e.g. `"Python with PostgreSQL"`) to target a specific deployment for that
one call. Prefer picking one deployment at the start of a run and sticking to it.

## Data tools

Each resource has five tools: `get_all_*`, `get_*`, `add_*`, `update_*`, `delete_*`.

| Resource | Tool prefix | Single-record key |
| --- | --- | --- |
| Categories | `..._category` / `..._categories` | `categoryId` (int) |
| Customers | `..._customer` / `..._customers` | `customerId` (5-char string) |
| Employees | `..._employee` / `..._employees` | `employeeId` (int) |
| Orders | `..._order` / `..._orders` | `orderId` (int) |
| Order Details | `..._order_detail` / `..._order_details` | composite: `productId` + `orderId` |
| Products | `..._product` / `..._products` | `productId` (int) |
| Shippers | `..._shipper` / `..._shippers` | `shipperId` (int) |
| Suppliers | `..._supplier` / `..._suppliers` | `supplierId` (int) |

## Record fields (JSON names; `*` = required)

| Resource | Fields |
| --- | --- |
| Category | `categoryID`*, `categoryName`*, `description`, `picture` |
| Customer | `customerID`* (5-char code), `companyName`*, `contactName`, `contactTitle`, `address`, `city`, `region`, `postalCode`, `country`, `phone`, `fax` |
| Employee | `employeeID`*, `firstName`*, `lastName`*, `title`, `titleOfCourtesy`, `birthDate`, `hireDate`, `address`, `city`, `region`, `postalCode`, `country`, `homePhone`, `extension`, `photoPath`, `notes`, `reportsTo` |
| Order | `orderID`*, `customerID`, `employeeID`, `orderDate`, `requiredDate`, `shippedDate`, `shipVia`, `freight`, `shipName`, `shipAddress`, `shipCity`, `shipRegion`, `shipPostalCode`, `shipCountry` |
| Order Detail | `orderID`* + `productID`* (composite), `unitPrice`*, `quantity`*, `discount`* (fraction, e.g. 0.15 = 15%) |
| Product | `productID`*, `productName`*, `supplierID`, `categoryID`, `quantityPerUnit`, `unitPrice`, `unitsInStock`, `unitsOnOrder`, `reorderLevel`, `discontinued` (bool) |
| Shipper | `shipperID`*, `companyName`*, `phone` |
| Supplier | `supplierID`*, `companyName`*, `contactName`, `contactTitle`, `address`, `city`, `region`, `postalCode`, `country`, `phone`, `fax`, `homePage` |

## Join keys

- `orders.customerID` → `customers.customerID`
- `orders.employeeID` → `employees.employeeID`
- `orders.shipVia` → `shippers.shipperID`
- `orderDetails.orderID` → `orders.orderID` · `orderDetails.productID` → `products.productID`
- `products.categoryID` → `categories.categoryID` · `products.supplierID` → `suppliers.supplierID`
- `employees.reportsTo` → `employees.employeeID` (self-join; null = no manager)

## Semantics that matter

- **Order-line revenue** = `unitPrice × quantity × (1 − discount)`, using the **order
  line's** `unitPrice` (price at time of sale) — never the product's current `unitPrice`.
- Dates are ISO 8601 and nullable. "In 1997" means `orderDate >= 1997-01-01` and
  `< 1998-01-01`. "Since/after December 31, 1996" means `orderDate > 1996-12-31`.
- String matches on names/titles/addresses (e.g. "Owner", "rue") are
  case-insensitive substring matches unless the exercise says otherwise.
- Nulls are common (`shipRegion`, `reportsTo`, ...). Filter null-safely; render as
  `(null)` in reports.

## Working pattern

1. Call `list_apis` once; `select_api` to the requested deployment, else the first
   available one. Record which deployment produced the data.
2. Fetch each needed table **once per run** with `get_all_*` and reuse that snapshot
   for every exercise. Classic Northwind is small (orders ≈ 830 rows, order details
   ≈ 2,155 rows), so full-table pulls are cheap and keep a run internally consistent.
3. The API has **no filtering, search, or aggregation endpoints** — all joins,
   grouping, and math happen client-side. For error-prone computations (relational
   division, multi-way joins) a throwaway script is allowed: put it in the system
   temp directory (`$env:TEMP`), run it, and delete it. Never leave scratch files in
   the workspace.
4. All six deployments serve equivalent data; results should match across them.

## Failure handling

- Treat every non-success API status code, API error message, MCP tool error,
  timeout, or malformed/unusable response as a hard stop for the run.
- Do not retry the call, continue with another exercise, fetch more data, or
  perform a write after a failure. This prevents additional resource usage while
  the deployment or API problem is unresolved.
- Before stopping, capture and report: timestamp; selected deployment; MCP tool;
  logical endpoint or operation; safe request parameters; HTTP status code when
  available; status and description; complete API/MCP error message or response
  body; request/correlation id and response headers when available; and the
  exercise and workflow step in progress. Redact secrets and credentials only.
- Also state the completed work, unattempted work, files already written, and
  credits or usage recorded before the failure. Provide a repair hint only when
  supported by the observed response.

## Write operations

- Only perform writes the task explicitly requests. `add_*` returns the new record's
  id; `update_*` takes the full DTO **including its existing id** (keep untouched
  fields at their current values).
- Verify every write immediately: re-fetch with `get_*`/`get_all_*` and quote the
  after-state.
- The database is shared, mutable state. Before inserting, check for an existing
  matching row to avoid duplicates on re-runs, and note what you found.
