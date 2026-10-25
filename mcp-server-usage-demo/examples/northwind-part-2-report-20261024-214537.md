# Northwind Exercises — Part 2 Report

- **Generated:** 2026-10-24 21:45:37 local
- **Pilot API:** .NET Core with SQL Server (localhost:11001)
- **Data snapshot:** categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 4 · suppliers 29 (shippers include the pre-existing 'Amazon Prime Shipping' row, shipperId 11038, from a prior run)
- **Data validation:** 98.08% (51 of 52 checks matched baseline · 8 of 9 exercises exact)

## Exercise 2.1 — Rename shipper 'Amazon' to 'Amazon Prime Shipping'

**Goal:** Change the company name from 'Amazon' to 'Amazon Prime Shipping'.  
**Data used:** `get_all_shippers`  
**Action taken:** No write performed. No shipper named 'Amazon' exists; shipperId 11038 is already named 'Amazon Prime Shipping' (left by a previous run), so the rename was already in effect. `update_shipper` was not called.  
**Verification:** Current `get_all_shippers` (fetched this run, no write): [{"shipperId": 1, "companyName": "Speedy Express", "phone": "(503) 555-9831"}, {"shipperId": 2, "companyName": "United Package", "phone": "(503) 555-3199"}, {"shipperId": 3, "companyName": "Federal Shipping", "phone": "(503) 555-9931"}, {"shipperId": 11038, "companyName": "Amazon Prime Shipping"}]  
**Notes:** Skipped because the target state already existed.

## Exercise 2.2 — Employee display names

**Goal:** Combine last and first name as 'LastName, FirstName'.  
**Data used:** `get_all_employees`  
**Logic:** Built DisplayName as lastName + ", " + firstName; ordered by employee id.  
**Result (9 rows):**

| DisplayName |
| --- |
| Davolio, Nancy |
| Fuller, Andrew |
| Leverling, Janet |
| Peacock, Margaret |
| Buchanan, Steven |
| Suyama, Michael |
| King, Robert |
| Callahan, Laura |
| Dodsworth, Anne |

## Exercise 2.3 — Employees with orders delivered to Belgium

**Goal:** Name, address, city and region of employees who placed orders shipped to Belgium.  
**Data used:** `get_all_employees`, `get_all_orders`  
**Logic:** Orders with shipCountry Belgium, distinct employeeIDs joined to employees; ordered by employee id.  
**Result (8 rows):**

| Name | Address | City | Region |
| --- | --- | --- | --- |
| Nancy Davolio | 507 - 20th Ave. E.Apt. 2A | Seattle | WA |
| Andrew Fuller | 908 W. Capital Way | Tacoma | WA |
| Janet Leverling | 722 Moss Bay Blvd. | Kirkland | WA |
| Margaret Peacock | 4110 Old Redmond Rd. | Redmond | WA |
| Steven Buchanan | 14 Garrett Hill | London | (null) |
| Michael Suyama | Coventry House Miner Rd. | London | (null) |
| Robert King | Edgeham Hollow Winchester Way | London | (null) |
| Anne Dodsworth | 7 Houndstooth Rd. | London | (null) |

## Exercise 2.4 — Speedy Express orders to Brussels customers

**Goal:** Employee and customer name for orders shipped by 'Speedy Express' to customers in Brussels.  
**Data used:** `get_all_shippers`, `get_all_orders`, `get_all_employees`, `get_all_customers`  
**Logic:** Joined orders to shippers, customers, and employees; kept orders shipped by Speedy Express to the Brussels customer (stored as Bruxelles); selected the order, employee, and customer names and ordered by order id.
**Result (2 rows):**

| OrderID | EmployeeName | CustomerName |
| --- | --- | --- |
| 10760 | Margaret Peacock | Maison Dewey |
| 11004 | Janet Leverling | Maison Dewey |

**Notes:** No customer has the city spelled 'Brussels'; the data uses the French spelling 'Bruxelles' (Maison Dewey, Belgium), so 'Brussels' was read as 'Bruxelles' too (an exact 'Brussels' match returns 0 rows). Line breaks inside text values are rendered as a single space.

## Exercise 2.5 — Employees and their managers

**Goal:** Employee name/title with manager name/title (null when none).  
**Data used:** `get_all_employees`  
**Logic:** Self-join employees.reportsTo to employeeID (left join); ordered by employee id.  
**Result (9 rows):**

| EmployeeName | EmployeeTitle | ManagerName | ManagerTitle |
| --- | --- | --- | --- |
| Nancy Davolio | Sales Representative | Andrew Fuller | Vice President, Sales |
| Andrew Fuller | Vice President, Sales | (null) | (null) |
| Janet Leverling | Sales Representative | Andrew Fuller | Vice President, Sales |
| Margaret Peacock | Sales Representative | Andrew Fuller | Vice President, Sales |
| Steven Buchanan | Sales Manager | Andrew Fuller | Vice President, Sales |
| Michael Suyama | Sales Representative | Steven Buchanan | Sales Manager |
| Robert King | Sales Representative | Steven Buchanan | Sales Manager |
| Laura Callahan | Inside Sales Coordinator | Andrew Fuller | Vice President, Sales |
| Anne Dodsworth | Sales Representative | Steven Buchanan | Sales Manager |

