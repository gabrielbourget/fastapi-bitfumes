"""main app file in blogs module"""
from fastapi import FastAPI

from . import database, models
from .routers import auth, blogs, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)

models.Base.metadata.create_all(bind = database.engine)
