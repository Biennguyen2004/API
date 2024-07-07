from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authorized to perform requested action")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
 

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()



# from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# from .. import schemas, models
# from sqlalchemy.orm import Session
# from ..database import engine, get_db
# from typing import Optional, List


# router = APIRouter(
#     prefix="/posts",
#     tags=['Posts']
# )

# @router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
    
#     return posts

# @router.get("/", response_model= schemas.Post)
# def get_posts(db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts """)
#     # post=cursor.fetchall()
#     # print (post)
#     posts = db.query(models.Post).all()
#     return posts


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published),)
    
#     # new_post = cursor.fetchone()
#     # conn.commit()
    
    
#     # new_post =models.Post.create(title =post.title,content= post.content,published= post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# # @app.post("/posts", status_code=status.HTTP_201_CREATED)
# # def create_post(post: Post):
# #     post_dict = post.dict()
# #     post_dict['id'] = randrange(0,10000000)
# #     my_post.append(post_dict)
# #     return {"DATA": post_dict}





# @router.get("/{id}", response_model= List[schemas.Post])
# def get_posts(id: int,db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)),)
#     # post = cursor.fetchone()
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     print(post)
#     return  post


# # @app.get("/posts/{id}")
# # def get_posts(id: int,):
# #     post = find_post(id)
# #     if not post: 
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
# #                             detail=f"post with id: {id} was not found")
# #     print(post)
# #     return {"Post_details": post}

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)),)
#     # Del = cursor.fetchone()
#     # conn.commit()
#     Del = db.query(models.Post).filter(models.Post.id == id)
    
#     if Del.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exits")
#     Del.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_post(id: int):
# #     # delete post 
# #     # find the index in the arr that has required ID
# #     # my_post.pop(index)
# #     index = find_index_post(id)
# #     if index == None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
# #                             detail=f"post with id: {id} does not exits")
    
# #     my_post.pop(index) 
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)



# @router.put("/{id}", response_model= schemas.Post)
# def update_post(id :int,update_post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))) )
#     # updated_post = cursor.fetchone()
#     # conn.commit()
#     post_query=db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()    
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exits")
   
#     post_query.update(update_post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()

# @app.put("/posts/{id}")
# def update_post(id :int,post: Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exits")
#     post_dict = post.dict()
#     post_dict['id ']= id
#     my_post[index] = post_dict
#     return {"data":post_dict} 
    


# @app.get("/posts/{id}")
# def get_posts(id: int, response : Response):
    
#     post = find_post(id)
#     if not post: 
#         Response.status_code = status.HTTP_404_NOT_FOUND
#         return {'message': f"post with id: {id} was not found"}
#     print(post)
#     return {"Post_details": post}





# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_post[len(my_post)-1]
#     return{"detail": post}

# @app.post("/posts")
# def create_post(post: Post):
#     print(post)
#     print(post.dict())
#     return {"DATA": post}




# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content:{payload['content']}"}
# title str, content str, category, Bool published