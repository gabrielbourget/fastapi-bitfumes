"""main app file in blogs module"""
from fastapi import FastAPI, Depends, HTTPException, status
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

@app.get("/blogs")
async def get_blogs(db: Session = Depends(get_db)):
  """get blog endpoint"""
  try:
    blog_posts = db.query(models.Blog).all()
    return { "data": blog_posts }
  except DatabaseError as e:
    raise HTTPException(status_code = 500, detail = "Database error") from e
  except Exception as e:
    raise HTTPException(status_code = 500, detail = "Internal server error") from e

@app.get("/blogs/{blog_id}", status_code = 200)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
  """get blog endpoint"""
  try:
    blog_post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog_post:
      raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"Blog post with id {blog_id} not found"
      )
      # response.status_code = status.HTTP_404_NOT_FOUND
      # return { "error": f"Blog post with id {blog_id} not found" }

    return { "data": blog_post }
  except DatabaseError as e:
    raise HTTPException(status_code=500, detail="Database error") from e
  except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error") from e

@app.post("/blogs", status_code = status.HTTP_201_CREATED)
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

@app.put("/blogs/{blog_id}", status_code = status.HTTP_202_ACCEPTED)
async def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
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
  except Exception as e:
    db.rollback()
    print(e)
    raise HTTPException(status_code = 500, detail="Internal server error") from e

@app.delete("/blogs/{blog_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
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
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code = 500, detail="Internal server error") from e
