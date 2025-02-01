from datetime import datetime, timedelta

from jose import jwt

JWT_SECRET = "CH27f4/2AJLcYXNHU2CvFPbNyJ54imMBUt9Ug/pYsD0="
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY__MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRY__MINUTES)
  to_encode.update({ "exp": expire })
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm = JWT_ALGORITHM)
  print(f"encoded jwt -> {encoded_jwt}")
  return encoded_jwt
