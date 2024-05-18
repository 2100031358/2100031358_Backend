-- List all customers
SELECT * FROM Customers;

-- Find all orders placed in January 2023
SELECT * FROM Orders WHERE OrderDate BETWEEN '2023-01-01' AND '2023-01-31';

-- Get the details of each order, including the customer name and email
SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate
FROM Orders
JOIN Customers ON Orders.CustomerID = Customers.CustomerID;

-- List the products purchased in a specific order (e.g., OrderID = 1)
SELECT Products.ProductID, Products.ProductName, OrderItems.Quantity
FROM Products
JOIN OrderItems ON Products.ProductID = OrderItems.ProductID
WHERE OrderItems.OrderID = 1;

-- Calculate the total amount spent by each customer
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID;

-- Find the most popular product (the one that has been ordered the most)
SELECT Products.ProductID, Products.ProductName, SUM(OrderItems.Quantity) AS TotalOrdered
FROM Products
JOIN OrderItems ON Products.ProductID = OrderItems.ProductID
GROUP BY Products.ProductID
ORDER BY TotalOrdered DESC
LIMIT 1;

-- Get the total number of orders and the total sales amount for each month in 2023
SELECT 
    DATE_FORMAT(OrderDate, '%Y-%m') AS Month,
    COUNT(*) AS TotalOrders,
    SUM(Price * Quantity) AS TotalSales
FROM Orders
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
WHERE OrderDate BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY Month;

-- Find customers who have spent more than $1000
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID
HAVING TotalSpent > 1000;
