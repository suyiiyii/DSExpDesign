from base_struct.adjacency_list_graph import AdjacencyListGraph
from base_struct.graph import Graph
from models import City, Transport
from store import db


class TransportMap:
    """内部存储城市和交通工具的图，用于进行路径规划"""

    def __init__(self, cities: list[City], transports: list[Transport]):
        self._data = None
        self.load(cities, transports)

    def load(self, cities: list[City], transports: list[Transport]):
        self._data: Graph[str, Transport] = AdjacencyListGraph()
        for city in cities:
            self._data.add_node(city.name)
        for transport in transports:
            self._data.get_node(transport.start).add_edge(self._data.get_node(transport.end), transport)

    def dump(self) -> (list[dict], list[Transport]):
        cities = map(lambda x: {"name": x.value}, self._data.get_nodes_func(lambda x: True))
        transports = map(lambda x: x.value, list(self._data.get_edges_func(lambda x: True)))
        return cities, transports

    @property
    def data(self):
        return self._data


class RoutePlanner:
    """静态类，路径规划的具体实现"""

    @staticmethod
    def plan(tm: TransportMap, start: str, end: str, strategy: str) -> list[Transport]:
        return tm.dump()[1]


tm = TransportMap(db.cities, db.transports)
print(tm.dump())
