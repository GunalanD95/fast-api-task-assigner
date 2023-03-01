from typing import Optional

from fastapi import FastAPI , Depends , Response
from . import schemas , db , models
from .db import engine
from sqlalchemy.orm import Session


app = FastAPI()

get_db = db.get_db
models.Base.metadata.create_all(engine)

@app.get("/")
def index():
    return {"Check": "Docs Page"}


# get all users
@app.get("/users/")
def get_all_users(db : Session = Depends(get_db)):
    address = db.query(models.Users).all()
    return address


# create user
@app.post('/create_user',response_model=schemas.User)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(user_name=request.user_name,is_Free =request.is_Free,is_Logged_in =request.is_Logged_in )
    print(new_user,"request",request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# login user

@app.put('/login/{id}', response_model=schemas.LoginUser)
def login_user(id: int, request: schemas.LoginUser,db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    user.is_Logged_in = request.is_Logged_in
    db.commit()
    return user



