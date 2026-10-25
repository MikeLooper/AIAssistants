# Northwind Exercises — Part 1 Report

- **Generated:** 2026-10-24 21:45:36 local
- **Pilot API:** .NET Core with SQL Server (localhost:11001)
- **Data snapshot:** categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 4 · suppliers 29 (shippers include the pre-existing 'Amazon Prime Shipping' row, shipperId 11038, from a prior run)
- **Data validation:** 99.17% (119 of 120 checks matched baseline · 8 of 9 exercises exact)

## Exercise 1.1 — Category names and descriptions

**Goal:** List every category name with its description.  
**Data used:** `get_all_categories`  
**Logic:** Projected categoryName and description for all categories; sorted by category name.  
**Result (11 rows):**

| CategoryName | Description |
| --- | --- |
| Beverages | Soft drinks, coffees, teas, beers, and ales |
| Condiments | Sweet and savory sauces, relishes, spreads, and seasonings |
| Confections | Desserts, candies, and sweet breads |
| Dairy Products | Cheeses |
| Grains/Cereals | Breads, crackers, pasta, and cereal |
| Meat/Poultry | Prepared meats |
| Produce | Dried fruit and bean curd |
| Seafood | Seaweed and fish |
| Test Cat | Test Category |
| Test Cat | Test Category |
| Test Cat | Test Category |

## Exercise 1.2 — Customers in London

**Goal:** Contact name, customer id and company name of customers in London.  
**Data used:** `get_all_customers`  
**Logic:** Filtered customers where city equals London (case-insensitive); sorted by customer id.  
**Result (6 rows):**

| ContactName | CustomerID | CompanyName |
| --- | --- | --- |
| Thomas Hardy | AROUT | Around the Horn |
| Victoria Ashworth | BSBEV | B's Beverages |
| Elizabeth Brown | CONSH | Consolidated Holdings |
| Ann Devon | EASTC | Eastern Connection |
| Simon Crowther | NORTS | North/South |
| Hari Kumar | SEVES | Seven Seas Imports |

## Exercise 1.3 — Owners in Mexico, Sweden and Germany

**Goal:** Company and contact names of Owners from Mexico, Sweden and Germany.  
**Data used:** `get_all_customers`  
**Logic:** Filtered customers whose contactTitle contains "owner" (case-insensitive) and country is Mexico, Sweden or Germany; sorted by country then company name.  
**Result (5 rows):**

| CompanyName | ContactName |
| --- | --- |
| Ottilies Käseladen | Henriette Pfalzheim |
| Ana Trujillo Emparedados y helados | Ana Trujillo |
| Antonio Moreno Taquería | Antonio Moreno |
| Tortuga Restaurante | Miguel Angel Paolino |
| Folk och fä HB | Maria Larsson |

**Notes:** "Owners" read as contactTitle containing "Owner".

## Exercise 1.4 — Discontinued products

**Goal:** Count discontinued products.  
**Data used:** `get_all_products`  
**Logic:** Counted products where discontinued is true.  
**Result (1 rows):**

| DiscontinuedProducts |
| --- |
| 8 |

## Exercise 1.5 — Suppliers with 'rue' in address

**Goal:** Company, city, country and postal code of suppliers whose address contains 'rue'.  
**Data used:** `get_all_suppliers`  
**Logic:** Case-insensitive substring match of 'rue' on address; ordered alphabetically by company name.  
**Result (5 rows):**

| CompanyName | City | Country | PostalCode |
| --- | --- | --- | --- |
| Aux joyeux ecclésiastiques | Paris | France | 75004 |
| Escargots Nouveaux | Montceau | France | 71300 |
| Forêts d'érables | Ste-Hyacinthe | Canada | J2S 7S8 |
| Gai pâturage | Annecy | France | 74000 |
| Ma Maison | Montréal | Canada | H1J 1C3 |

**Notes:** Substring match, so it is not limited to the whole word "rue".

## Exercise 1.6 — Total quantity ordered per product

**Goal:** Product id and total quantity ordered for each product in Order Details.  
**Data used:** `get_all_order_details`  
**Logic:** Summed quantity grouped by productID; sorted by product id.  
**Result (77 rows):**

