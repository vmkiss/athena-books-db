from flask import Flask, render_template, json, redirect
import os
import database.db_connector as db
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
        if request.form.get("Add_Person"):
            # grab user form inputs
            title = request.form["title"]
            author = request.form["author"]
            publisher = request.form["publisher"]
            genre = request.form["genre"]
            price = request.form["price"]
            quantity = request.form["quantity"]

        # account for null genre
        if genre == "":
            query = "INSERT INTO Books (title, author, publisher, price, quantity) VALUES (%s, %s, %s, %s, %s)"
            cursor = db_connection.cursor()
            cursor.execute(query, (title, author, publisher, price, quantity))
            db_connection.commit()
        
        # no null inputs
        else:
            query = "INSERT INTO Books (title, author, publisher, genre, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor = db_connection.cursor()
            cursor.execute(query, (title, author, publisher, genre, price, quantity))
            db_connection.commit()

        # redirect back to Books page
        return redirect("/people")
        

            
    # Populate publisher dropdown form
    publisher_selection = "SELECT publisherID, publisherName FROM Publishers"
    cursor = db_connection.cursor()
    cursor.execute(publisher_selection)
    publisher_data = cursor.fetchall()

    # Populate author dropdown form
    author_selection = "SELECT authorID, authorName FROM Publishers"
    cursor = db_connection.cursor()
    cursor.execute(author_selection)
    author_data = cursor.fetchall()

    query = "SELECT * FROM Books;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    
    return render_template("books.j2", Books=results)
    
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4925)) 
    #                                 ^^^^
    
    app.run(port=port, debug=True) 

