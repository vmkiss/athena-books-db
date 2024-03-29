# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 02/27/2024

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
import MySQLdb

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_kissv'
app.config['MYSQL_PASSWORD'] = '2679' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_kissv'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

#------------------------------------------PUBLISHERS-----------------------------------------------------
# CRUD operations for Publishers entity
# Code adapted from OSU 340 flask-starter-app (people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 03/04/2024
@app.route('/publishers', methods=["POST", "GET"])
def publishers():
    # Insert new publisher (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Publisher"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

        db_connection = db.connect_to_database()
        query = "INSERT INTO Publishers (publisherName, publisherAddress, publisherCity, publisherState, publisherZip) VALUES (%s, %s, %s, %s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (name, address, city, state, zip))
        db_connection.commit()
        db_connection.close()

        # redirect back to Publishers page
        return redirect("/publishers")
    
    # Grab publishers data so it can be sent to template
    if request.method == "GET":
        # Get all data from publishers
        db_connection = db.connect_to_database()
        query = "SELECT publisherID AS PublisherID, publisherName AS Name, publisherAddress AS Address, publisherCity AS City, publisherState AS State, publisherZip AS ZipCode FROM Publishers;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # render Publishers page using query data
        return render_template("publishers.j2", data=data)

#---------------------------------------------AUTHORS---------------------------------------------------------------------------------------
# CRUD operations for Authors entity
# Code adapted from OSU 340 flask-starter-app (people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 03/04/2024
@app.route('/authors', methods=["POST", "GET"])
def authors():
    # Insert new author (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Author"):
            # grab user form inputs
            name = request.form["name"]
            publisherID = request.form["publisher"]

        db_connection = db.connect_to_database()
        query = "INSERT INTO Authors (authorName, publisherID) VALUES (%s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (name, publisherID))
        db_connection.commit()
        db_connection.close()

        # redirect back to Authors page
        return redirect("/authors")
    
    # Grab authors data so it can be sent to template (READ)
    if request.method == "GET":
        # Get all data from Authors
        db_connection = db.connect_to_database()
        query = "SELECT Authors.authorID AS AuthorID, Authors.authorName AS Name, Publishers.publisherName AS Publisher FROM Authors INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()

        # Populate publisher dropdown form
        publisher_selection = "SELECT publisherID, publisherName FROM Publishers ORDER BY publisherName"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(publisher_selection)
        publisher_data = cursor.fetchall()
        db_connection.close()

        # render Authors page using query data and publisher data
        return render_template("authors.j2", data=data, publishers=publisher_data)
    
