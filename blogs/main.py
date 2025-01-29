"""main app file in blogs module"""
from fastapi import FastAPI
from . import schemas, models
from . import database

app = FastAPI()

models.Base.metadata.create_all(bind = database.engine)

@app.post("/blogs")
async def create_blog(blog: schemas.Blog):
  """create blog endpoint"""
  return { "data": blog }
