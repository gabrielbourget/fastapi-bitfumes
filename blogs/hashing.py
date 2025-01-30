"""hashing module"""
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

class Hash():
  """hashing class"""
  def bcrypt(self, password: str):
    """hash password utility"""
    hashed_password = pwd_ctx.hash(password)
    return hashed_password
