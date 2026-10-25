# Part 2 baseline
Snapshot: categories 11 · customers 91 · employees 9 · orders 831 · order details 2155 · products 77 · shippers 4 · suppliers 29

## 2.1
**Action taken:** `update_shipper` with payload `{"shipperId": 11038, "companyName": "Amazon Prime Shipping"}` (phone was already null, so no other field changed).
**Verification:** `get_shipper(11038)` returned `{"shipperId":11038,"companyName":"Amazon Prime Shipping"}`. `get_all_shippers` after the write returned 4 rows: `{"shipperId":1,"companyName":"Speedy Express","phone":"(503) 555-9831"}`, `{"shipperId":2,"companyName":"United Package","phone":"(503) 555-3199"}`, `{"shipperId":3,"companyName":"Federal Shipping","phone":"(503) 555-9931"}`, `{"shipperId":11038,"companyName":"Amazon Prime Shipping"}`.

## 2.2
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

## 2.3
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

## 2.4
| OrderID | EmployeeName | CustomerName |
| --- | --- | --- |
| 10760 | Margaret Peacock | Maison Dewey |
| 11004 | Janet Leverling | Maison Dewey |

## 2.5
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

## 2.6
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

## 2.7
| EmployeeName | BirthDate |
| --- | --- |
| Margaret Peacock | 1937-09-19 |
| Nancy Davolio | 1948-12-08 |
| Andrew Fuller | 1952-02-19 |

## 2.8
| CustomerName |
| --- |
| FISSA Fabrica Inter. Salchichas S.A. |
| Paris spécialités |

## 2.9
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
