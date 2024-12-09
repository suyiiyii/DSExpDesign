import queue

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


def compare_first_element(item):
    return item[0]

class RoutePlanner:
    """静态类，路径规划的具体实现"""

    @staticmethod
    def plan(tm: TransportMap, start: str, end: str, strategy: str) -> list[Transport]:
        if strategy == "cheapest":
            return RoutePlanner.cheapest(tm, start, end)
        else:
            raise ValueError("Unknown strategy")

    @staticmethod
    def cheapest(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''Dijkstra算法'''
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue = queue.PriorityQueue()
        pri_queue.put((0, start_node, [start_node]))
        visited = set()
        while not pri_queue.empty():
            distance, node, path = pri_queue.get()
            if node in visited:
                continue
            visited.add(node)
            if node == end_node:
                return [edge.value for edge in path if isinstance(edge.value, Transport)]
            for edge in node.edges:
                pri_queue.put((distance + edge.value.price, edge.to_node, path + [edge]))
        return []



tm = TransportMap(db.cities, db.transports)
print(tm.dump())
