from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import Optional
from .security import hash_password
# -------------------- User CRUD --------------------
def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password) # بعداً هش می‌کنیم
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
 
# -------------------- Task CRUD --------------------
#from .models import Task
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task =  models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int,status: Optional[bool] = None, priority: Optional[int] = None):
    query= db.query( models.Task).filter( models.Task.user_id == user_id)
    if status is not None:
        query = query.filter(models.Task.status == status)
    
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    
    return query.all()

#محدود کردن Taskها به صاحبش 


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int,user_id:int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def toggle_task_status(db: Session, task_id: int, user_id: int):
    """برعکس کردن وضعیت یک تسک"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()
    
    if not task:
        return None

    task.status = not task.status
    db.commit()
    db.refresh(task)
    return task
    