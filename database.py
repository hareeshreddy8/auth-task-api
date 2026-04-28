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
    
    conn.commit()
    conn.close()

def usernames():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT username FROM users """)
    all_usernames = cursor.fetchall()

    return all_usernames

def insert_user(username,password):
    conn = get_connection()

    cursor = conn.cursor()

    query = f"INSERT INTO users (username,password) VALUES(?,?)"
    
    params = (username,password)

    cursor.execute(query,params)

    conn.commit()
    cursor.execute("""SELECT * FROM users WHERE username = ? """,(username,))
    user_details = cursor.fetchone()



    conn.close()
    return {
        "id" : user_details[0],
        "username": user_details[1]
    }