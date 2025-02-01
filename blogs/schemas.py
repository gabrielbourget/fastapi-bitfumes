"""blog schema"""
from typing import List, Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
  """base user schema"""
  name: str
  email: str
  password: str

class User(BaseUser):
  """user schema"""
  class Config:
    """config schema for use with sqlalchemy"""
    from_attributes = True

class LoginUser(BaseModel):
  username: str
  password: str

class BaseBlog(BaseModel):
  """base blog schema"""
  title: str
  body: str
  published: Optional[bool]

class Blog(BaseBlog):
  """blog schema"""
  class Config:
    """config schema for use with sqlalchemy"""
    from_attributes = True

class ReadUser(BaseModel):
  """read user schema"""
  name: str
  email: str
  blogs: List[Blog] = []

  class Config:
    """config schema for use with sqlalchemy"""
    from_attributes = True

class ReadBlog(BaseModel):
  """blog response schema"""
  title: str
  body: str
  creator: ReadUser

  class Config:
    """config schema for use with sqlalchemy"""
    from_attributes = True

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  email: Optional[str] = None
