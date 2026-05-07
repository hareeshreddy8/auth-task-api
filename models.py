from pydantic import BaseModel
from typing import Optional, List, Literal
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

class filtertasks(BaseModel):
    priority : Optional[str] = None
    status : Optional[bool] = None

class sortCriteria(BaseModel):
    by : Literal["due_date", "priority"] = "due_date"
    order : Literal["ASC","DESC"] = "ASC"



