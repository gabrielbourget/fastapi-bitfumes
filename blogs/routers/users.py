"""users router file"""
# from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import database, schemas
from ..handlers.users import create_user, get_user

router = APIRouter(
  tags = ["users"],
  prefix = "/users"
)

db = Depends(database.get_db)

@router.get("/{user_id}", response_model = schemas.ReadUser)
def get_user_route(user_id: int, db: Session = db):
  return get_user(user_id, db)

@router.post("/", status_code = status.HTTP_201_CREATED,response_model = schemas.ReadUser)
def create_user_route(user: schemas.User, db: Session = db):
  return create_user(user, db)
