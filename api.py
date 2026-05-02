from fastapi import FastAPI,HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from models import Usercreate,Userlogin,TaskCreate
import database
import task_manager,auth



database.create_table_users()
database.create_table_tasks()
auth_app = FastAPI()
security = HTTPBearer()

@auth_app.post("/users",status_code=200)
def signup_user_api(user_details : Usercreate):
    data, error = auth.signup_user(user_details.username,user_details.password)

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
        user_details.password
    )
    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    if error:
        msg, code = error
        raise HTTPException(status_code=code, detail=msg)

    token = auth.create_token(user_id)

    return {
        "message": "login successfull. ",
        "access_token": token
    }



@auth_app.post("/tasks",status_code=200)
def add_task_api(task: TaskCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = auth.decode_token(token)
    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    
    data,error = task_manager.add_task_logic(user_id,task.name,task.priority,task.due_date)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail=msg)
    
    return {
        "message": "Task created successfully. ",
        "data": data
    }

@auth_app.get("/tasks",status_code=200)
def fetch_all_task_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = auth.decode_token(token)

    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    
    tasks = task_manager.fetch_tasks(user_id)
    if not tasks :
        raise HTTPException(status_code=400,detail="no tasks found")
    return {
        "message": "Tasks fetched successfully",
        "data": tasks
    }

@auth_app.patch("/tasks/{task_id}/complete",status_code=200)
def complete_tasks_api(task_id : int,credentials:HTTPAuthorizationCredentials=Depends(security)):
    token = credentials.credentials
    user_id = auth.decode_token(token)
    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    
    updated_task , error = task_manager.complete_task(user_id,task_id)

    if error:
        msg,code = error
        raise HTTPException(status_code=code,detail = msg)
    
    return {
        "message": "task marked successfully. ",
        "data": updated_task
    }

@auth_app.delete("/tasks/{task_id}", status_code=200)
def delete_task_api(task_id: int,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = auth.decode_token(token)
    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    
    deleted_task, error = task_manager.delete_task(
        task_id,
        user_id
    )

    if error:
        msg, code = error
        raise HTTPException(status_code=code, detail=msg)

    return {
        "message": f"Task with task id {task_id} deleted successfully"
    }