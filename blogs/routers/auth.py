"""auth router file"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, schemas

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

  return existing_user
