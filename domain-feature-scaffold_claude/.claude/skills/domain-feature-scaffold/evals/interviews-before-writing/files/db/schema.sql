CREATE TABLE Customers (
    CustomerID   INT IDENTITY PRIMARY KEY,
    CompanyName  NVARCHAR(40) NOT NULL,
    ContactName  NVARCHAR(30) NULL,
    Country      NVARCHAR(15) NULL
);

CREATE TABLE Suppliers (
    SupplierID   INT IDENTITY PRIMARY KEY,
    CompanyName  NVARCHAR(40) NOT NULL,
    ContactName  NVARCHAR(30) NULL,
    Phone        NVARCHAR(24) NULL,
    Country      NVARCHAR(15) NULL
);
