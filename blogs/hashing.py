"""hashing module"""
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def bcrypt(self, password: str):
  """hash password utility"""
  hashed_password = pwd_ctx.hash(password)
  return hashed_password

def verify(plaintext_password, hashed_password):
  """verify password utility"""
  return pwd_ctx.verify(plaintext_password, hashed_password)