#----------------------------------------------CUSTOMERS---------------------------------------------------------------------------------
# CRUD operations for Customers entity
# Code adapted from OSU 340 flask-starter-app (people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 03/04/2024
@app.route('/customers', methods=["POST", "GET"])
def customers():
    # Insert new customer (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Customer"):
            # grab user form inputs
            name = request.form["name"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

        db_connection = db.connect_to_database()
        query = "INSERT INTO Customers (customerName, customerPhone, customerEmail, customerAddress, customerCity, customerState, customerZip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (name, phone, email, address, city, state, zip))
        db_connection.commit()
        db_connection.close()

        # redirect back to Customers page
        return redirect("/customers")
    
    # Grab customers data so it can be sent to template (READ)
    if request.method == "GET":
        # Get all data from Customers
        db_connection = db.connect_to_database()
        query = "SELECT customerID AS CustomerID, customerName AS Name, customerPhone as Phone, customerEmail as Email, customerAddress AS Address, customerCity AS City, customerState AS State, customerZip AS ZipCode FROM Customers;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # render Customers page using query data
        return render_template("customers.j2", data=data)
    
# UPDATE Customers
# Code adapted from OSU 340 flask-starter-app (edit people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 03/04/2024
@app.route("/edit_customer/<int:CustomerID>", methods=["POST", "GET"])
def edit_customer(CustomerID):
    # Get data from from customer selected by user
    if request.method == "GET":
        db_connection = db.connect_to_database()
        query = "SELECT customerID AS CustomerID, customerName AS Name, customerPhone as Phone, customerEmail as Email, customerAddress AS Address, customerCity AS City, customerState AS State, customerZip AS ZipCode FROM Customers WHERE CustomerID = %s" % (CustomerID)
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # render Edit Customers page with query data
        return render_template("edit_customers.j2", data=data)

    if request.method == "POST":
        # fire off if user clicks the 'submit' button on Edit Customer
        if request.form.get("EditCustomer"):
            # grab user form inputs
            id = request.form["CustomerID"]
            name = request.form["name"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

        # update customer with values provided by user
        db_connection = db.connect_to_database()
        query = "UPDATE Customers SET customerName = %s, customerPhone = %s, customerEmail = %s, customerAddress = %s, customerCity = %s, customerState = %s, customerZip = %s WHERE customerID = %s"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (name, phone, email, address, city, state, zip, id))
        db_connection.commit()
        db_connection.close()

        # redirect back to Customers page
        return redirect("/customers")


#-------------------------------------------------------BOOKS---------------------------------------------------------------
# CRUD operations for Books entity
# Code adapted from OSU 340 flask-starter-app (people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 02/27/2024
@app.route('/books', methods=["POST", "GET"])
def books():
    # Insert new book (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Book"):
            # grab user form inputs
            title = request.form["title"]
            authorID = request.form["author"]
            genre = request.form["genre"]
            price = request.form["price"]
            quantity = request.form["quantity"]
        
        db_connection = db.connect_to_database()
        query = "INSERT INTO Books (title, authorID, genre, price, inventoryQty) VALUES (%s, %s, %s, %s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (title, authorID, genre, price, quantity))
        db_connection.commit()
        db_connection.close()

        # redirect back to Books page
        return redirect("/books")
    
    # Grab books data so it can be sent to template (READ)
    if request.method == "GET":
        # Get all data from Books
        db_connection = db.connect_to_database()
        query = "SELECT Books.bookID as BookID, Books.title AS Title, Authors.authorName AS Author, Publishers.publisherName as Publisher, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity FROM Books INNER JOIN Authors ON Authors.authorID = Books.authorID INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID ORDER BY Books.title;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()

        # Populate author dropdown form
        author_selection = "SELECT authorID, authorName FROM Authors"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(author_selection)
        author_data = cursor.fetchall()

        db_connection.close()

        # render Books page using query data and author data
        return render_template("books.j2", data=data, authors=author_data)


#DELETE
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (delete people route)
# Queries and variable values are our original work
# Date retrieved: 03/04/2024
@app.route("/delete_book/<int:BookID>")
def delete_books(BookID):
    # delete book selected by user
    db_connection = db.connect_to_database()
    query = "DELETE FROM Books WHERE BookID = '%s';" 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (BookID,))
    db_connection.commit()
    db_connection.close()

    #redirect back to books page
    return redirect("/books")


# UPDATE
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (edit people route)
# Queries and variable values are our original work
# Date retrieved: 02/27/2024
@app.route("/edit_book/<int:BookID>", methods=["POST", "GET"])
def edit_book(BookID):
    if request.method == "GET":
        # Get data from book selected by user
        db_connection = db.connect_to_database()
        query = "SELECT Books.bookID as BookID, Publishers.publisherName as Publisher, Authors.authorName AS Author, Books.title AS Title, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity FROM Books INNER JOIN Authors ON Authors.authorID = Books.authorID INNER JOIN Publishers ON Publishers.publisherID = Authors.publisherID WHERE BookID = %s" % (BookID)
        cur = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        # Populate author dropdown form
        author_selection = "SELECT authorID, authorName FROM Authors"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(author_selection)
        author_data = cursor.fetchall()

        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("edit_books.j2", data=data, authors=author_data)


    if request.method == "POST":
        #fire off if user clicks the 'submit' button on Edit Book
        if request.form.get("EditBook"):
            #grab user form inputs
            id = request.form["BookID"]
            title = request.form["title"]
            author = request.form["author"]
            genre = request.form["genre"]
            price = request.form["price"]
            quantity = request.form["quantity"]

        # update book with values provided by user
        db_connection = db.connect_to_database()
        query = "UPDATE Books SET Books.title = %s, Books.authorID = %s, Books.genre = %s, Books.price = %s, Books.inventoryQty = %s WHERE BookID = %s"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (title, author, genre, price, quantity, id))
        db_connection.commit()
        db_connection.close()

        # redirect back to Books page
        return redirect("/books")
    

