# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def get_current_user_dependency(current_user=Depends(get_current_user)):
    return current_user
