from datetime import datetime, timedelta
from typing import Optional

from python_jose import jwt

from . import schemas

JWT_SECRET = "CH27f4/2AJLcYXNHU2CvFPbNyJ54imMBUt9Ug/pYsD0="
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY__MINUTES = 30

def create_access_token(data: schemas.TokenData, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()

  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRY__MINUTES)
    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return encoded_jwt