#--------------------------------------------------------------PURCHASES-------------------------------------------------
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (people route)
# Queries and variable values are our original work
# Date retrieved: 03/01/2024
@app.route('/purchases', methods=["POST", "GET"])
def purchases():
    # Insert new purchase (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Purchase"):
            # grab user form inputs
            customer = request.form["customer"]
            date = request.form["date"]
            status = request.form["status"]

            # insert purchase without customer
            if customer == "N/A" or customer == "0":
                db_connection = db.connect_to_database()
                query = "INSERT INTO Purchases (customerID, datePlaced, purchaseStatus) VALUES (NULL, %s, %s)" 
                cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query, (date, status))
                db_connection.commit()
                db_connection.close() 

            # insert purchase with customer
            else:
                db_connection = db.connect_to_database()
                query = "INSERT INTO Purchases (customerID, datePlaced, purchaseStatus) VALUES (%s, %s, %s)"
                cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query, (customer, date, status))
                db_connection.commit()
                db_connection.close()

            #redirect back to Purchases page
            return redirect("/add_book_purchase")

    # Grab purchases data so it can be sent to template (READ)
    if request.method == "GET":
        # Get all data from Purchases
        db_connection = db.connect_to_database()
        query = "SELECT Purchases.purchaseID as PurchaseID, Customers.customerName as Customer, Purchases.datePlaced as Date, Purchases.purchaseStatus as Status FROM Purchases LEFT JOIN Customers ON Customers.customerID = Purchases.customerID;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()

        # Populate book dropdown form
        book_selection = "SELECT bookID, title FROM Books"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(book_selection)
        book_data = cursor.fetchall()

        # Populate customer dropdown form
        customer_selection = "SELECT customerID, customerName FROM Customers"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(customer_selection)
        customer_data = cursor.fetchall()

        db_connection.close()
        #render Purchases page using wuery data, customer data, and book data
        return render_template("purchases.j2", data=data, customers=customer_data, books=book_data)

#DELETE from Purchases
# Code adapted from OSU 340 flask-starter-app (delete people route)
# Queries and variable values are our original work
# https://github.com/osu-cs340-ecampus/flask-starter-app
# Date retrieved: 03/01/2024
@app.route("/delete_purchase/<int:PurchaseID>")
def delete_purchases(PurchaseID):
    # delete purchase selected by user
    db_connection = db.connect_to_database()
    query = "DELETE FROM Purchases WHERE PurchaseID = '%s';" 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (PurchaseID,))
    db_connection.commit()
   # db_connection.close()

# also DELETE from BookPurchases 
    query2 = "DELETE FROM BookPurchases WHERE PurchaseID = '%s';" 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query2, (PurchaseID,))
    db_connection.commit()
    db_connection.close()
    #redirect back to purchases page
    return redirect("/purchases")

# UPDATE
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (edit people route)
# Queries and variable values are our original work
# Date retrieved: 03/01/2024
@app.route("/edit_purchase/<int:PurchaseID>", methods=["POST", "GET"])
def edit_purchase(PurchaseID):
    if request.method == "GET":
        # Get data from purchase selected by user        
        db_connection = db.connect_to_database()
        query = "SELECT Purchases.purchaseID as PurchaseID, Customers.customerName as Customer, Purchases.datePlaced as Date, Purchases.purchaseStatus as Status FROM Purchases LEFT JOIN Customers ON Customers.customerID = Purchases.customerID WHERE PurchaseID = %s" % (PurchaseID)
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()

        # Populate customer dropdown form
        customer_selection = "SELECT customerID, customerName FROM Customers"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(customer_selection)
        customer_data = cursor.fetchall()

        db_connection.close()
        #render Purchases page using query data and customer data
        return render_template("edit_purchases.j2", data=data, customers=customer_data)


    if request.method == "POST":
        if request.form.get("editPurchase"):
            # grab user form inputs
            id = request.form["PurchaseID"]
            customer = request.form["customer"]
            date = request.form["date"]
            status = request.form["status"]
        
            # Update selected purchase with values provided by user - NO CUSTOMER
            if customer == "N/A" or customer == "0":
                db_connection = db.connect_to_database()
                query = "UPDATE Purchases SET customerID=NULL, Purchases.datePlaced=%s, Purchases.purchaseStatus=%s WHERE PurchaseID=%s" 
                cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query, (date, status, id))
                db_connection.commit()
                db_connection.close()
             # Update selected purchase with values by user - CUSTOMER EXISTS   
            else:
                db_connection = db.connect_to_database()
                query = "UPDATE Purchases SET Purchases.customerID=%s, Purchases.datePlaced=%s, Purchases.purchaseStatus=%s WHERE PurchaseID=%s" 
                cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query, (customer, date, status, id))
                db_connection.commit()
                db_connection.close()

            #redirect back to Purchases page
            return redirect("/purchases")


