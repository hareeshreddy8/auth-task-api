from pydantic import BaseModel
from datetime import date


class Usercreate(BaseModel):
    username : str
    password : str

class Userlogin(BaseModel):
    username: str
    password : str

class TaskCreate(BaseModel):
    name : str
    priority : str
    due_date : date





