from passlib.context import CryptContext
from fastapi import APIRouter, Depends, status, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def verify(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)

