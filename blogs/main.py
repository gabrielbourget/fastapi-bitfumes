"""main app file in blogs module"""
from fastapi import FastAPI

from . import database, models
from .routers import blogs, users

app = FastAPI()

app.include_router(blogs.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind = database.engine)
