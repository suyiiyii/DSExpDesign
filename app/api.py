from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from models import City,Transport
from store import db

api = FastAPI(root_path="/api")

@api.get("/city", response_model=list[City])
async def get_cities():
    return db.cities


@api.get("/transport", response_model=list[Transport])
async def get_transports():
    return db.transports


api.mount("", app=StaticFiles(directory="app/static", html=True), name="static")
