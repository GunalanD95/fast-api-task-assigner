from .db import Base , SessionLocal , get_db

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable = False)
    is_Free = Column(Boolean,default=True)
    is_Logged_in = Column(Boolean,default=False)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable = False)