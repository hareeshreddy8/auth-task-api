from fastapi import FastAPI,HTTPException
from fastapi import Header,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from models import Usercreate,Userlogin,TaskCreate
import database
import auth

database.create_table_users()
database.create_table_tasks()
auth_app = FastAPI()
security = HTTPBearer()

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
def login_user_request(user_details : Userlogin):
    user_id, error = auth.login_user(
        user_details.username,
        user_details.password,
        database.get_user_by_username
    )

    if error:
        msg, code = error
        raise HTTPException(status_code=code, detail=msg)

    token = auth.create_token(user_id)

    return {
        "access_token": token
    }

def get_user_id(token: str):
    return auth.decode_token(token)


@auth_app.post("/tasks",status_code=200)
def add_task_api(task: TaskCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = get_user_id(token)
    
    data,error = auth.add_task_logic(user_id,task.name,task.priority,task.due_date,database.users,database.insert_task_for_user)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail=msg)
    
    return data

@auth_app.get("/tasks",status_code=200)
def get_all_task_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = get_user_id(token)

    tasks = database.get_all_tasks(user_id)
    if not tasks :
        raise HTTPException(status_code=400,detail="no tasks found")
    return tasks

@auth_app.patch("/tasks/{task_id}/complete",status_code=200)
def complete_tasks_api(task_id : int,credentials:HTTPAuthorizationCredentials=Depends(security)):
    token = credentials.credentials
    user_id = get_user_id(token)

    updated_task , error = auth.complete_task(user_id,task_id ,database.update_task_user)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail = msg)
    
    return {
        "msg": "task marked successfully. ",
        "data": updated_task
    }

@auth_app.delete("/tasks/{task_id}", status_code=200)
def delete_task_api(task_id: int,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = get_user_id(token)

    deleted_task, error = auth.delete_task(
        task_id,
        user_id,
        database.delete_task_user
    )

    if error:
        msg, code = error
        raise HTTPException(status_code=code, detail=msg)

    return {
        "message": "Task deleted successfully"
    }