from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'RetailStore'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        email = request.form['Email']
        date_of_birth = request.form['DateOfBirth']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Customers (FirstName, LastName, Email, DateOfBirth) VALUES (%s, %s, %s, %s)', (first_name, last_name, email, date_of_birth))
        mysql.connection.commit()
        cursor.close()
        flash('Customer added successfully')
        return redirect(url_for('add_customer'))
    return render_template('customer_form.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['ProductName']
        price = request.form['Price']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Products (ProductName, Price) VALUES (%s, %s)', (product_name, price))
        mysql.connection.commit()
        cursor.close()
        flash('Product added successfully')
        return redirect(url_for('add_product'))
    return render_template('product_form.html')

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form['CustomerID']
        order_date = request.form['OrderDate']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Orders (CustomerID, OrderDate) VALUES (%s, %s)', (customer_id, order_date))
        mysql.connection.commit()
        cursor.close()
        flash('Order added successfully')
        return redirect(url_for('add_order'))
    return render_template('order_form.html')

@app.route('/add_order_item', methods=['GET', 'POST'])
def add_order_item():
    if request.method == 'POST':
        order_id = request.form['OrderID']
        product_id = request.form['ProductID']
        quantity = request.form['Quantity']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO OrderItems (OrderID, ProductID, Quantity) VALUES (%s, %s, %s)', (order_id, product_id, quantity))
        mysql.connection.commit()
        cursor.close()
        flash('Order item added successfully')
        return redirect(url_for('add_order_item'))
    return render_template('order_item_form.html')

@app.route('/customers')
def customers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.close()
    return render_template('customers.html', customers=customers)

@app.route('/products')
def products():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products)

@app.route('/orders')
def orders():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Orders')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)

@app.route('/order_items')
def order_items():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM OrderItems')
    order_items = cursor.fetchall()
    cursor.close()
    return render_template('order_items.html', order_items=order_items)

@app.route('/list_customers')
def list_customers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.close()
    return render_template('list_customers.html', customers=customers)

@app.route('/orders_january_2023')
def orders_january_2023():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Orders WHERE YEAR(OrderDate) = 2023 AND MONTH(OrderDate) = 1')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders_january_2023.html', orders=orders)

@app.route('/order_details')
def order_details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate
        FROM Orders
        INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    ''')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('order_details.html', orders=orders)

@app.route('/order_products/<int:order_id>')
def order_products(order_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT Products.ProductName, Products.Price, OrderItems.Quantity
        FROM OrderItems
        INNER JOIN Products ON OrderItems.ProductID = Products.ProductID
        WHERE OrderItems.OrderID = %s
    ''', (order_id,))
    products = cursor.fetchall()
    cursor.close()
    return render_template('order_products.html', products=products)

@app.route('/customer_spending')
def customer_spending():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
        FROM Customers
        LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
        LEFT JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
        LEFT JOIN Products ON OrderItems.ProductID = Products.ProductID
        GROUP BY Customers.CustomerID
    ''')
    spending = cursor.fetchall()
    cursor.close()
    return render_template('customer_spending.html', spending=spending)

@app.route('/most_popular_product')
def most_popular_product():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT Products.ProductID, Products.ProductName, COUNT(OrderItems.ProductID) AS TotalOrders
        FROM Products
        LEFT JOIN OrderItems ON Products.ProductID = OrderItems.ProductID
        GROUP BY Products.ProductID
        ORDER BY TotalOrders DESC
        LIMIT 1
    ''')
    popular_product = cursor.fetchone()
    cursor.close()
    return render_template('most_popular_product.html', popular_product=popular_product)

@app.route('/monthly_sales')
def monthly_sales():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
    SELECT MONTH(OrderDate) AS Month,
           COUNT(*) AS TotalOrders,
           SUM(OrderItems.Quantity * Products.Price) AS TotalSales
    FROM Orders
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    WHERE YEAR(OrderDate) = 2023
    GROUP BY MONTH(OrderDate)
    ''')
    monthly_sales = cursor.fetchall()
    cursor.close()
    return render_template('monthly_sales.html', monthly_sales=monthly_sales)

@app.route('/big_spender')
def big_spender():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
        FROM Customers
        LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
        LEFT JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
        LEFT JOIN Products ON OrderItems.ProductID = Products.ProductID
        GROUP BY Customers.CustomerID
        HAVING TotalSpent > 1000
    ''')
    big_spenders = cursor.fetchall()
    cursor.close()
    return render_template('big_spender.html', big_spenders=big_spenders)


if __name__ == '__main__':
    app.run(debug=True)
