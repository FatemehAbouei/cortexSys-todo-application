from fastapi import FastAPI, Depends,HTTPException,status
from sqlalchemy.orm import Session
from app import models, schemas, crud, security,jwt,db, auth, security
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=db.engine) # جدول‌ها (اگه ساخته نشده بودن)
app = FastAPI()
# Dependency برای گرفتن session دیتابیس
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Auth --------------------
@app.post("/register/", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    # db_user = crud.get_user_by_email(db, user.email)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user

@app.post("/login/",response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = jwt.create_access_token(db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

    # db_user = db.query(models.User).filter(models.User.email == user.email).first()
    # if not db_user or not security.verify_password(user.password, db_user.hashed_password):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # access_token = jwt.create_access_token({"user_id": db_user.id})
    # return {"access_token": access_token, "token_type": "bearer"}


# -------------------- User APIs --------------------
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    # return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)





@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db),current_user=Depends(auth.get_current_user)):   # فعلاً تستی):
      return crud.create_task(db=db, task=task, user_id=current_user.id)


@app.get("/tasks/", response_model=list[schemas.TaskOut])
def read_tasks(db: Session = Depends(get_db),current_user=Depends(auth.get_current_user)):
    return crud.get_tasks_by_user(db=db, user_id=current_user.id)


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):

    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

    #return crud.update_task(db, task_id=task_id, task=task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}

    #return crud.delete_task(db, task_id=task_id)






