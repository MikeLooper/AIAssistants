# Northwind Exercises — Part 4 Report

- **Generated:** 2026-10-24 21:45:39 local
- **Pilot API:** .NET Core with SQL Server (localhost:11001)
- **Data snapshot:** categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 4 · suppliers 29 (shippers include the pre-existing 'Amazon Prime Shipping' row, shipperId 11038, from a prior run)
- **Data validation:** 100.00% (276 of 276 checks matched baseline · 5 of 5 exercises exact)

## Exercise 4.1 — Total revenues per customer

**Goal:** Total revenue per customer.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Per customer sum of line revenue; customers with no orders omitted; sorted by customer id.  
**Result (89 rows):**

| CustomerID | CompanyName | TotalRevenue |
| --- | --- | --- |
| ALFKI | Alfreds Futterkiste | 4273.00 |
| ANATR | Ana Trujillo Emparedados y helados | 1402.95 |
| ANTON | Antonio Moreno Taquería | 7023.98 |
| AROUT | Around the Horn | 13390.65 |
| BERGS | Berglunds snabbköp | 24927.58 |
| BLAUS | Blauer See Delikatessen | 3239.80 |
| BLONP | Blondesddsl père et fils | 18534.08 |
| BOLID | Bólido Comidas preparadas | 4232.85 |
| BONAP | Bon app' | 21963.25 |
| BOTTM | Bottom-Dollar Markets | 20801.60 |
| BSBEV | B's Beverages | 6089.90 |
| CACTU | Cactus Comidas para llevar | 1814.80 |
| CENTC | Centro comercial Moctezuma | 100.80 |
| CHOPS | Chop-suey Chinese | 12348.88 |
| COMMI | Comércio Mineiro | 3810.75 |
| CONSH | Consolidated Holdings | 1719.10 |
| DRACD | Drachenblut Delikatessen | 3763.21 |
| DUMON | Du monde entier | 1615.90 |
| EASTC | Eastern Connection | 14761.04 |
| ERNSH | Ernst Handel | 104874.98 |
| FAMIA | Familia Arquibaldo | 4107.55 |
| FOLIG | Folies gourmandes | 11666.90 |
| FOLKO | Folk och fä HB | 29567.56 |
| FRANK | Frankenversand | 26656.56 |
| FRANR | France restauration | 3172.16 |
| FRANS | Franchi S.p.A. | 1545.70 |
| FURIB | Furia Bacalhau e Frutos do Mar | 6427.42 |
| GALED | Galería del gastrónomo | 836.70 |
| GODOS | Godos Cocina Típica | 11446.36 |
| GOURL | Gourmet Lanchonetes | 8414.14 |
| GREAL | Great Lakes Food Market | 18507.45 |
| GROSR | GROSELLA-Restaurante | 1488.70 |
| HANAR | Hanari Carnes | 32841.37 |
| HILAA | HILARION-Abastos | 22768.76 |
| HUNGC | Hungry Coyote Import Store | 3063.20 |
| HUNGO | Hungry Owl All-Night Grocers | 49979.91 |
| ISLAT | Island Trading | 6146.30 |
| KOENE | Königlich Essen | 30908.38 |
| LACOR | La corne d'abondance | 1992.05 |
| LAMAI | La maison d'Asie | 9328.20 |
| LAUGB | Laughing Bacchus Wine Cellars | 522.50 |
| LAZYK | Lazy K Kountry Store | 357.00 |
| LEHMS | Lehmanns Marktstand | 19261.41 |
| LETSS | Let's Stop N Shop | 3076.47 |
| LILAS | LILA-Supermercado | 16076.60 |
| LINOD | LINO-Delicateses | 16476.57 |
| LONEP | Lonesome Pine Restaurant | 4258.60 |
| MAGAA | Magazzini Alimentari Riuniti | 7176.22 |
| MAISD | Maison Dewey | 9736.08 |
| MEREP | Mère Paillarde | 28872.19 |
| MORGK | Morgenstern Gesundkost | 5042.20 |
| NORTS | North/South | 649.00 |
| OCEAN | Océano Atlántico Ltda. | 3460.20 |
| OLDWO | Old World Delicatessen | 15177.46 |
| OTTIK | Ottilies Käseladen | 12496.20 |
| PERIC | Pericles Comidas clásicas | 4242.20 |
| PICCO | Piccolo und mehr | 23128.86 |
| PRINI | Princesa Isabel Vinhos | 5044.94 |
| QUEDE | Que Delícia | 6664.81 |
| QUEEN | Queen Cozinha | 25717.50 |
| QUICK | QUICK-Stop | 110277.31 |
| RANCH | Rancho grande | 2844.10 |
| RATTC | Rattlesnake Canyon Grocery | 51097.80 |
| REGGC | Reggiani Caseifici | 7048.24 |
| RICAR | Ricardo Adocicados | 12450.80 |
| RICSU | Richter Supermarkt | 19343.78 |
| ROMEY | Romero y tomillo | 1467.29 |
| SANTG | Santé Gourmet | 5735.15 |
| SAVEA | Save-a-lot Markets | 104361.95 |
| SEVES | Seven Seas Imports | 16215.33 |
| SIMOB | Simons bistro | 16817.10 |
| SPECD | Spécialités du monde | 2423.35 |
| SPLIR | Split Rail Beer & Ale | 11441.63 |
| SUPRD | Suprêmes délices | 24088.78 |
| THEBI | The Big Cheese | 3361.00 |
| THECR | The Cracker Box | 1947.24 |
| TOMSP | Toms Spezialitäten | 4778.14 |
| TORTU | Tortuga Restaurante | 10812.15 |
| TRADH | Tradição Hipermercados | 6850.66 |
| TRAIH | Trail's Head Gourmet Provisioners | 1571.20 |
| VAFFE | Vaffeljernet | 15843.93 |
| VICTE | Victuailles en stock | 9182.43 |
| VINET | Vins et alcools Chevalier | 1480.00 |
| WANDK | Die Wandernde Kuh | 9588.43 |
| WARTH | Wartian Herkku | 15648.70 |
| WELLI | Wellington Importadora | 6068.20 |
| WHITC | White Clover Markets | 27363.61 |
| WILMK | Wilman Kala | 3161.35 |
| WOLZA | Wolski  Zajazd | 3531.95 |

