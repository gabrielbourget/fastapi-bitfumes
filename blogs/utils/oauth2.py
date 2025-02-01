"""oauth2 utils"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from .token import verify_token

db = Depends(get_db)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = db):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )

  token_data = verify_token(token)

  user = db.query(models.User).filter(models.User.email == token_data.email).first()

  if not user:
    raise credentials_exception

  return user
