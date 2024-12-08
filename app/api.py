from dataclasses import dataclass

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from models import City, Transport
from route_planner import RoutePlanner, tm
from store import db

api = FastAPI(root_path="/api")


@api.get("/city", response_model=list[City])
async def get_cities():
    return db.cities


@api.get("/transport", response_model=list[Transport])
async def get_transports():
    return db.transports


@api.post("/city", response_model=City)
async def add_city(city: City):
    db.add_city(city)
    return city


@api.post("/transport", response_model=Transport)
async def add_transport(transport: Transport):
    db.add_transport(transport)
    return transport


@api.get("/routeMap", response_model=dict[str, str])
async def get_route_map():
    return {"data": db.route_map}


@dataclass
class RoutePlanReq:
    strategy: str
    start: str
    end: str


@api.post("/routePlan", response_model=list[Transport])
async def get_route_plan(req: RoutePlanReq):
    return RoutePlanner.plan(tm, req.start, req.end, req.strategy)


api.mount("", app=StaticFiles(directory="app/static", html=True), name="static")
