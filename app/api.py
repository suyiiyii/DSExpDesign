from fastapi import FastAPI

import models
from store import db

app = FastAPI(root_path="/api")


@app.get("/city", response_model=list[models.City])
async def get_cities():
    return db.cities


@app.get("/transport", response_model=list[models.Transport])
async def get_transports():
    return db.transports