## Exercise 4.2 — UK customers who paid more than 1000

**Goal:** UK customers whose total payments exceed 1000.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Per-customer totals for customers with country UK, kept totals > 1000; sorted by total descending.  
**Result (6 rows):**

| CustomerID | CompanyName | TotalPaid |
| --- | --- | --- |
| SEVES | Seven Seas Imports | 16215.33 |
| EASTC | Eastern Connection | 14761.04 |
| AROUT | Around the Horn | 13390.65 |
| ISLAT | Island Trading | 6146.30 |
| BSBEV | B's Beverages | 6089.90 |
| CONSH | Consolidated Holdings | 1719.10 |

## Exercise 4.3 — Customer totals overall and in 1997

**Goal:** Per-customer total from all orders and from 1997 orders.  
**Data used:** `get_all_customers`, `get_all_orders`, `get_all_order_details`  
**Logic:** Per customer sum of line revenue overall and for orders dated in 1997 (0.00 when none in 1997); customers with no orders omitted; sorted by customer id.  
**Result (89 rows):**

| CustomerID | CompanyName | Country | Customer's total from all orders | Customer's total from 1997 orders |
| --- | --- | --- | --- | --- |
| ALFKI | Alfreds Futterkiste | Germany | 4273.00 | 2022.50 |
| ANATR | Ana Trujillo Emparedados y helados | Mexico | 1402.95 | 799.75 |
| ANTON | Antonio Moreno Taquería | Mexico | 7023.98 | 5960.78 |
| AROUT | Around the Horn | UK | 13390.65 | 6406.90 |
| BERGS | Berglunds snabbköp | Sweden | 24927.58 | 13849.02 |
| BLAUS | Blauer See Delikatessen | Germany | 3239.80 | 1079.80 |
| BLONP | Blondesddsl père et fils | France | 18534.08 | 7817.88 |
| BOLID | Bólido Comidas preparadas | Spain | 4232.85 | 3026.85 |
| BONAP | Bon app' | France | 21963.25 | 11208.36 |
| BOTTM | Bottom-Dollar Markets | Canada | 20801.60 | 7630.25 |
| BSBEV | B's Beverages | UK | 6089.90 | 3179.50 |
| CACTU | Cactus Comidas para llevar | Argentina | 1814.80 | 238.00 |
| CENTC | Centro comercial Moctezuma | Mexico | 100.80 | 0.00 |
| CHOPS | Chop-suey Chinese | Switzerland | 12348.88 | 6516.40 |
| COMMI | Comércio Mineiro | Brazil | 3810.75 | 1128.00 |
| CONSH | Consolidated Holdings | UK | 1719.10 | 787.60 |
| DRACD | Drachenblut Delikatessen | Germany | 3763.21 | 420.00 |
| DUMON | Du monde entier | France | 1615.90 | 487.00 |
| EASTC | Eastern Connection | UK | 14761.04 | 4514.35 |
| ERNSH | Ernst Handel | Austria | 104874.98 | 48096.26 |
| FAMIA | Familia Arquibaldo | Brazil | 4107.55 | 3127.13 |
| FOLIG | Folies gourmandes | France | 11666.90 | 11666.90 |
| FOLKO | Folk och fä HB | Sweden | 29567.56 | 13314.67 |
| FRANK | Frankenversand | Germany | 26656.56 | 11829.78 |
| FRANR | France restauration | France | 3172.16 | 920.10 |
| FRANS | Franchi S.p.A. | Italy | 1545.70 | 249.70 |
| FURIB | Furia Bacalhau e Frutos do Mar | Portugal | 6427.42 | 5065.32 |
| GALED | Galería del gastrónomo | Spain | 836.70 | 493.20 |
| GODOS | Godos Cocina Típica | Spain | 11446.36 | 3458.35 |
| GOURL | Gourmet Lanchonetes | Brazil | 8414.14 | 8008.79 |
| GREAL | Great Lakes Food Market | USA | 18507.45 | 8565.32 |
| GROSR | GROSELLA-Restaurante | Venezuela | 1488.70 | 387.50 |
| HANAR | Hanari Carnes | Brazil | 32841.37 | 6022.77 |
| HILAA | HILARION-Abastos | Venezuela | 22768.76 | 13482.74 |
| HUNGC | Hungry Coyote Import Store | USA | 3063.20 | 2283.20 |
| HUNGO | Hungry Owl All-Night Grocers | Ireland | 49979.91 | 20454.41 |
| ISLAT | Island Trading | UK | 6146.30 | 2560.50 |
| KOENE | Königlich Essen | Germany | 30908.38 | 9664.21 |
| LACOR | La corne d'abondance | France | 1992.05 | 0.00 |
| LAMAI | La maison d'Asie | France | 9328.20 | 6923.87 |
| LAUGB | Laughing Bacchus Wine Cellars | Canada | 522.50 | 335.50 |
| LAZYK | Lazy K Kountry Store | USA | 357.00 | 357.00 |
| LEHMS | Lehmanns Marktstand | Germany | 19261.41 | 13076.13 |
| LETSS | Let's Stop N Shop | USA | 3076.47 | 1698.40 |
| LILAS | LILA-Supermercado | Venezuela | 16076.60 | 5175.20 |
| LINOD | LINO-Delicateses | Venezuela | 16476.57 | 7359.48 |
| LONEP | Lonesome Pine Restaurant | USA | 4258.60 | 1837.20 |
| MAGAA | Magazzini Alimentari Riuniti | Italy | 7176.22 | 4695.88 |
| MAISD | Maison Dewey | Belgium | 9736.08 | 5297.00 |
| MEREP | Mère Paillarde | Canada | 28872.19 | 23332.31 |
| MORGK | Morgenstern Gesundkost | Germany | 5042.20 | 3596.40 |
| NORTS | North/South | UK | 649.00 | 604.00 |
| OCEAN | Océano Atlántico Ltda. | Argentina | 3460.20 | 429.20 |
| OLDWO | Old World Delicatessen | USA | 15177.46 | 5475.38 |
| OTTIK | Ottilies Käseladen | Germany | 12496.20 | 8254.27 |
| PERIC | Pericles Comidas clásicas | Mexico | 4242.20 | 2065.40 |
| PICCO | Piccolo und mehr | Austria | 23128.86 | 9305.58 |
| PRINI | Princesa Isabel Vinhos | Portugal | 5044.94 | 1409.20 |
| QUEDE | Que Delícia | Brazil | 6664.81 | 3502.41 |
| QUEEN | Queen Cozinha | Brazil | 25717.50 | 10132.77 |
| QUICK | QUICK-Stop | Germany | 110277.31 | 61109.91 |
| RANCH | Rancho grande | Argentina | 2844.10 | 1149.40 |
| RATTC | Rattlesnake Canyon Grocery | USA | 51097.80 | 19383.75 |
| REGGC | Reggiani Caseifici | Italy | 7048.24 | 3000.84 |
| RICAR | Ricardo Adocicados | Brazil | 12450.80 | 4283.78 |
| RICSU | Richter Supermarkt | Switzerland | 19343.78 | 11864.42 |
| ROMEY | Romero y tomillo | Spain | 1467.29 | 0.00 |
| SANTG | Santé Gourmet | Norway | 5735.15 | 700.00 |
| SAVEA | Save-a-lot Markets | USA | 104361.95 | 57713.58 |
| SEVES | Seven Seas Imports | UK | 16215.33 | 9021.25 |
| SIMOB | Simons bistro | Denmark | 16817.10 | 16232.41 |
| SPECD | Spécialités du monde | France | 2423.35 | 52.35 |
| SPLIR | Split Rail Beer & Ale | USA | 11441.63 | 2475.00 |
| SUPRD | Suprêmes délices | Belgium | 24088.78 | 6137.48 |
| THEBI | The Big Cheese | USA | 3361.00 | 2955.40 |
| THECR | The Cracker Box | USA | 1947.24 | 1621.24 |
| TOMSP | Toms Spezialitäten | Germany | 4778.14 | 2004.34 |
| TORTU | Tortuga Restaurante | Mexico | 10812.15 | 5523.35 |
| TRADH | Tradição Hipermercados | Brazil | 6850.66 | 1320.40 |
| TRAIH | Trail's Head Gourmet Provisioners | USA | 1571.20 | 1333.30 |
| VAFFE | Vaffeljernet | Denmark | 15843.93 | 8960.13 |
| VICTE | Victuailles en stock | France | 9182.43 | 5807.12 |
| VINET | Vins et alcools Chevalier | France | 1480.00 | 379.80 |
| WANDK | Die Wandernde Kuh | Germany | 9588.43 | 4262.83 |
| WARTH | Wartian Herkku | Finland | 15648.70 | 12262.94 |
| WELLI | Wellington Importadora | Brazil | 6068.20 | 4415.15 |
| WHITC | White Clover Markets | USA | 27363.61 | 9146.51 |
| WILMK | Wilman Kala | Finland | 3161.35 | 1174.35 |
| WOLZA | Wolski  Zajazd | Poland | 3531.95 | 1207.85 |

