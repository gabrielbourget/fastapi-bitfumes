"""main app file in blogs module"""
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Blog(BaseModel):
  """blog schema"""
  title: str
  body: str
  published: Optional[bool]

@app.post("/blogs")
async def create_blog(blog: Blog):
  """create blog endpoint"""
  return { "data": blog }
