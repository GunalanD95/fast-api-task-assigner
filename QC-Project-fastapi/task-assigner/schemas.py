from pydantic import BaseModel
from .db import Base 
from typing import Optional

class User(BaseModel):
    user_name: str 
    is_Free: bool = True 
    is_Logged_in: bool = False
    task_id: Optional[int] = None

    class Config():
        orm_mode = True

class LoginUser(BaseModel):
    is_Logged_in: bool = True

    class Config():
        orm_mode = True  


class Task(BaseModel):
    task_name: str
    status: str = 'Open'  
    assigned_user: Optional[int] = None
    class Config():
        orm_mode = True


