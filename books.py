from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
@app.route("/books/author/<author>/count")

def book_search(author):

    conn = sqlite3.connect("books.db")

    cursor = conn.cursor()

    cursor.execute("""
select count(*) from books
where author = ?
""", (author,))

    data = cursor.fetchone()

    conn.close()


