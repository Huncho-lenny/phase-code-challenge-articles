import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn