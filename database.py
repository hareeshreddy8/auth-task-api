import sqlite3
def convert_rows_into_tasks(rows):
    tasks = []
    for row in rows :
        tasks = []
    #converting tuple data into json format for api
    for row in rows:
        task = {
            
            "id": row[0],
            "user_id": row[1],
            "name":row[2],
            "priority": row[3],
            "due_date": row[4],
            "status": bool(row[5])
        }

        tasks.append(task)

    return tasks

def get_connection():
    conn = sqlite3.connect("app.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
def create_table_users():
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

def users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT username,id FROM users """)
    all_users = cursor.fetchall()

    return all_users

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


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    user_details = cursor.fetchone()

    conn.close()
    if user_details:
        return {
        "id" : user_details[0],
        "username" : user_details[1],
        "password":user_details[2]
        }
    else:
        return None

def create_table_tasks():
    conn = get_connection()
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
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (user_id,name,priority,due_date) VALUES (?,?,?,?)",(user_id,name,priority,due_date))
    conn.commit()

    
    conn.close()

    return {"user_id" : user_id,
        "name" : name,
        "priority": priority,
        "due_date": due_date
        }

def get_all_tasks_by_user(user_id,limit,offset):
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute("""SELECT tasks.id,
                            tasks.name,
                            tasks.priority,
                            tasks.due_date,
                            tasks.status,
                            users.username
                        FROM tasks
                        JOIN users
                        ON tasks.user_id = users.id
                        WHERE users.id = ?
                        LIMIT ? OFFSET ?""", (user_id, limit, offset))
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM tasks JOIN users ON tasks.user_id = users.id WHERE tasks.user_id = ?", (user_id,))
    total = cursor.fetchone()[0]

    conn.close()
    tasks = []
    #converting tuple data into json format for api
    for row in rows:
        task = {
            
            "id": row[0],
            "name": row[1],
            "priority": row[2],
            "due_date": row[3],
            "status": bool(row[4]),
            "username": row[5]
        }

        tasks.append(task)
    return tasks,total

def complete_task_by_user(user_id,task_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = 1
    WHERE user_id = ?
    AND id = ?
    """,(user_id,task_id))
    conn.commit()

    cursor.execute("""SELECT * FROM tasks WHERE user_id = ? AND id = ?""",(user_id,task_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            
            "id": row[0],
            "user_id": row[1],
            "name":row[2],
            "priority": row[3],
            "due_date": row[4],
            "status": bool(row[5])
        }
    return None

def delete_task_by_user(task_id,user_id):
    conn = get_connection()
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


def filter_user_tasks(user_id,priority,status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT * FROM tasks WHERE user_id = ?"""
    params = [user_id]

    if priority :
        query += "AND tasks.priority = ?"
        params.append(priority)

    if status is not None:
        query += "AND tasks.status = ?"
        params.append(status)

    cursor.execute(query,tuple(params))

    rows = cursor.fetchall()

    conn.close()
    tasks = convert_rows_into_tasks(rows)

    return tasks

def sort_user_tasks(user_id,by,order):
    conn = get_connection()

    cursor = conn.cursor()
    # clean_order = "ASC" if order == "ASC" else "DESC"
    if by == "priority":
        query = f"""
                    SELECT * FROM tasks WHERE user_id = ?
                    ORDER BY 
                    CASE priority
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                    END
                    {order}
                """
        
    else:
        query = f"""SELECT * FROM tasks WHERE user_id = ? ORDER BY {by} {order}"""


    cursor.execute(query,(user_id,))

    rows = cursor.fetchall()

    conn.close()

    tasks = convert_rows_into_tasks(rows)
    return tasks


def tasks_statsistics_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM tasks
        WHERE user_id = ?
        GROUP BY status
    """, (user_id,))

    task_stats = cursor.fetchall()

    completed = 0
    pending = 0

    for status, count in task_stats:

        if status == 1:
            completed = count

        elif status == 0:
            pending = count

    conn.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }