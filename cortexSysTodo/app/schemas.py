from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# -------------------- User Schemas --------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None  # ← اختیاری


class UserLogin(BaseModel):
    username: str
    password: str 
    
    class Config:
        orm_mode = True  # برای کار با SQLAlchemy


# -------------------- Task Schemas --------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False   # 👈 Boolean
    priority: int = 0
    due_date: Optional[datetime] = None
    #user_id: int

#class TaskCreate(TaskCreate):
 #    user_id: int   # چون هر تسک باید به یه یوزر وصل بشه

class TaskOut(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int