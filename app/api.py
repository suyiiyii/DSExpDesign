from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.params import Depends, Header
from starlette.staticfiles import StaticFiles

from .models import City, Transport
from .route_planner import RoutePlanner, get_tm, TransportMap
from .store import ServiceException, Database, get_database

api = FastAPI(root_path="/api")


@dataclass
class ResultStatus:
    status: str
    msg: str = ""


def db_obj(dataset: str = Header(None)):
    # 根据头部返回不同的数据库对象
    return get_database(dataset)


def tm_obj(dataset: str = Header(None)):
    # 根据头部返回不同的数据库对象
    return get_tm(dataset)


@api.get("/city", response_model=list[City])
async def get_cities(db: Database = Depends(db_obj)):
    return db.cities


@api.get("/transport", response_model=list[Transport])
async def get_transports(db: Database = Depends(db_obj)):
    return db.transports


@api.post("/city", response_model=City)
async def add_city(city: City, db: Database = Depends(db_obj)):
    db.add_city(city)
    # tm.load(db.cities, db.transports)
    return city


@api.post("/transport", response_model=Transport)
async def add_transport(transport: Transport, db: Database = Depends(db_obj)):
    db.add_transport(transport)
    # tm.load(db.cities, db.transports)
    return transport


@api.post("/city/delete", response_model=ResultStatus)
async def delete_city(city: City, db: Database = Depends(db_obj)):
    try:
        db.delete_city(city)
        # tm.load(db.cities, db.transports)
    except ServiceException as e:
        return ResultStatus(status="error", msg=str(e))
    return ResultStatus(status="success", msg="delete success")


@api.post("/transport/delete", response_model=ResultStatus)
async def delete_transport(transport: Transport, db: Database = Depends(db_obj)):
    db.delete_transport(transport)
    # tm.load(db.cities, db.transports)
    return ResultStatus(status="success", msg="delete success")

@api.get("/routeMap", response_model=dict[str, str])
async def get_route_map(db: Database = Depends(db_obj)):
    return {"data": db.route_map}


@dataclass
class RoutePlanReq:
    strategy: str
    start: str
    end: str
    start_time: str

@dataclass
class RoutePlanResp:
    path: list[Transport]
    total_price: int
    total_time: int

@api.post("/routePlan", response_model=RoutePlanResp)
async def get_route_plan(req: RoutePlanReq, tm: TransportMap = Depends(tm_obj)):
    data = RoutePlanner.plan(tm, req.start, req.end, req.strategy, req.start_time)
    return RoutePlanResp(path=data[0], total_price=data[1], total_time=data[2])


api.mount("", app=StaticFiles(directory="app/static", html=True), name="static")
