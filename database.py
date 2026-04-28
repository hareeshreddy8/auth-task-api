import sqlite3

def get_connection():
    conn = sqlite3.connect("users.db")
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)""")