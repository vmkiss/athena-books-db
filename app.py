from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
import MySQLdb
db_connection = db.connect_to_database()

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("books.j2")

@app.route('/books', methods=["POST", "GET"])
def books():
    # Insert new book
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
        query = "INSERT INTO Books (title, authorID, publisherID, genre, price, inventoryQty) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (title, authorID, publisherID, genre, price, quantity))
        db_connection.commit()

        # redirect back to Books page
        return redirect("/books")
    
    # Grab books data so it can be sent to template
    if request.method == "GET":
        # Grab all books in Books - was getting error message when adding indents so I kept it all on one line
        query = "SELECT Books.bookID, Publishers.publisherName as Publishers, Authors.authorName AS Author, Books.title, Books.genre, Books.price, Books.inventoryQty FROM Books INNER JOIN Authors ON Authors.authorID = Books.authorID INNER JOIN Publishers ON Publishers.publisherID = Books.publisherID;"
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

        # render Books page passing query data, publisher data, and author data to template
        return render_template("books.j2", data=data, publishers=publisher_data, authors=author_data)

    # Commented out because I don't think we need this anymore
    # query = "SELECT * FROM Books;"
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    
    #return render_template("books.j2", Books=results)

# @app.route("/delete_books/<int:bookID")
# def delete_books(bookID):
    # query = "DELETE FROM Books WHERE bookID = '%s';"
    # cursor = db_connection.cursor()
    # cursor.execute(query, (bookID))
    # db_connection.commit()

    # redirect back to books page
    # return redirect("/books")
    
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4925)) 
    #                                 ^^^^
    
    app.run(port=port, debug=True) 

