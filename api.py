from fastapi import FastAPI,HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from typing import Optional,List
from models import Usercreate,Userlogin,TaskCreate,filtertasks,sortCriteria
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
def login_user_api(user_details : Userlogin):
    user_id, error = auth.login_user(
        user_details.username,
        user_details.password
    )
    if not user_id :
        raise HTTPException(status_code=400,detail="invalid credentials.  ")
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
def fetch_tasks_api(credentials:HTTPAuthorizationCredentials = Depends(security),limit : int = 10,offset : int = 0):
    token = credentials.credentials
    user_id = auth.decode_token(token)

    if not user_id :
        raise HTTPException(status_code=401,detail="unauthorized. ")
    
    data,error = task_manager.paginate_tasks(user_id,limit,offset)
    if error :
        message,code = error
        raise HTTPException(status_code=code,detail=message)
    if data :
        return {
        "message": "Tasks fetched successfully",
        "count": data[1],
        "limit": limit,
        "Offset": offset,
        "data": data[0]
        }
@auth_app.get("/tasks/filter",status_code=200)
def filter_tasks_user_api(filter_by: filtertasks = Depends(filtertasks), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = auth.decode_token(token)

    if not user_id :
        raise HTTPException(status_code=401,detail = "unauthorized.")
    
    filtered_data,error = task_manager.filter_task(user_id,filter_by.priority,filter_by.status)

    if error :
        message, code = error
        raise HTTPException(status_code=code,detail=message)
    
    return {
        "message": "Tasks filtered successfully. ",
        "data": filtered_data
    }

@auth_app.get("/tasks/sort",status_code=200)
def sort_tasks_api(by:sortCriteria = Depends(sortCriteria),credentials : HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401,detail="unauthorized. ")
    sorted_tasks,error = task_manager.sort_tasks_by(user_id,by.by,by.order)

    if error :
        message, code = error
        raise HTTPException(status_code=code,detail=message)
    
    return {
        "message": "Tasks sorted successfully. ",
        "data": sorted_tasks
    }




@auth_app.patch("/tasks/{task_id}/complete",status_code=200)
def update_tasks_api(task_id : int,credentials:HTTPAuthorizationCredentials=Depends(security)):
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

@auth_app.get("/tasks/stats",status_code=200)
def tasks_stats_api(credentials : HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    user_id = auth.decode_token(token)

    if not user_id:
        raise HTTPException(status_code=401,detail="Unuthorized. ")
    
    stats,error = task_manager.stats_logic(user_id)

    if error :
        msg,code = error
        raise HTTPException(status_code=code,detail=msg)
    

    return {
        "message": "Stats obtained successfully. ",
        "data": stats
    }