"""auth router file"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, hashing, models, schemas
from ..token import ACCESS_TOKEN_EXPIRY__MINUTES, create_access_token

router = APIRouter(tags = ["auth"])

db = Depends(database.get_db)

@router.post("/login")
def login_route(user: schemas.LoginUser, db: Session = db):
  existing_user = db.query(models.User).filter(models.User.email == user.username).first()

  if not existing_user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = f"User with email {user.email} not found"
    )

  if not hashing.verify(user.password, existing_user.password):
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")

  access_token_expiry = timedelta(minutes = ACCESS_TOKEN_EXPIRY__MINUTES)
  access_token = create_access_token(
    data = { "sub", user.username },
    expires_delta = access_token_expiry
  )

  return { "access_token": access_token, "token_type": "bearer" }
