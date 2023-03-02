from .db import Base , SessionLocal , get_db

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable = False)
    status    = Column(String,default='Open')
    assigned_user = Column(Integer, ForeignKey("users.id"),default=None)



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable = False)
    is_Free = Column(Boolean,default=True)
    is_Logged_in = Column(Boolean,default=False)
    task_id = Column(Integer, ForeignKey("tasks.id"),default=None)


