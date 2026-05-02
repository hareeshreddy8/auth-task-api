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

def users():
    conn = get_connection_users()
    cursor = conn.cursor()
    cursor.execute("""SELECT username,id FROM users """)
    all_users = cursor.fetchall()

    return all_users

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


def insert_task_for_user(user_id,name,priority,due_date):
    conn = get_connection_tasks()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (user_id,name,priority,due_date) VALUES (?,?,?,?)",(user_id,name,priority,due_date))
    conn.commit()

    
    conn.close()

    return {"user_id" : user_id,
        "name" : name,
        "priority": priority,
        "due_date": due_date
        }

def get_all_tasks_by_user(user_id):
    conn = get_connection_tasks()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = ?",(user_id,))
    rows = cursor.fetchall()

    conn.close()
    tasks = []
    #converting tuple data into json format for api
    for row in rows:
        task = {
            
            "id": row[0],
            "user_id": row[1],
            "name": row[2],
            "priority": row[3],
            "due_date": row[4],
            "status": bool(row[5])
        }

        tasks.append(task)
    return tasks

def complete_task_by_user(user_id,task_id):
    conn = get_connection_tasks()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = 1
    WHERE user_id = ?
    AND id = ?
    """,(user_id,task_id))
    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE user_id = ? AND id = ?",(user_id,task_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "name": row[2],
            "priority": row[3],
            "due_date": row[4],
            "status": bool(row[5])
        }
    return None

def delete_task_by_user(task_id,user_id):
    conn = get_connection_tasks()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
        AND user_id = ?
        """,(task_id,user_id))
    
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return False

    conn.close()
    return True