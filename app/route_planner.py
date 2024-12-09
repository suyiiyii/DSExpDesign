import queue

from .base_struct.adjacency_list_graph import AdjacencyListGraph
from .base_struct.graph import Graph
from .models import City, Transport
from .store import db


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


def time2int(timestr: str) -> int:
    '''将时间字符串转换为整数'''
    h, m = map(int, timestr.split(':'))
    return h * 60 + m

class RoutePlanner:
    """静态类，路径规划的具体实现"""

    @staticmethod
    def plan(tm: TransportMap, start: str, end: str, strategy: str) -> list[Transport]:
        if strategy == "cheapest":
            return RoutePlanner.cheapest(tm, start, end)
        elif strategy == "fastest":
            return RoutePlanner.fastest(tm, start, end)
        elif strategy == "leastTransfers":
            return RoutePlanner.transfer_count_least(tm, start, end)
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

    @staticmethod
    def get_all_paths(tm: TransportMap, start: str, end: str) -> list[list[Transport]]:
        '''深搜，暴力搜索所有路径'''
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        paths = []
        def dfs(node, path):
            if node == end_node:
                paths.append([edge.value for edge in path if isinstance(edge.value, Transport)])
                return
            for edge in node.edges:
                if edge.to_node not in path:
                    dfs(edge.to_node, path + [edge])
        dfs(start_node, [])
        return paths

    @staticmethod
    def time_reasonable(path: list[Transport]) -> bool:
        '''判断路径是否合理'''
        for i in range(len(path) - 1):
            if time2int(path[i].end_time) > time2int(path[i + 1].start_time):
                return False
        return True

    @staticmethod
    def calc_transfer_count(path: list[Transport]) -> int:
        '''计算换乘次数'''
        st = set()
        for t in path:
            st.add(t.run_id)
        return len(st)

    @staticmethod
    def fastest(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''深搜，暴力搜索所有路径，返回耗时最短的路径'''
        paths = RoutePlanner.get_all_paths(tm, start, end)
        paths = filter(RoutePlanner.time_reasonable, paths)
        return min(paths, key=lambda ts: (time2int(ts[-1].end_time) - time2int(ts[0].start_time)))

    @staticmethod
    def transfer_count_least(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''深搜，暴力搜索所有路径，返回换乘次数最少的路径'''
        paths = RoutePlanner.get_all_paths(tm, start, end)
        paths = filter(RoutePlanner.time_reasonable, paths)
        return min(paths, key=RoutePlanner.calc_transfer_count)



tm = TransportMap(db.cities, db.transports)
print(tm.dump())
