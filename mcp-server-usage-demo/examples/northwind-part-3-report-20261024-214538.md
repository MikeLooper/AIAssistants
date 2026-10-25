# Northwind Exercises — Part 3 Report

- **Generated:** 2026-10-24 21:45:38 local
- **Pilot API:** .NET Core with SQL Server (localhost:11001)
- **Data snapshot:** categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 4 · suppliers 29 (shippers include the pre-existing 'Amazon Prime Shipping' row, shipperId 11038, from a prior run)
- **Data validation:** 100.00% (137 of 137 checks matched baseline · 9 of 9 exercises exact)

## Exercise 3.1 — Customers who bought all products bought by 'LAZYK'

**Goal:** Customers who bought every product purchased by customer LAZYK.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Relational division over the 2 distinct products LAZYK bought; LAZYK itself excluded; sorted by name.  
**Result (10 rows):**

| CustomerName |
| --- |
| Antonio Moreno Taquería |
| Bottom-Dollar Markets |
| Ernst Handel |
| HILARION-Abastos |
| Hungry Owl All-Night Grocers |
| Königlich Essen |
| Lehmanns Marktstand |
| Ottilies Käseladen |
| Pericles Comidas clásicas |
| Queen Cozinha |

**Notes:** LAZYK trivially satisfies its own condition and is excluded from the list.

## Exercise 3.2 — Average product price by category

**Goal:** Average product price per category.  
**Data used:** `get_all_categories`, `get_all_products`  
**Logic:** Grouped products by categoryID; average of current unitPrice; only categories that have products; sorted by category name.  
**Result (8 rows):**

| CategoryName | AveragePrice | ProductCount |
| --- | --- | --- |
| Beverages | 37.98 | 12 |
| Condiments | 23.06 | 12 |
| Confections | 25.16 | 13 |
| Dairy Products | 28.73 | 10 |
| Grains/Cereals | 20.25 | 7 |
| Meat/Poultry | 54.01 | 6 |
| Produce | 32.37 | 5 |
| Seafood | 20.68 | 12 |

**Notes:** Categories without products (average undefined) are omitted.

## Exercise 3.3 — Suppliers with more than 3 products

**Goal:** Identifier and name of suppliers providing more than 3 products.  
**Data used:** `get_all_suppliers`, `get_all_products`  
**Logic:** Counted products per supplierID; kept counts > 3; sorted by supplier id.  
**Result (4 rows):**

| SupplierID | CompanyName | ProductCount |
| --- | --- | --- |
| 2 | New Orleans Cajun Delights | 4 |
| 7 | Pavlova, Ltd. | 5 |
| 8 | Specialty Biscuits, Ltd. | 4 |
| 12 | Plutzer Lebensmittelgroßmärkte AG | 5 |

## Exercise 3.4 — Employees who sold more than 70 different products

**Goal:** Identifier, name and total sales of employees who sold more than 70 distinct products.  
**Data used:** `get_all_employees`, `get_all_orders`, `get_all_order_details`  
**Logic:** Per employee: distinct productIDs across their orders and total sales = sum(unitPrice x quantity x (1 - discount)); kept distinct count > 70; ordered by employee id.  
**Result (3 rows):**

| EmployeeID | EmployeeName | TotalSales | DistinctProducts |
| --- | --- | --- | --- |
| 1 | Nancy Davolio | 192107.60 | 72 |
| 3 | Janet Leverling | 202812.84 | 74 |
| 4 | Margaret Peacock | 232890.85 | 75 |

## Exercise 3.5 — Employees selling products of more than 7 suppliers

**Goal:** Employee names who sell products from more than 7 suppliers.  
**Data used:** `get_all_employees`, `get_all_orders`, `get_all_order_details`, `get_all_products`  
**Logic:** Per employee: distinct supplierIDs of products on their orders; kept count > 7; sorted by name.  
**Result (9 rows):**

| EmployeeName | DistinctSuppliers |
| --- | --- |
| Andrew Fuller | 29 |
| Anne Dodsworth | 26 |
| Janet Leverling | 29 |
| Laura Callahan | 29 |
| Margaret Peacock | 29 |
| Michael Suyama | 26 |
| Nancy Davolio | 29 |
| Robert King | 29 |
| Steven Buchanan | 29 |

## Exercise 3.6 — Orders with quantity above 5x the product average

