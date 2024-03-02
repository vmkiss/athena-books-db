from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
import MySQLdb
#db_connection = db.connect_to_database()

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

# CRUD operations for Publishers entity
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
    
    # Grab publishers data so it can be sent to template (READ)
    if request.method == "GET":
        # Grab all books in Books - was getting error message when adding indents so I kept it all on one line
        db_connection = db.connect_to_database()
        query = "SELECT publisherID AS PublisherID, publisherName AS Name, publisherAddress AS Address, publisherCity AS City, publisherState AS State, publisherZip AS ZipCode FROM Publishers;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("publishers.j2", data=data)
    
# CRUD operations for Customers entity
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

        # redirect back to Publishers page
        return redirect("/publishers")
    
    # Grab publishers data so it can be sent to template (READ)
    if request.method == "GET":
        # Grab all books in Books - was getting error message when adding indents so I kept it all on one line
        db_connection = db.connect_to_database()
        query = "SELECT customerID AS CustomerID, customerName AS Name, customerAddress AS Address, customerCity AS City, customerState AS State, customerZip AS ZipCode FROM Customers;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("customers.j2", data=data)
    


# CRUD operations for Books entity
@app.route('/books', methods=["POST", "GET"])
def books():
    # Insert new book (CREATE)
    if request.method == "POST":
        if request.form.get("Add_Book"):
            # grab user form inputs
            title = request.form["title"]
            authorID = request.form["author"]
            publisherID = request.form["publisher"]
            genre = request.form["genre"]
            price = request.form["price"]
            quantity = request.form["quantity"]

        # account for null genre
        # if genre == "":
            #query = "INSERT INTO Books (title, author, publisher, price, quantity) VALUES (%s, %s, %s, %s, %s)"
            #cursor = db_connection.cursor()
            #cursor.execute(query, (title, author, publisher, price, quantity))
            #db_connection.commit()
        
        # no null inputs
        #else:
        db_connection = db.connect_to_database()
        query = "INSERT INTO Books (title, authorID, publisherID, genre, price, inventoryQty) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (title, authorID, publisherID, genre, price, quantity))
        db_connection.commit()
        db_connection.close()

        # redirect back to Books page
        return redirect("/books")
    
    # Grab books data so it can be sent to template (READ)
    if request.method == "GET":
        # Grab all books in Books - was getting error message when adding indents so I kept it all on one line
        db_connection = db.connect_to_database()
        query = "SELECT Books.bookID as BookID, Publishers.publisherName as Publishers, Authors.authorName AS Author, Books.title AS Title, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity FROM Books INNER JOIN Authors ON Authors.authorID = Books.authorID INNER JOIN Publishers ON Publishers.publisherID = Books.publisherID;"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
            
        # Populate publisher dropdown form
        publisher_selection = "SELECT publisherID, publisherName FROM Publishers"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(publisher_selection)
        publisher_data = cursor.fetchall()

        # Populate author dropdown form
        author_selection = "SELECT authorID, authorName FROM Authors"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(author_selection)
        author_data = cursor.fetchall()

        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("books.j2", data=data, publishers=publisher_data, authors=author_data)


#DELETE
@app.route("/delete_book/<int:BookID>")
def delete_books(BookID):
    db_connection = db.connect_to_database()
    query = "DELETE FROM Books WHERE BookID = '%s';" 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (BookID,))
    db_connection.commit()
    db_connection.close()

    #redirect back to books page
    return redirect("/books")


# UPDATE
@app.route("/edit_book/<int:BookID>", methods=["POST", "GET"])
def edit_book(BookID):
    if request.method == "GET":
        #mySQL query to grab info of book with our passed ID
        #query = "SELECT * FROM Books WHERE BookID = %s" % (BookID)
        db_connection = db.connect_to_database()
        query = "SELECT Books.bookID as BookID, Publishers.publisherName as Publisher, Authors.authorName AS Author, Books.title AS Title, Books.genre AS Genre, Books.price as Price, Books.inventoryQty as Quantity FROM Books INNER JOIN Authors ON Authors.authorID = Books.authorID INNER JOIN Publishers ON Publishers.publisherID = Books.publisherID WHERE BookID = %s" % (BookID)
        cur = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        # Populate publisher dropdown form
        publisher_selection = "SELECT publisherID, publisherName FROM Publishers"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(publisher_selection)
        publisher_data = cursor.fetchall()

        # Populate author dropdown form
        author_selection = "SELECT authorID, authorName FROM Authors"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(author_selection)
        author_data = cursor.fetchall()

        db_connection.close()

        # render Books page passing query data, publisher data, and author data to template
        return render_template("edit_books.j2", data=data, publishers=publisher_data, authors=author_data)


    if request.method == "POST":
        #fire off if user clicks the 'submit' button on Edit Book
        if request.form.get("EditBook"):
            #grab user form inputs
            id = request.form["BookID"]
            title = request.form["title"]
            author = request.form["author"]
            publisher = request.form["publisher"]
            genre = request.form["genre"]
            price = request.form["price"]
            quantity = request.form["quantity"]

        # # account for null genre
        # if genre == "":
        #     query = "UPDATE Books SET Books.title = %s, Books.author = %s, Books.publisher = %s, Books.price = %s = NULL, Books.quantity = %s"
        #     cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute(query, (title, author, publisher, price, quantity))
        #     db_connection.commit()
        
        # # no null inputs
        # else:
        db_connection = db.connect_to_database()
        query = "UPDATE Books SET Books.title = %s, Books.authorID = %s, Books.publisherID = %s, Books.genre = %s, Books.price = %s, Books.inventoryQty = %s WHERE BookID = %s"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (title, author, publisher, genre, price, quantity, id))
        db_connection.commit()
        db_connection.close()

        # redirect back to Books page
        return redirect("/books")
    


    
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4978)) 
    #                                 ^^^^
    
    app.run(port=port, debug=True) 

