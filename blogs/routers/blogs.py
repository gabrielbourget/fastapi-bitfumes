"""blogs router file"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm import Session

from .. import database, models, schemas

router = APIRouter()

db = Depends(database.get_db)

@router.get(
  "/blogs/{blog_id}",
  status_code = 200,
  response_model = schemas.ReadBlog,
  tags=["blogs"]
)
async def get_blog(blog_id: int, db: Session = db):
  """get blog endpoint"""
  blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

  if not blog_post:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = f"Blog post with id {blog_id} not found"
    )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return { "error": f"Blog post with id {blog_id} not found" }

  return blog_post

@router.get("/blogs", response_model = List[schemas.ReadBlog], tags=["blogs"])
async def get_blogs(db: Session = db):
  """get blog endpoint"""
  blog_posts = db.query(models.Blog).all()
  return blog_posts

@router.post("/blogs", status_code = status.HTTP_201_CREATED, tags=["blogs"])
async def create_blog(blog: schemas.Blog, db: Session = db):
  """create blog endpoint"""

  try:
    # new_blog_post = models.Blog(**blog.dict())
    new_blog_post = models.Blog(title = blog.title, body = blog.body, user_id = 1)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)

    return new_blog_post
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(status_code=400, detail="Blog post already exists") from e
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail="Database error") from e

@router.put("/blogs/{blog_id}", status_code = status.HTTP_202_ACCEPTED, tags=["blogs"])
async def update_blog(blog_id: int, blog: schemas.Blog, db: Session = db):
  """update blog endpoint"""
  try:
    existing_blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not existing_blog_post:
      raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Blog post with id {blog_id} not found"
      )

    (db.query(models.Blog)
      .filter(models.Blog.id == blog_id)
      .update(blog.dict(), synchronize_session = False)
    )
    db.commit()

    return { "data": "Blog post updated" }
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code = 500, detail="Database error") from e

@router.delete("/blogs/{blog_id}", status_code = status.HTTP_204_NO_CONTENT, tags=["blogs"])
async def delete_blog(blog_id: int, db: Session = db):
  """delete blog endpoint"""

  try:
    existing_blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not existing_blog_post:
      raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Blog post with id {blog_id} not found"
      )

    db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session = False)
    db.commit()

    return { "data": "Blog post deleted" }
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code = 500, detail="Database error") from e
