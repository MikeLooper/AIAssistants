# Part 1 baseline
Snapshot: categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 3 · suppliers 29

## 1.1
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

## 1.2
| ContactName | CustomerID | CompanyName |
| --- | --- | --- |
| Thomas Hardy | AROUT | Around the Horn |
| Victoria Ashworth | BSBEV | B's Beverages |
| Elizabeth Brown | CONSH | Consolidated Holdings |
| Ann Devon | EASTC | Eastern Connection |
| Simon Crowther | NORTS | North/South |
| Hari Kumar | SEVES | Seven Seas Imports |

## 1.3
| CompanyName | ContactName |
| --- | --- |
| Ottilies Käseladen | Henriette Pfalzheim |
| Ana Trujillo Emparedados y helados | Ana Trujillo |
| Antonio Moreno Taquería | Antonio Moreno |
| Tortuga Restaurante | Miguel Angel Paolino |
| Folk och fä HB | Maria Larsson |

## 1.4
| DiscontinuedProducts |
| --- |
| 8 |

## 1.5
| CompanyName | City | Country | PostalCode |
| --- | --- | --- | --- |
| Aux joyeux ecclésiastiques | Paris | France | 75004 |
| Escargots Nouveaux | Montceau | France | 71300 |
| Forêts d'érables | Ste-Hyacinthe | Canada | J2S 7S8 |
| Gai pâturage | Annecy | France | 74000 |
| Ma Maison | Montréal | Canada | H1J 1C3 |

## 1.6
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

## 1.7
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

## 1.8
| CustomerName | CustomerID |
| --- | --- |
| FISSA Fabrica Inter. Salchichas S.A. | FISSA |
| Paris spécialités | PARIS |

## 1.9
**Action taken:** `add_shipper` with payload `{"companyName": "Amazon"}`; the API returned `{"id":11038}`.
**Verification:** `get_shipper(11038)` returned `{"shipperId":11038,"companyName":"Amazon"}`. `get_all_shippers` after the write returned 4 rows: `{"shipperId":1,"companyName":"Speedy Express","phone":"(503) 555-9831"}`, `{"shipperId":2,"companyName":"United Package","phone":"(503) 555-3199"}`, `{"shipperId":3,"companyName":"Federal Shipping","phone":"(503) 555-9931"}`, `{"shipperId":11038,"companyName":"Amazon"}`.
