import json
import os
from pathlib import Path

from .models import City, Transport

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_CITY_PATH = BASE_DIR.parent / "data" / "city.json"
DATA_TRANSPORT_PATH = BASE_DIR.parent / "data" / "transport.json"
GRAPH_PATH = BASE_DIR.parent / "graph.md"

class ServiceException(Exception):
    pass

class Database:

    def __init__(self, city_file: Path = DATA_CITY_PATH, transport_file: Path = DATA_TRANSPORT_PATH):
        self._cities: list[City]
        self._transports: list[Transport]
        self._city_file_path = city_file
        self._transport_file_path = transport_file
        self._load()
        self._save_route_map()

    def _store(self):
        with open(self._city_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([city.__dict__ for city in self._cities], ensure_ascii=False, indent=2))
        with open(self._transport_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([transport.__dict__ for transport in self._transports], ensure_ascii=False, indent=2))
        print("Data stored successfully")
        return

    def _generate_graph(self) -> str:
        graph = ""
        graph += "graph\n"
        '''深圳 -- G2944 --> 广州'''
        for transport in self._transports:
            graph += (f"\t{transport.start} -- {transport.run_id}  {transport.price}￥<br/>"
                      f"{transport.start_time} - {transport.end_time} --> {transport.end}\n")
        return graph

    def _save_route_map(self):
        graph = ""
        graph += "# 线路图\n"
        graph += "```mermaid\n"
        graph += self._generate_graph()
        graph += "```"
        with open(GRAPH_PATH, "w", encoding="utf-8") as f:
            f.write(graph)

    def _load(self) -> (
            list[City], list[Transport]):
        with open(self._city_file_path, "r", encoding="utf-8") as f:
            cities = [City(**city) for city in json.loads(f.read())]
        with open(self._transport_file_path, "r", encoding="utf-8") as f:
            transports = [Transport(**transport) for transport in json.loads(f.read())]
        self._cities, self._transports = cities, transports
        return cities, transports

    @property
    def cities(self) -> list[City]:
        return self._cities

    @property
    def transports(self) -> list[Transport]:
        return self._transports

    @property
    def route_map(self) -> str:
        return self._generate_graph()

    def generate_graph_with_path(self, path: list[Transport]) -> str:
        graph = ""
        graph += "graph\n"
        for transport in self._transports:
            if transport in path:
                graph += (f"\t{transport.start} == {transport.run_id}  {transport.price}￥<br/>"
                          f"{transport.start_time} - {transport.end_time} ==> {transport.end}\n")
            else:
                graph += (f"\t{transport.start} -- {transport.run_id}  {transport.price}￥<br/>"
                          f"{transport.start_time} - {transport.end_time} --> {transport.end}\n")
        return graph

    def add_city(self, city: City):
        self._cities.append(city)
        self._store()

    def delete_city(self, city: City):
        for transport in self._transports:
            if transport.start == city.name or transport.end == city.name:
                raise ServiceException("City is used in transport")
        self._cities.remove(city)
        self._store()

    def add_transport(self, transport: Transport):
        self._transports.append(transport)
        self._store()

    def delete_transport(self, transport: Transport):
        self._transports.remove(transport)
        self._store()

    def check(self):
        cities = [city.name for city in self._cities]
        for transport in self._transports:
            if transport.price <= 0:
                raise ServiceException(f"Price must be positive {transport}")
            if transport.start not in cities or transport.end not in cities:
                raise ServiceException("City not found" + transport.start +" "+ transport.end)


def get_database(dataset: str):
    new_db = None
    if dataset == "full":
        new_db = Database()
    elif dataset == "exp1":
        new_db = Database(DATA_CITY_PATH.parent / "city_exp1.json", DATA_CITY_PATH.parent / "transport_exp1.json")
    elif dataset == "exp2":
        new_db = Database(DATA_CITY_PATH.parent / "city_exp2.json", DATA_CITY_PATH.parent / "transport_exp2.json")
    new_db.check()
    return new_db


if __name__ == '__main__':
    db = Database()
    db.check()
    print(db.cities)
    print(db.transports)