## Exercise 4.4 — Orders per customer since 1996-12-31

**Goal:** Number of orders per customer after December 31, 1996, only where count > 1.  
**Data used:** `get_all_customers`, `get_all_orders`  
**Logic:** Counted orders with orderDate > 1996-12-31 per customer; kept count > 1; sorted by count descending then customer id.  
**Result (87 rows):**

| CustomerID | CompanyName | OrderCount |
| --- | --- | --- |
| SAVEA | Save-a-lot Markets | 28 |
| ERNSH | Ernst Handel | 24 |
| QUICK | QUICK-Stop | 22 |
| FOLKO | Folk och fä HB | 16 |
| HILAA | HILARION-Abastos | 16 |
| BERGS | Berglunds snabbköp | 15 |
| BONAP | Bon app' | 14 |
| HUNGO | Hungry Owl All-Night Grocers | 14 |
| BOTTM | Bottom-Dollar Markets | 13 |
| HANAR | Hanari Carnes | 12 |
| KOENE | Königlich Essen | 12 |
| LEHMS | Lehmanns Marktstand | 12 |
| LINOD | LINO-Delicateses | 12 |
| QUEEN | Queen Cozinha | 12 |
| RATTC | Rattlesnake Canyon Grocery | 12 |
| WHITC | White Clover Markets | 12 |
| AROUT | Around the Horn | 11 |
| FRANK | Frankenversand | 11 |
| GREAL | Great Lakes Food Market | 11 |
| LAMAI | La maison d'Asie | 11 |
| REGGC | Reggiani Caseifici | 11 |
| WARTH | Wartian Herkku | 11 |
| MEREP | Mère Paillarde | 10 |
| SUPRD | Suprêmes délices | 10 |
| BSBEV | B's Beverages | 9 |
| GODOS | Godos Cocina Típica | 9 |
| GOURL | Gourmet Lanchonetes | 9 |
| LILAS | LILA-Supermercado | 9 |
| OTTIK | Ottilies Käseladen | 9 |
| RICAR | Ricardo Adocicados | 9 |
| RICSU | Richter Supermarkt | 9 |
| VAFFE | Vaffeljernet | 9 |
| BLONP | Blondesddsl père et fils | 8 |
| MAGAA | Magazzini Alimentari Riuniti | 8 |
| OLDWO | Old World Delicatessen | 8 |
| PICCO | Piccolo und mehr | 8 |
| VICTE | Victuailles en stock | 8 |
| WELLI | Wellington Importadora | 8 |
| BLAUS | Blauer See Delikatessen | 7 |
| EASTC | Eastern Connection | 7 |
| ISLAT | Island Trading | 7 |
| MAISD | Maison Dewey | 7 |
| WILMK | Wilman Kala | 7 |
| ALFKI | Alfreds Futterkiste | 6 |
| ANTON | Antonio Moreno Taquería | 6 |
| CACTU | Cactus Comidas para llevar | 6 |
| CHOPS | Chop-suey Chinese | 6 |
| FRANS | Franchi S.p.A. | 6 |
| FURIB | Furia Bacalhau e Frutos do Mar | 6 |
| LONEP | Lonesome Pine Restaurant | 6 |
| QUEDE | Que Delícia | 6 |
| SEVES | Seven Seas Imports | 6 |
| SIMOB | Simons bistro | 6 |
| TORTU | Tortuga Restaurante | 6 |
| WANDK | Die Wandernde Kuh | 6 |
| WOLZA | Wolski  Zajazd | 6 |
| FAMIA | Familia Arquibaldo | 5 |
| FOLIG | Folies gourmandes | 5 |
| OCEAN | Océano Atlántico Ltda. | 5 |
| RANCH | Rancho grande | 5 |
| SANTG | Santé Gourmet | 5 |
| TOMSP | Toms Spezialitäten | 5 |
| TRADH | Tradição Hipermercados | 5 |
| COMMI | Comércio Mineiro | 4 |
| DRACD | Drachenblut Delikatessen | 4 |
| GALED | Galería del gastrónomo | 4 |
| LACOR | La corne d'abondance | 4 |
| LETSS | Let's Stop N Shop | 4 |
| MORGK | Morgenstern Gesundkost | 4 |
| PERIC | Pericles Comidas clásicas | 4 |
| SPECD | Spécialités du monde | 4 |
| SPLIR | Split Rail Beer & Ale | 4 |
| ANATR | Ana Trujillo Emparedados y helados | 3 |
| CONSH | Consolidated Holdings | 3 |
| DUMON | Du monde entier | 3 |
| FRANR | France restauration | 3 |
| HUNGC | Hungry Coyote Import Store | 3 |
| LAUGB | Laughing Bacchus Wine Cellars | 3 |
| NORTS | North/South | 3 |
| PRINI | Princesa Isabel Vinhos | 3 |
| THEBI | The Big Cheese | 3 |
| THECR | The Cracker Box | 3 |
| TRAIH | Trail's Head Gourmet Provisioners | 3 |
| BOLID | Bólido Comidas preparadas | 2 |
| LAZYK | Lazy K Kountry Store | 2 |
| ROMEY | Romero y tomillo | 2 |
| VINET | Vins et alcools Chevalier | 2 |

## Exercise 4.5 — Products with fewer than 200 units ordered

**Goal:** Total quantity ordered per product, only where quantity < 200.  
**Data used:** `get_all_products`, `get_all_order_details`  
**Logic:** Summed quantity per productID from Order Details; kept totals < 200; sorted by quantity ascending then product id.  
**Result (5 rows):**

| ProductID | ProductName | TotalQuantity |
| --- | --- | --- |
| 9 | Mishi Kobe Niku | 95 |
| 15 | Genen Shouyu | 122 |
| 37 | Gravad lax | 125 |
| 48 | Chocolade | 138 |
| 67 | Laughing Lumberjack Lager | 184 |

## Data validation — Part 4

**Validation score:** 100.00% (276 of 276 checks matched the baseline)

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
| 4.1 | 89 | 89 | 89 | 100.00% | Match |
| 4.2 | 6 | 6 | 6 | 100.00% | Match |
| 4.3 | 89 | 89 | 89 | 100.00% | Match |
| 4.4 | 87 | 87 | 87 | 100.00% | Match |
| 4.5 | 5 | 5 | 5 | 100.00% | Match |

**Differences:**

None
