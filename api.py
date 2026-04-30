from fastapi import FastAPI,HTTPException
from models import Usercreate,Userlogin,TaskCreate
import database
import auth

database.create_table_users()
database.create_table_tasks()
auth_app = FastAPI()

@auth_app.post("/users",status_code=200)
def signup_user_api(user_details : Usercreate):
    data, error = auth.signup_user(user_details.username,user_details.password,database.users,database.insert_user)

    if error :
        msg , code = error 
        raise HTTPException(status_code=code,detail = msg)
    
    return {
        "message" : "successfully signedup. ",
        "data" : data
    }

@auth_app.post("/login",status_code=200)
def login_user_request(user_request : Userlogin):
    msg= auth.login_user(user_request.username,user_request.password,database.get_user_by_username)

    return msg 

@auth_app.post("/tasks",status_code=200)
def add_task_api(task : TaskCreate):
    data,error = auth.add_task_logic(task.user_id,task.name,task.priority,task.due_date,database.users,database.insert_task_for_user)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail=msg)
    
    return data

@auth_app.get("/tasks",status_code=200)
def get_all_task_user(user_id : int):
    tasks = database.get_all_tasks(user_id)
    if not tasks :
        raise HTTPException(status_code=400,detail="no tasks found")
    return tasks

@auth_app.post("/tasks/{task_id}",status_code=200)
def update_tasks_api(user_id:int,task_id:int):
    updated_task , error = auth.update_task_user(user_id,task_id,database.update_task_user)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail = msg)
    
    return {
        "msg": "task updated successfully. ",
        "data": updated_task
    }

@auth_app.delete("/tasks/{task_id}",status_code=200)
def delete_task_api(user_id:int,task_id:int):
    deleted_task , error = auth.delete_task(user_id,task_id,database.delete_task_user)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail=msg)
    
    return {
        "msg": "task deleted successfully. ",
    }