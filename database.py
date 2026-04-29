import sqlite3

def get_connection_users():
    conn = sqlite3.connect("users.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
def create_table_users():
    conn = get_connection_users()
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
    conn = get_connection_users()
    cursor = conn.cursor()
    cursor.execute("""SELECT username FROM users """)
    all_usernames = cursor.fetchall()

    return all_usernames

def insert_user(username,password):
    conn = get_connection_users()

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


def get_user_by_username(username):
    conn = get_connection_users()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    user_details = cursor.fetchone()

    conn.close()
    return {
        "id" : user_details[0],
        "username" : user_details[1],
        "password":user_details[2]
    }


def get_connection_tasks():
    conn = sqlite3.connect("tasks.db")
    return conn
def create_table_tasks():
    conn = get_connection_tasks()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER ,
                   name TEXT NOT NULL,
                   priority TEXT,
                   due_date TEXT,
                   status BOOLEAN DEFAULT 0,
                   FOREIGN KEY (user_id) REFERENCES users(id))""")
    
    conn.commit()
    conn.close()

    