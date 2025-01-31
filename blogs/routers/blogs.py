"""blogs router file"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import database, schemas
from ..handlers.blogs import create_blog, delete_blog, get_blog, get_blogs, update_blog

router = APIRouter(
  tags = ["blogs"],
  prefix = "/blogs"
)

db = Depends(database.get_db)

@router.get("/{blog_id}", status_code = 200, response_model = schemas.ReadBlog)
def get_blog_route(blog_id: int, db: Session = db):
  return get_blog(blog_id, db)

@router.get("/", response_model = List[schemas.ReadBlog])
def get_blogs_route(db: Session = db):
  return get_blogs(db)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_blog_route(blog: schemas.Blog, db: Session = db):
  return create_blog(blog, db)

@router.put("/{blog_id}", status_code = status.HTTP_202_ACCEPTED)
def update_blog_route(blog_id: int, blog: schemas.Blog, db: Session = db):
  return update_blog(blog_id, blog, db)

@router.delete("/{blog_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_blog_route(blog_id: int, db: Session = db):
  return delete_blog(blog_id, db)
