""""Blog model file"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from blogs.database import Base


class Blog(Base):
  """blog model"""

  __tablename__ = "blogs"

  id = Column(Integer, primary_key = True, index = True)
  title = Column(String)
  body = Column(String)
  published = Column(Boolean, default = False)
  user_id = Column(Integer, ForeignKey("users.id"))
  creator = relationship("User", back_populates="blogs")

class User(Base):
  """user model"""

  __tablename__ = "users"

  id = Column(Integer, primary_key = True, index = True)
  name = Column(String)
  email = Column(String)
  password = Column(String)
  blogs = relationship("Blog", back_populates="creator")
