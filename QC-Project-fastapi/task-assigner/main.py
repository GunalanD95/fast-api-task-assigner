from typing import Optional
from fastapi import FastAPI , Depends , Response
from . import schemas , db , models
from .db import engine
from sqlalchemy.orm import Session
from collections import  deque 
import requests
from apscheduler.schedulers.background import BackgroundScheduler



app = FastAPI()


get_db = db.get_db
models.Base.metadata.create_all(engine)

@app.get("/")
async def index():
    return {"Check": "Docs Page"}


# create user
@app.post('/create_user',response_model=schemas.User)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(user_name=request.user_name,is_Free =request.is_Free,is_Logged_in =request.is_Logged_in,task_id = request.task_id )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get all users
@app.get("/users/")
async def get_all_users(db : Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


# login user
@app.put('/login/{id}', response_model=schemas.LoginUser)
async def login_user(id: int, request: schemas.LoginUser,db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    print("user--->",user)
    if not user:
        return {f'There is no user with id {id}'}
    user.is_Logged_in = request.is_Logged_in
    db.commit()
    return f"{user.user_name} has successfully logged in"


# create tasks
@app.post('/create_task',response_model=schemas.Task)
async def create_task(request: schemas.Task, db: Session = Depends(get_db)):
    new_task = models.Tasks(task_name=request.task_name,status=request.status)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# get all tasks
@app.get("/tasks/")
async def get_all_taskss(db : Session = Depends(get_db)):
    tasks = db.query(models.Tasks).all()
    return tasks


# get all open-free_tasks
def get_free_tasks(db):
    free_tasks = deque()
    free_tasks = db.query(models.Tasks).filter(models.Tasks.status == 'Open').all()
    return deque(free_tasks)

# get all free-users (loggedin)
def get_free_users(db):
    free_users = db.query(models.Users).filter(models.Users.is_Logged_in == True, models.Users.is_Free == True).all()
    return deque(free_users)


# get all in-progress-free_tasks
def get_in_progresss_tasks(db):
    tasks = db.query(models.Tasks).filter(models.Tasks.status == 'In Progress').all()
    return deque(tasks)


# Assign All Open-tasks
@app.post('/assign_all_tasks')
async def assign_free_tasks(db : Session = Depends(get_db)):
    free_tasks = get_free_tasks(db)
    free_users = get_free_users(db)

    if not free_tasks and not free_users:
        print("There is no Free-Tasks and Free_users ")
        return False
    elif free_tasks and not free_users:
        print("There are no Free_users ")
        return False
    elif free_users and not free_tasks:
        print("there is no Free-Tasks")
        return False
    
    while free_tasks:
        task_to_assign = free_tasks.popleft()
        if not free_users:
            break 
        assignee = free_users.popleft()

        # assign task to user
        assignee.task_id = task_to_assign.id
        assignee.is_Free = False

        # make task to in-progress
        task_to_assign.assigned_user = assignee.id
        task_to_assign.status = 'In Progress'
        
        db.commit()
        print(f"Assigned {task_to_assign.task_name} to {assignee.user_name}")

    print("Assigned all Free tasks")
    return True


# close tasks if assigned to user
@app.put('/close_all_tasks')
async def close_all_tasks(db : Session = Depends(get_db)):
    in_progress_tasks = get_in_progresss_tasks(db)

    if not in_progress_tasks:
        print("There are no in-progress tasks currently in pipeline")
        return False
    while in_progress_tasks:
        task = in_progress_tasks.popleft()

        task.status = 'Done'

        # remove task_id from user and make him free for next task 
        user = db.query(models.Users).filter(models.Users.id == task.assigned_user).first()

        user.is_Free = True 
        user.task_id = None


        db.commit()
        print(f"{task.task_name} has been completed by {user.user_name}")

    print("Closed all Inprogress tasks")
    return True 




def close_all_tasks():
    print("Calling Cron Job to assign free tasks and close all in-progress task")
    assign_tasks = requests.post('http://localhost:8000/assign_all_tasks')
    # if there are some tasks - then we can close them
    if assign_tasks:
        close_tasks = requests.put('http://localhost:8000/close_all_tasks')



# CRON-JOB
@app.on_event("startup")
async def startup():
    # Start the scheduled task scheduler on startup
    scheduler = BackgroundScheduler()
    # cron job to run the function every minute
    scheduler.add_job(close_all_tasks, 'cron', minute='*')
    scheduler.start()
    








