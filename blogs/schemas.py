"""blog schema"""
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
  """blog schema"""
  title: str
  body: str
  published: Optional[bool]
