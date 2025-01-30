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
    """config schema for use with sqlalchemy"""
    from_attributes = True

class User(BaseModel):
  """user schema"""
  name: str
  email: str
  password: str

class UserResponse(User):
  """user response schema"""
  class Config:
    """config schema for use with sqlalchemy"""
    from_attributes = True
