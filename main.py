"""main app file"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
  """hello world endpoint"""
  return {"message": "Hello World"}

@app.get("/about")
def about():
  """about endpoint"""
  return { "data": "about endpoint" }
