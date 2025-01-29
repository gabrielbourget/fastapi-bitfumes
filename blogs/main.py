"""main app file in blogs module"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError
from . import schemas, models
from . import database

app = FastAPI()

models.Base.metadata.create_all(bind = database.engine)

def get_db():
  """get database connection"""
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/blogs")
async def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
  """create blog endpoint"""

  try:
    # new_blog_post = models.Blog(**blog.dict())
    new_blog_post = models.Blog(title = blog.title, body = blog.body)
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(status_code=400, detail="Blog post already exists") from e
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail="Database error") from e
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail="Internal server error") from e

  return { "data": new_blog_post }

@app.get("/blogs")
async def get_blogs(db: Session = Depends(get_db)):
  """get blog endpoint"""
  blog_posts = db.query(models.Blog).all()
  return { "data": blog_posts }