## Exercise 2.6 — London customers buying from Pavlova, Ltd. / Karkki Oy

**Goal:** Customer, product and supplier names for London customers and the two suppliers.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`, `get_all_products`, `get_all_suppliers`  
**Logic:** Joined customers (city London) -> orders -> order details -> products -> suppliers; kept supplier names Pavlova, Ltd. or Karkki Oy; distinct rows sorted by customer, supplier, product.  
**Result (9 rows):**

| CustomerName | ProductName | SupplierName |
| --- | --- | --- |
| Around the Horn | Valkoinen suklaa | Karkki Oy |
| Around the Horn | Outback Lager | Pavlova, Ltd. |
| B's Beverages | Maxilaku | Karkki Oy |
| B's Beverages | Outback Lager | Pavlova, Ltd. |
| Eastern Connection | Maxilaku | Karkki Oy |
| North/South | Outback Lager | Pavlova, Ltd. |
| Seven Seas Imports | Maxilaku | Karkki Oy |
| Seven Seas Imports | Alice Mutton | Pavlova, Ltd. |
| Seven Seas Imports | Pavlova | Pavlova, Ltd. |

## Exercise 2.7 — Employees older than every London employee

**Goal:** Employees strictly older than any employee who lives in London.  
**Data used:** `get_all_employees`  
**Logic:** Kept employees whose birthDate is earlier than the earliest London employee birthDate (1955-03-04); sorted by birth date.  
**Result (3 rows):**

| EmployeeName | BirthDate |
| --- | --- |
| Margaret Peacock | 1937-09-19 |
| Nancy Davolio | 1948-12-08 |
| Andrew Fuller | 1952-02-19 |

**Notes:** "Strictly older than any London employee" read as older than all London employees (born before the oldest of them); London employees are therefore excluded.

## Exercise 2.8 — Customers who purchased no product

**Goal:** Customer names with no purchased product.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Customers with no order-detail line reachable through their orders; sorted by name.  
**Result (2 rows):**

| CustomerName |
| --- |
| FISSA Fabrica Inter. Salchichas S.A. |
| Paris spécialités |

**Notes:** "Customer name" read as companyName. A customer with orders but no order lines would also qualify.

## Exercise 2.9 — Customers who bought all products under 5

**Goal:** Customers who bought every product with price < 5.  
**Data used:** `get_all_products`, `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Relational division: customers whose purchased-product set contains all 2 products with current unitPrice < 5 (product ids [24, 33]); sorted by name.  
**Result (9 rows):**

| CustomerName |
| --- |
| Bottom-Dollar Markets |
| Ernst Handel |
| Familia Arquibaldo |
| La maison d'Asie |
| Queen Cozinha |
| Reggiani Caseifici |
| Save-a-lot Markets |
| Suprêmes délices |
| Tortuga Restaurante |

**Notes:** Product price taken from the product catalog (current unitPrice), as the exercise refers to the product price.

## Data validation — Part 2

**Validation score:** 98.08% (51 of 52 checks matched the baseline)

**Snapshot check:**

| Table | Baseline | Current | Result |
| --- | --- | --- | --- |
| categories | 11 | 11 | Match |
| customers | 91 | 91 | Match |
| employees | 9 | 9 | Match |
| orders | 831 | 831 | Match |
| order details | 2155 | 2155 | Match |
| products | 77 | 77 | Match |
| shippers | 4 | 4 | Match |
| suppliers | 29 | 29 | Match |

**Exercise check:**

| Exercise | Baseline rows | Current rows | Matched | Score | Status |
| --- | --- | --- | --- | --- | --- |
| 2.1 | 1 | 0 | 0 | 0.00% | Mismatch |
| 2.2 | 9 | 9 | 9 | 100.00% | Match |
| 2.3 | 8 | 8 | 8 | 100.00% | Match |
| 2.4 | 2 | 2 | 2 | 100.00% | Match |
| 2.5 | 9 | 9 | 9 | 100.00% | Match |
| 2.6 | 9 | 9 | 9 | 100.00% | Match |
| 2.7 | 3 | 3 | 3 | 100.00% | Match |
| 2.8 | 2 | 2 | 2 | 100.00% | Match |
| 2.9 | 9 | 9 | 9 | 100.00% | Match |

**Differences:**

- 2.1: Write exercise skipped this run (no payload sent); the baseline reflects an executed write. Scored 0/1 per validation rules.
