from fastapi import FastAPI,HTTPException
from models import Usercreate,Userlogin
import database
import auth

database.create_table_users()
database.create_table_tasks()
auth_app = FastAPI()

@auth_app.post("/users",status_code=200)
def signup_user_api(user_details : Usercreate):
    data, error = auth.signup_user(user_details.username,user_details.password,database.usernames,database.insert_user)

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