| ProductID | TotalQuantity |
| --- | --- |
| 1 | 828 |
| 2 | 1057 |
| 3 | 328 |
| 4 | 453 |
| 5 | 298 |
| 6 | 301 |
| 7 | 763 |
| 8 | 372 |
| 9 | 95 |
| 10 | 742 |
| 11 | 706 |
| 12 | 344 |
| 13 | 891 |
| 14 | 404 |
| 15 | 122 |
| 16 | 1158 |
| 17 | 978 |
| 18 | 539 |
| 19 | 723 |
| 20 | 313 |
| 21 | 1016 |
| 22 | 348 |
| 23 | 580 |
| 24 | 1125 |
| 25 | 318 |
| 26 | 753 |
| 27 | 365 |
| 28 | 640 |
| 29 | 746 |
| 30 | 612 |
| 31 | 1397 |
| 32 | 297 |
| 33 | 755 |
| 34 | 506 |
| 35 | 883 |
| 36 | 805 |
| 37 | 125 |
| 38 | 623 |
| 39 | 793 |
| 40 | 1103 |
| 41 | 981 |
| 42 | 697 |
| 43 | 580 |
| 44 | 601 |
| 45 | 508 |
| 46 | 548 |
| 47 | 485 |
| 48 | 138 |
| 49 | 520 |
| 50 | 235 |
| 51 | 886 |
| 52 | 500 |
| 53 | 722 |
| 54 | 755 |
| 55 | 903 |
| 56 | 1263 |
| 57 | 434 |
| 58 | 534 |
| 59 | 1496 |
| 60 | 1577 |
| 61 | 603 |
| 62 | 1083 |
| 63 | 445 |
| 64 | 740 |
| 65 | 745 |
| 66 | 239 |
| 67 | 184 |
| 68 | 799 |
| 69 | 714 |
| 70 | 817 |
| 71 | 1057 |
| 72 | 806 |
| 73 | 293 |
| 74 | 297 |
| 75 | 1155 |
| 76 | 981 |
| 77 | 791 |

## Exercise 1.7 — Condiment products

**Goal:** Product names that are condiments.  
**Data used:** `get_all_categories`, `get_all_products`  
**Logic:** Joined products to categories on categoryID and kept category name "Condiments"; sorted by product name.  
**Result (12 rows):**

| ProductName |
| --- |
| Aniseed Syrup |
| Chef Anton's Cajun Seasoning |
| Chef Anton's Gumbo Mix |
| Genen Shouyu |
| Grandma's Boysenberry Spread |
| Gula Malacca |
| Louisiana Fiery Hot Pepper Sauce |
| Louisiana Hot Spiced Okra |
| Northwoods Cranberry Sauce |
| Original Frankfurter grüne Soße |
| Sirop d'érable |
| Vegie-spread |

## Exercise 1.8 — Customers with no orders

**Goal:** Customer names with no rows in Orders.  
**Data used:** `get_all_customers`, `get_all_orders`  
**Logic:** Customers whose customerID does not appear in any order; sorted by name.  
**Result (2 rows):**

| CustomerName | CustomerID |
| --- | --- |
| FISSA Fabrica Inter. Salchichas S.A. | FISSA |
| Paris spécialités | PARIS |

**Notes:** "Customer name" read as companyName.

## Exercise 1.9 — Add shipper 'Amazon'

**Goal:** Add a shipper named 'Amazon'.  
**Data used:** `get_all_shippers`  
**Action taken:** No write performed. `get_all_shippers` already returned a shipper matching Amazon: [{"shipperId": 11038, "companyName": "Amazon Prime Shipping"}]. No row named exactly 'Amazon' exists, but this row is the result of a previous run (Exercise 1.9 add followed by Exercise 2.1 rename). Adding again would create a duplicate Amazon shipper, so `add_shipper` was not called.  
**Verification:** Current `get_all_shippers` (fetched this run, no write): [{"shipperId": 1, "companyName": "Speedy Express", "phone": "(503) 555-9831"}, {"shipperId": 2, "companyName": "United Package", "phone": "(503) 555-3199"}, {"shipperId": 3, "companyName": "Federal Shipping", "phone": "(503) 555-9931"}, {"shipperId": 11038, "companyName": "Amazon Prime Shipping"}]  
**Notes:** Skipped because the Amazon shipper already existed (renamed to "Amazon Prime Shipping" by an earlier run).

## Data validation — Part 1

**Validation score:** 99.17% (119 of 120 checks matched the baseline)

**Snapshot check:**

| Table | Baseline | Current | Result |
| --- | --- | --- | --- |
| categories | 11 | 11 | Match |
| customers | 91 | 91 | Match |
| employees | 9 | 9 | Match |
| orders | 831 | 831 | Match |
| order details | 2155 | 2155 | Match |
| products | 77 | 77 | Match |
| shippers | 3 | 4 | Mismatch |
| suppliers | 29 | 29 | Match |

**Exercise check:**

| Exercise | Baseline rows | Current rows | Matched | Score | Status |
| --- | --- | --- | --- | --- | --- |
| 1.1 | 11 | 11 | 11 | 100.00% | Match |
| 1.2 | 6 | 6 | 6 | 100.00% | Match |
| 1.3 | 5 | 5 | 5 | 100.00% | Match |
| 1.4 | 1 | 1 | 1 | 100.00% | Match |
| 1.5 | 5 | 5 | 5 | 100.00% | Match |
| 1.6 | 77 | 77 | 77 | 100.00% | Match |
| 1.7 | 12 | 12 | 12 | 100.00% | Match |
| 1.8 | 2 | 2 | 2 | 100.00% | Match |
| 1.9 | 1 | 0 | 0 | 0.00% | Mismatch |

**Differences:**

- 1.9: Write exercise skipped this run (no payload sent); the baseline reflects an executed write. Scored 0/1 per validation rules.
