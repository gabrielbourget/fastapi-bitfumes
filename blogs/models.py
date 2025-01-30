""""Blog model file"""
from sqlalchemy import Column, Integer, String, Boolean
from blogs.database import Base

class Blog(Base):
  """blog model"""

  __tablename__ = "blogs"

  id = Column(Integer, primary_key = True, index = True)
  title = Column(String)
  body = Column(String)
  published = Column(Boolean, default = False)

class User(Base):
  """user model"""

  __tablename__ = "users"

  id = Column(Integer, primary_key = True, index = True)
  name = Column(String)
  email = Column(String)
  password = Column(String)
