from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError,  jwt

from ..schemas import TokenData

JWT_SECRET = "CH27f4/2AJLcYXNHU2CvFPbNyJ54imMBUt9Ug/pYsD0="
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY__MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRY__MINUTES)
  to_encode.update({ "exp": expire })
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm = JWT_ALGORITHM)
  return encoded_jwt

def verify_token(token: str):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Could not validate credentials",
    headers = { "WWW-Authenticate": "Bearer" }
  )

  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])
    email: str = payload.get("sub")

    if email is None:
      raise credentials_exception from None
    
    token_data = TokenData(email = email)
    return token_data
  except JWTError:
    raise credentials_exception from None
