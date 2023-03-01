from pydantic import BaseModel
from .db import Base 

class User(BaseModel):
    user_name: str 
    is_Free: bool = True 
    is_Logged_in: bool = False

    class Config():
        orm_mode = True


class LoginUser(BaseModel):
    is_Logged_in: bool = True

    class Config():
        orm_mode = True   

class Task(BaseModel):
    task_id: int

    class Config():
        orm_mode = True