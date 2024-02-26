from flask import Flask, render_template, json
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

@app.route('/books')
def books():
    query = "SELECT * FROM Books;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    
    return render_template("books.j2", Books=results)
    
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4925)) 
    #                                 ^^^^
    
    app.run(port=port, debug=True) 