#---------------------------------------------BOOKPURCHASES------------------------------------------------------------------------
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (people route)
# Queries and variable values are our original work
# Date retrieved: 03/04/2024
@app.route('/bookpurchases', methods=["POST", "GET"])
def bookpurchases():
    # (READ)
    if request.method == "GET":
        #Grab all items in BookPurchases
        db_connection = db.connect_to_database()
        query = "SELECT BookPurchases.BookPurchasesID, Books.bookID as BookID, Books.title as Book, Purchases.purchaseID as PurchaseID, BookPurchases.orderQty as Quantity, BookPurchases.unitPrice as Price, BookPurchases.lineTotal as Total FROM BookPurchases INNER JOIN Books ON Books.bookID = BookPurchases.bookID INNER JOIN Purchases ON BookPurchases.purchaseID = Purchases.purchaseID ORDER BY BookPurchasesID ASC;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # Render BookPurchases page using query data
        return render_template("bookpurchases.j2", data=data)

# ADD
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (people route)
# Queries and variable values are our original work
# Date retrieved: 03/04/2024
@app.route('/add_book_purchase', methods =["POST", "GET"])
def add_book_purchase():
    if request.method == "POST":
        if request.form.get("Add_Book_Purchase"):
            #grab user form inputs
            book = request.form["book"]
            quantity = request.form["quantity"]

        db_connection = db.connect_to_database()
        query = "INSERT INTO BookPurchases (bookID, purchaseID, orderQty, unitPrice, lineTotal) VALUES (%s, (SELECT MAX(purchaseID) FROM Purchases), %s, (SELECT price FROM Books WHERE bookID = %s), (orderQty*unitPrice))"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (book, quantity, book))
        db_connection.commit()
        db_connection.close()

        # redirect back to Add BookPurchase page
        return redirect("/add_book_purchase")
        
    if request.method == "GET":
        # Populate book dropdown form
        db_connection = db.connect_to_database()

        # Populate book dropdown form
        book_selection = "SELECT bookID, title FROM Books"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(book_selection)
        book_data = cursor.fetchall()
            
        db_connection.close()

        #render Purchases page passing query data
        return render_template("add_book_purchase.j2", books=book_data)

# UPDATE
# Code adapted from OSU 340 flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app (edit people route)
# Queries and variable values are our original work
# Date retrieved: 03/11/2024
@app.route("/edit_bookpurchases/<int:BookPurchasesID>", methods=["POST", "GET"])
def edit_bookpurchases(BookPurchasesID):
    if request.method == "GET":
    # get data from bookpurchase selected by user
        db_connection = db.connect_to_database()
        query = "SELECT BookPurchases.BookPurchasesID, Books.bookID as BookID, Books.title as Book, Purchases.purchaseID as PurchaseID, BookPurchases.orderQty as Quantity, BookPurchases.unitPrice as Price, BookPurchases.lineTotal as Total FROM BookPurchases INNER JOIN Books ON Books.bookID = BookPurchases.bookID INNER JOIN Purchases ON BookPurchases.purchaseID = Purchases.purchaseID WHERE BookPurchasesID = %s;" % (BookPurchasesID)
        cur = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("edit_bookpurchases.j2", data=data)

    if request.method == "POST":
        # fire off if user clicks the 'submit' button on Edit BookPurchase
        if request.form.get("editBookPurchase"):
            #grab user form inputs
            id = request.form["BookPurchasesID"]
            quantity = request.form["quantity"]

        # update selected BookPurchase with values from user
        db_connection = db.connect_to_database()
        query = "UPDATE BookPurchases SET orderQty=%s, lineTotal=(orderQty*unitPrice) WHERE BookPurchasesID= %s"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (quantity, id))
        db_connection.commit()
        db_connection.close()

        # redirect back to BookPurchases page
        return redirect("/bookpurchases")



# Listener

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 4929)) 
     
    app.run(port=port, debug=True) 

