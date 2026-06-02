import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INTEGER
)
""")

cursor.execute("""
INSERT INTO books (title, author, year)
VALUES
('1984', 'George Orwell', 1949),
('Dune', 'Frank Herbert', 1965),
('The Hobbit', 'J.R.R. Tolkien', 1937)
""")

conn.commit()
conn.close()

print("Database created")
