from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def book_to_dict(book):
    return {
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "year": book[3]
    }
def get_connection():
    return sqlite3.connect("books.db")
@app.route("/books")
def get_books():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books
    """)

    data = cursor.fetchall()

    conn.close()

    result = [book_to_dict(book) for book in data]

    return jsonify(result)

@app.route("/books/<int:book_id>")
def get_book(book_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    WHERE id = ?
    """, (book_id,))

    data = cursor.fetchone()

    conn.close()

    if data:
        result = book_to_dict(data) 
        return jsonify(result)
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route("/books/author/<author>")   
def get_books_by_author(author):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    WHERE author = ?
    """, (author,))

    data = cursor.fetchall()

    conn.close()

    result = [book_to_dict(book) for book in data]

    if not result:
        return jsonify({
            "error": "Books not found"
        }), 404
    else:
        return jsonify(result)

@app.route("/books/year/<int:year>")
def get_books_by_year(year):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    WHERE year = ?
    """, (year,))

    data = cursor.fetchall()

    conn.close()

    result = [book_to_dict(book) for book in data]

    if not result:
        return jsonify({
            "error": "Books not found"
        }), 404
    else:
        return jsonify(result)

@app.route("/books/search/<title>")
def search_books_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    WHERE title LIKE ?
    """, ('%' + title + '%',))

    data = cursor.fetchall()

    conn.close()

    result = [book_to_dict(book) for book in data]

    if not result:
        return jsonify({
            "error": "Books not found"
        }), 404
    else:
        return jsonify(result)

@app.route("/books/count")
def count_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM books
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return jsonify({"count": count})

@app.route("/books/oldest")
def get_oldest_book():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    ORDER BY year ASC 
    LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    if data:
        result = book_to_dict(data)
        return jsonify(result)
    else:
        return jsonify({"error": "Books not found"}), 404

@app.route("/books/newest")
def get_newest_book():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    ORDER BY year DESC 
    LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    if data:
        result = book_to_dict(data)
        return jsonify(result)
    else:
        return jsonify({"error": "Books not found"}), 404

@app.route("/books/random")
def get_random_book():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
select * from books
order by random()
limit 1
                   """)
    data = cursor.fetchone()
    conn.close()
    if data:
        return jsonify(book_to_dict(data))      
    else:
        return jsonify({"error": "Books not found"}), 404

@app.route("/books/author/<author>/count")
def count_books_by_author(author):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM books 
    WHERE author = ?
    """, (author,))

    count = cursor.fetchone()[0]

    if count == 0:
        conn.close()
        return jsonify({
            "error": "Books not found"
        }), 404
    conn.close()
    return jsonify({
        "count": count,
        "author": author
    })

@app.route("/books/between/<int:year1>/<int:year2>")
def get_books_between_years(year1, year2):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books 
    WHERE year BETWEEN ? AND ?
    """, (year1, year2))

    data = cursor.fetchall()

    conn.close()

    result = [book_to_dict(book) for book in data]

    if not result:
        return jsonify({
            "error": "Books not found"
        }), 404
    else:
        return jsonify(result)

@app.route("/books", methods=["POST"])
def post_book():
    
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    year = data.get("year")

    if not title or not author or not year:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()
    

    cursor.execute("""
    INSERT INTO books (title, author, year)
    VALUES (?, ?, ?)
    """, (title, author, year))
    
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Book added successfully"
    }), 201

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    DELETE FROM books 
    WHERE id = ?
    """, (book_id,))
    
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({
            "error": "Book not found"
        }), 404
    conn.close()
    
    return jsonify({"message": "Book deleted successfully"})

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    year = data.get("year")
    
    if not title or not author or not year:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE books 
    SET title = ?, author = ?, year = ?
    WHERE id = ?
    """, (title, author, year, book_id))
    
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({
            "error": "Book not found"
        }), 404
    conn.close()
    
    return jsonify({"message": "Book updated successfully"})

@app.route("/books/stats")
def get_book_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM books
    """)
    total_books = cursor.fetchone()[0]

    cursor.execute("""
    SELECT * FROM books
    ORDER BY year ASC 
    LIMIT 1  
    """)
    oldest_year = cursor.fetchone()

    cursor.execute("""
    SELECT * FROM books
    ORDER BY year DESC 
    LIMIT 1
    """)
    newest_year = cursor.fetchone()
    
    if newest_year and oldest_year:
        oldest_year = oldest_year[3]
        newest_year = newest_year[3]
    
    conn.close()

    return jsonify({
        "total_books": total_books,
        "oldest_year": oldest_year,
        "newest_year": newest_year
    })

if __name__ == "__main__":
    app.run(debug=True)

