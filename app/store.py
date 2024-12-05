import json

from models import City, Transport

DATA_CITY_PATH = "./data/city.json"
DATA_TRANSPORT_PATH = "./data/transport.json"


class Database:

    def __init__(self):
        self._cities: list[City] = self._load()[0]
        self._transports: list[Transport] = self._load()[1]
        self._generate_graph()

    def _store(self):
        with open(DATA_CITY_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps([city.__dict__ for city in self._cities]))
        with open(DATA_TRANSPORT_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps([transport.__dict__ for transport in self._transports]))
        print("Data stored successfully")
        return

    def _generate_graph(self):
        with open("../graph.md", "w", encoding="utf-8") as f:
            f.write("# 线路图\n")
            f.write("```mermaid\n")
            f.write("graph\n")
            '''深圳 -- G2944 --> 广州'''
            for transport in self._transports:
                f.write(f"\t{transport.start} -- {transport.run_id} --> {transport.end}\n")
            f.write("```")

    def _load(self) -> (list[City], list[Transport]):
        with open(DATA_CITY_PATH, "r", encoding="utf-8") as f:
            cities = [City(**city) for city in json.loads(f.read())]
        with open(DATA_TRANSPORT_PATH, "r", encoding="utf-8") as f:
            transports = [Transport(**transport) for transport in json.loads(f.read())]
        return cities, transports

    @property
    def cities(self) -> list[City]:
        return self._cities

    @property
    def transports(self) -> list[Transport]:
        return self._transports

    def add_city(self, city: City):
        self._cities.append(city)
        self._store()

    def add_transport(self, transport: Transport):
        self._transports.append(transport)
        self._store()


db = Database()

if __name__ == '__main__':
    print(db.cities)
    print(db.transports)