**Goal:** Customer and product where the quantity in one order exceeds 5 times the average quantity of that product per order.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`, `get_all_products`  
**Logic:** Average quantity per product = mean quantity over all order lines of that product (one line per order); kept lines with quantity > 5 x average; sorted by customer, product, order id.  
**Result (3 rows):**

| CustomerName | ProductName | OrderID | QuantityInOrder | AvgQuantityPerOrder |
| --- | --- | --- | --- | --- |
| Ernst Handel | Manjimup Dried Apples | 10776 | 120 | 22.72 |
| Ernst Handel | Wimmers gute Semmelknödel | 11072 | 130 | 24.67 |
| Save-a-lot Markets | Jack's New England Clam Chowder | 10678 | 120 | 20.87 |

**Notes:** Each order has at most one line per product, so "quantity in a single order" is the line quantity.

## Exercise 3.7 — Total revenues in 1997

**Goal:** Total revenue of orders placed in 1997.  
**Data used:** `get_all_orders`, `get_all_order_details`  
**Logic:** Summed unitPrice x quantity x (1 - discount) for lines of orders with orderDate in 1997 (>= 1997-01-01 and < 1998-01-01).  
**Result (1 rows):**

| TotalRevenue1997 |
| --- |
| 617085.20 |

**Notes:** Freight excluded.

## Exercise 3.8 — Total paid by each customer

**Goal:** Total amount each customer has paid so far.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Per customer sum of line revenue across all orders; customers with no orders omitted; sorted by total descending, then customer id.  
**Result (89 rows):**

| CustomerID | CompanyName | TotalPaid |
| --- | --- | --- |
| QUICK | QUICK-Stop | 110277.31 |
| ERNSH | Ernst Handel | 104874.98 |
| SAVEA | Save-a-lot Markets | 104361.95 |
| RATTC | Rattlesnake Canyon Grocery | 51097.80 |
| HUNGO | Hungry Owl All-Night Grocers | 49979.91 |
| HANAR | Hanari Carnes | 32841.37 |
| KOENE | Königlich Essen | 30908.38 |
| FOLKO | Folk och fä HB | 29567.56 |
| MEREP | Mère Paillarde | 28872.19 |
| WHITC | White Clover Markets | 27363.61 |
| FRANK | Frankenversand | 26656.56 |
| QUEEN | Queen Cozinha | 25717.50 |
| BERGS | Berglunds snabbköp | 24927.58 |
| SUPRD | Suprêmes délices | 24088.78 |
| PICCO | Piccolo und mehr | 23128.86 |
| HILAA | HILARION-Abastos | 22768.76 |
| BONAP | Bon app' | 21963.25 |
| BOTTM | Bottom-Dollar Markets | 20801.60 |
| RICSU | Richter Supermarkt | 19343.78 |
| LEHMS | Lehmanns Marktstand | 19261.41 |
| BLONP | Blondesddsl père et fils | 18534.08 |
| GREAL | Great Lakes Food Market | 18507.45 |
| SIMOB | Simons bistro | 16817.10 |
| LINOD | LINO-Delicateses | 16476.57 |
| SEVES | Seven Seas Imports | 16215.33 |
| LILAS | LILA-Supermercado | 16076.60 |
| VAFFE | Vaffeljernet | 15843.93 |
| WARTH | Wartian Herkku | 15648.70 |
| OLDWO | Old World Delicatessen | 15177.46 |
| EASTC | Eastern Connection | 14761.04 |
| AROUT | Around the Horn | 13390.65 |
| OTTIK | Ottilies Käseladen | 12496.20 |
| RICAR | Ricardo Adocicados | 12450.80 |
| CHOPS | Chop-suey Chinese | 12348.88 |
| FOLIG | Folies gourmandes | 11666.90 |
| GODOS | Godos Cocina Típica | 11446.36 |
| SPLIR | Split Rail Beer & Ale | 11441.63 |
| TORTU | Tortuga Restaurante | 10812.15 |
| MAISD | Maison Dewey | 9736.08 |
| WANDK | Die Wandernde Kuh | 9588.43 |
| LAMAI | La maison d'Asie | 9328.20 |
| VICTE | Victuailles en stock | 9182.43 |
| GOURL | Gourmet Lanchonetes | 8414.14 |
| MAGAA | Magazzini Alimentari Riuniti | 7176.22 |
| REGGC | Reggiani Caseifici | 7048.24 |
| ANTON | Antonio Moreno Taquería | 7023.98 |
| TRADH | Tradição Hipermercados | 6850.66 |
| QUEDE | Que Delícia | 6664.81 |
| FURIB | Furia Bacalhau e Frutos do Mar | 6427.42 |
| ISLAT | Island Trading | 6146.30 |
| BSBEV | B's Beverages | 6089.90 |
| WELLI | Wellington Importadora | 6068.20 |
| SANTG | Santé Gourmet | 5735.15 |
| PRINI | Princesa Isabel Vinhos | 5044.94 |
| MORGK | Morgenstern Gesundkost | 5042.20 |
| TOMSP | Toms Spezialitäten | 4778.14 |
| ALFKI | Alfreds Futterkiste | 4273.00 |
| LONEP | Lonesome Pine Restaurant | 4258.60 |
| PERIC | Pericles Comidas clásicas | 4242.20 |
| BOLID | Bólido Comidas preparadas | 4232.85 |
| FAMIA | Familia Arquibaldo | 4107.55 |
| COMMI | Comércio Mineiro | 3810.75 |
| DRACD | Drachenblut Delikatessen | 3763.21 |
| WOLZA | Wolski  Zajazd | 3531.95 |
| OCEAN | Océano Atlántico Ltda. | 3460.20 |
| THEBI | The Big Cheese | 3361.00 |
| BLAUS | Blauer See Delikatessen | 3239.80 |
| FRANR | France restauration | 3172.16 |
| WILMK | Wilman Kala | 3161.35 |
| LETSS | Let's Stop N Shop | 3076.47 |
| HUNGC | Hungry Coyote Import Store | 3063.20 |
| RANCH | Rancho grande | 2844.10 |
| SPECD | Spécialités du monde | 2423.35 |
| LACOR | La corne d'abondance | 1992.05 |
| THECR | The Cracker Box | 1947.24 |
| CACTU | Cactus Comidas para llevar | 1814.80 |
| CONSH | Consolidated Holdings | 1719.10 |
| DUMON | Du monde entier | 1615.90 |
| TRAIH | Trail's Head Gourmet Provisioners | 1571.20 |
| FRANS | Franchi S.p.A. | 1545.70 |
| GROSR | GROSELLA-Restaurante | 1488.70 |
| VINET | Vins et alcools Chevalier | 1480.00 |
| ROMEY | Romero y tomillo | 1467.29 |
| ANATR | Ana Trujillo Emparedados y helados | 1402.95 |
| GALED | Galería del gastrónomo | 836.70 |
| NORTS | North/South | 649.00 |
| LAUGB | Laughing Bacchus Wine Cellars | 522.50 |
| LAZYK | Lazy K Kountry Store | 357.00 |
| CENTC | Centro comercial Moctezuma | 100.80 |

**Notes:** All orders counted regardless of shippedDate (no payment data exists).

## Exercise 3.9 — 10 top selling products

**Goal:** Ten top selling products.  
**Data used:** `get_all_products`, `get_all_order_details`  
**Logic:** Ranked products by total revenue (sum of line revenue) descending; top 10; total quantity shown for reference.  
**Result (10 rows):**

| Rank | ProductID | ProductName | TotalRevenue | TotalQuantity |
| --- | --- | --- | --- | --- |
| 1 | 38 | Côte de Blaye | 141396.74 | 623 |
| 2 | 29 | Thüringer Rostbratwurst | 80368.67 | 746 |
| 3 | 59 | Raclette Courdavault | 71155.70 | 1496 |
| 4 | 62 | Tarte au sucre | 47234.97 | 1083 |
| 5 | 60 | Camembert Pierrot | 46825.48 | 1577 |
| 6 | 56 | Gnocchi di nonna Alice | 42593.06 | 1263 |
| 7 | 51 | Manjimup Dried Apples | 41819.65 | 886 |
| 8 | 17 | Alice Mutton | 32698.38 | 978 |
| 9 | 18 | Carnarvon Tigers | 29171.88 | 539 |
| 10 | 28 | Rössle Sauerkraut | 25696.64 | 640 |

**Notes:** "Top selling" read as highest revenue.

## Data validation — Part 3

**Validation score:** 100.00% (137 of 137 checks matched the baseline)

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
| 3.1 | 10 | 10 | 10 | 100.00% | Match |
| 3.2 | 8 | 8 | 8 | 100.00% | Match |
| 3.3 | 4 | 4 | 4 | 100.00% | Match |
| 3.4 | 3 | 3 | 3 | 100.00% | Match |
| 3.5 | 9 | 9 | 9 | 100.00% | Match |
| 3.6 | 3 | 3 | 3 | 100.00% | Match |
| 3.7 | 1 | 1 | 1 | 100.00% | Match |
| 3.8 | 89 | 89 | 89 | 100.00% | Match |
| 3.9 | 10 | 10 | 10 | 100.00% | Match |

**Differences:**

None
