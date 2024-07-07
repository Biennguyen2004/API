from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models
from .database import engine
from .routers import post, user, auth, vote

from .config import settings

 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}




# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel

# from typing import Optional, List
# from random import randrange    
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from sqlalchemy.orm import Session
# import time
# from . import models, schemas, utils
# from .database import engine, get_db
# from .router import post, user, auth


# models.Base.metadata.create_all(bind = engine)


# app = FastAPI()




        
        
        
# my_post = [{"title": "Đồ ăn ngon", "content": "Quán ăn ở đây ngon quá", "id":1},{"title": "Địa điểm đẹp", "content": "Quảng ninh cảnh đẹp quá ", "id":2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p
    
    
    
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p['id'] == id:
#             return i

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)

# @app.get("/")
# def root(): 
#     return {"message": "hi"}










