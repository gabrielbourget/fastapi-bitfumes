"""main app file in blogs module"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError
from . import schemas, models, database, hashing
from .routers import blogs, users

app = FastAPI()

app.include_router(blogs.router)
# app.include_router(users.router)

models.Base.metadata.create_all(bind = database.engine)

# @app.get("/blogs")
# @app.get("/blogs", response_model = List[schemas.ReadBlog], tags=["blogs"])
# async def get_blogs(db: Session = Depends(database.get_db)):
#   """get blog endpoint"""
#   try:
#     blog_posts = db.query(models.Blog).all()
#     return blog_posts
#   except DatabaseError as e:
#     raise HTTPException(status_code = 500, detail = "Database error") from e
#   except Exception as e:
#     print(e)
#     raise HTTPException(status_code = 500, detail = "Internal server error") from e

# @app.get(
#   "/blogs/{blog_id}",
#   status_code = 200,
#   response_model = schemas.ReadBlog,
#   tags=["blogs"]
# )
# async def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
#   """get blog endpoint"""
#   try:
#     blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

#     if not blog_post:
#       raise HTTPException(
#         status_code = status.HTTP_404_NOT_FOUND,
#         detail = f"Blog post with id {blog_id} not found"
#       )
#       # response.status_code = status.HTTP_404_NOT_FOUND
#       # return { "error": f"Blog post with id {blog_id} not found" }

#     return blog_post
#   except DatabaseError as e:
#     raise HTTPException(status_code=500, detail="Database error") from e
#   except Exception as e:
#     raise HTTPException(status_code=500, detail="Internal server error") from e

# @app.post("/blogs", status_code = status.HTTP_201_CREATED, tags=["blogs"])
# async def create_blog(blog: schemas.Blog, db: Session = Depends(database.get_db)):
#   """create blog endpoint"""

#   try:
#     # new_blog_post = models.Blog(**blog.dict())
#     new_blog_post = models.Blog(title = blog.title, body = blog.body, user_id = 1)
#     db.add(new_blog_post)
#     db.commit()
#     db.refresh(new_blog_post)

#     return new_blog_post
#   except IntegrityError as e:
#     db.rollback()
#     raise HTTPException(status_code=400, detail="Blog post already exists") from e
#   except DatabaseError as e:
#     db.rollback()
#     raise HTTPException(status_code=500, detail="Database error") from e
#   except Exception as e:
#     db.rollback()
#     raise HTTPException(status_code=500, detail="Internal server error") from e

# @app.put("/blogs/{blog_id}", status_code = status.HTTP_202_ACCEPTED, tags=["blogs"])
# async def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(database.get_db)):
#   """update blog endpoint"""
#   try:
#     existing_blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

#     if not existing_blog_post:
#       raise HTTPException(
#         status_code = status.HTTP_404_NOT_FOUND,
#         detail = f"Blog post with id {blog_id} not found"
#       )

#     (db.query(models.Blog)
#       .filter(models.Blog.id == blog_id)
#       .update(blog.dict(), synchronize_session = False)
#     )
#     db.commit()

#     return { "data": "Blog post updated" }
#   except DatabaseError as e:
#     db.rollback()
#     raise HTTPException(status_code = 500, detail="Database error") from e
#   except Exception as e:
#     db.rollback()
#     print(e)
#     raise HTTPException(status_code = 500, detail="Internal server error") from e

# @app.delete("/blogs/{blog_id}", status_code = status.HTTP_204_NO_CONTENT, tags=["blogs"])
# async def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
#   """delete blog endpoint"""

#   try:
#     existing_blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

#     if not existing_blog_post:
#       raise HTTPException(
#         status_code = status.HTTP_404_NOT_FOUND,
#         detail = f"Blog post with id {blog_id} not found"
#       )

#     db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session = False)
#     db.commit()

#     return { "data": "Blog post deleted" }
#   except DatabaseError as e:
#     db.rollback()
#     raise HTTPException(status_code = 500, detail="Database error") from e
#   except Exception as e:
#     db.rollback()
#     raise HTTPException(status_code = 500, detail="Internal server error") from e

@app.get("/users/{user_id}", response_model = schemas.ReadUser, tags=["users"])
async def get_user(user_id: int, db: Session = Depends(database.get_db)):
  """get user endpoint"""
  user = db.query(models.User).filter(models.User.id == user_id).first()

  if not user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = f"User with id {user_id} not found"
    )

  return user

@app.post(
  "/users",
  status_code = status.HTTP_201_CREATED,
  response_model = schemas.ReadUser,
  tags=["users"]
)
async def create_user(user: schemas.User, db: Session = Depends(database.get_db)):
  """create user endpoint"""
  hasher = hashing.Hash()

  try:
    new_user = models.User(
      name = user.name,
      email = user.email,
      password = hasher.bcrypt(password = user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.ReadUser(name = new_user.name, email = new_user.email)
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(status_code = 400, detail = "User already exists") from e
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code = 500, detail = "Database error") from e
  except Exception as e:
    db.rollback()
    print(e)
    raise HTTPException(status_code = 500, detail = "Internal server error") from e
