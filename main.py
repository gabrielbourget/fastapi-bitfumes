"""main app file"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

# import uvicorn

class Blog(BaseModel):
  """blog schema"""
  title: str
  body: str
  published: Optional[bool]

app = FastAPI()

@app.get("/")
async def index():
  """hello world endpoint"""
  return {"message": "Hello World"}

@app.get("/blogs")
async def blogs(limit = 10, published: bool = True, sort: Optional[str] = None):
  """unpublished blog endpoint"""
  if sort == "Ascending":
    return { "data": "sort parameter included" }
  if published:
    return { "data": f"{limit} published blog posts" }

  return { "data": f"{limit} blog posts" }

@app.get("/blogs/unpublished")
async def unpublished_blogs():
  """blogs endpoint"""
  return { "data": "unpublished blogs" }

@app.get("/blogs/{blog_id}")
async def get_blog(blog_id: int):
  """get blog endpoint"""
  return { "id": blog_id }

@app.get("/blogs/{blog_id}/comments")
async def get_blog_comments(blog_id: int, limit = 10):
  """get blog comments endpoint"""
  return { "comments": ["comment 1", "comment 2", "comment 3"], "id": blog_id, "limit": limit }

@app.post("/blogs")
async def create_blog(blog: Blog):
  """create blog endpoint"""
  return { "data": blog }

@app.get("/about")
async def about():
  """about endpoint"""
  return { "data": "about endpoint" }


# if __name__ == "__main__":
#   uvicorn.run(app, host = "127.0.0.1", port = 9000)
