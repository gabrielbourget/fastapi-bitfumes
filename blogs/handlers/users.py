from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm import Session

from .. import database, hashing, models, schemas

db = Depends(database.get_db)

def get_user(user_id: int, db: Session = db):
  """get user endpoint"""
  user = db.query(models.User).filter(models.User.id == user_id).first()

  if not user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = f"User with id {user_id} not found"
    )

  return user

async def create_user(user: schemas.User, db: Session = db):
  """create user endpoint"""

  try:
    new_user = models.User(
      name = user.name,
      email = user.email,
      password = hashing.bcrypt(password = user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.ReadUser(name = new_user.name, email = new_user.email)
  except IntegrityError as e:
    db.rollback()
    raise HTTPException(status_code = 400, detail = "User already exists") from e
  except DatabaseError as e:
    db.rollback()
    raise HTTPException(status_code = 500, detail = "Database error") from e