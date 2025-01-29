"""blog schema"""
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
  """blog schema"""
  title: str
  body: str
  published: Optional[bool]

class BlogResponse(Blog):
  """blog response schema"""
  class Config:
    orm_mode = True