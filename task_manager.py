import database

#logic to add task into database for specific user 

def add_task_logic(user_id,name,priority,due_date):
    all_userids = [u[1] for u in database.users()]

    if user_id not in all_userids:
        return None,("Invalid Userid. ",400)
    
    if not name.strip():
        return None,("Invalid task name. ",400)
    
    priority = priority.lower()
    if priority not in {"high","medium","low"}:
        return None,("Invalid priority. ",400)
    
    data = database.insert_task_for_user(user_id,name,priority,due_date)
    return data,None

# def fetch_tasks(user_id):
#     tasks = database.get_all_tasks_by_user(user_id)

#     if tasks :
#         return tasks,None
#     else:
#         return None,(f"no tasks found for id {user_id}",404)

def complete_task(user_id,task_id):
    
    updated_task = database.complete_task_by_user(user_id,task_id)

    if not updated_task:
        return None,("No tasks found",404)
    
    return updated_task,None


def delete_task(task_id, user_id):
    
    if task_id <= 0:
        return None, ("Invalid task id", 400)

    deleted = database.delete_task_by_user(task_id, user_id)

    if not deleted:
        return None, ("Task not found", 404)

    return True, None

def paginate_tasks(user_id,limit,offset):
    if limit <= 0 :
        return None,("Invalid limit request",400)
    
    if offset  < 0 :
        return None,("invalid offset request",400)
    
    tasks,total = database.get_all_tasks_by_user(user_id,limit,offset)

    if not tasks :
        return tasks,("No tasks found",404)
    
    return [tasks,total],None

def filter_task(user_id,priority,status):
    if priority:
        priority = priority.lower()

        if priority not in {"high","low","medium"}:
            return None,("Invalide priority",400)
    
    filtered_tasks = database.filter_user_tasks(user_id,priority,status)

    return filtered_tasks,None

def sort_tasks_by(user_id,by,order):
    by = by.lower()

    if by not in {"due_date","priority"}:
        return None,("invalid sort criteria. ",400)
    sorted_tasks = database.sort_user_tasks(user_id,by,order)

    return sorted_tasks,None
    
