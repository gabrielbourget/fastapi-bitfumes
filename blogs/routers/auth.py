"""auth router file"""

# from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, hashing, models
from ..schemas import LoginUser
from ..utils.token import create_access_token

router = APIRouter(tags = ["auth"])

db = Depends(database.get_db)
empty_depends = Depends()

# def login_route(user: OAuth2PasswordRequestForm = empty_depends, db: Session = db):
@router.post("/login")
def login_route(user: LoginUser, db: Session = db):
  existing_user = db.query(models.User).filter(models.User.email == user.username).first()

  if not existing_user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = f"User with email {user.email} not found"
    )

  if not hashing.verify(user.password, existing_user.password):
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

  access_token = create_access_token(data = { "sub": user.username })

  return { "access_token": access_token, "token_type": "bearer" }
