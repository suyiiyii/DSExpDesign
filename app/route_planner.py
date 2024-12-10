import queue
from collections import defaultdict

from .base_struct.adjacency_list_graph import AdjacencyListGraph
from .base_struct.graph import Graph, Node, Edge
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
        for edge in transports:
            self._data.get_node(edge.start).add_edge(self._data.get_node(edge.end), edge)

    def dump(self) -> (list[dict], list[Transport]):
        cities = map(lambda x: {"name": x.value}, self._data.get_nodes_func(lambda x: True))
        transports = map(lambda x: x.value, list(self._data.get_edges_func(lambda x: True)))
        return cities, transports

    @property
    def data(self):
        return self._data


def time2int(time_str: str) -> int:
    '''将时间字符串转换为整数'''
    h, m = map(int, time_str.split(':'))
    return h * 60 + m


def time_delta(t_from: str | int, t_to: str | int) -> int:
    '''计算两个时间字符串的时间差'''
    if isinstance(t_from, str):
        t_from = time2int(t_from)
    if isinstance(t_to, str):
        t_to = time2int(t_to)

    if t_from <= t_to:
        return t_to - t_from
    else:
        return 24 * 60 - t_from + t_to

class RoutePlanner:
    """静态类，路径规划的具体实现"""

    @staticmethod
    def plan(tm: TransportMap, start: str, end: str, strategy: str) -> list[Transport]:
        if strategy == "cheapest":
            return RoutePlanner.cheapest(tm, start, end)
        elif strategy == "fastest":
            return RoutePlanner.fastest_v2(tm, start, end)
        elif strategy == "leastTransfers":
            return RoutePlanner.transfer_count_least(tm, start, end)
        else:
            raise ValueError("Unknown strategy")

    @staticmethod
    def cheapest(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''Dijkstra算法'''
        # TODO： 未考虑时间
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
        paths: list[list[Transport]] = []

        def dfs(node: Node, path: list[Transport]):
            # TODO: 目前只会选择最早出发的交通工具，还需要支持选择尽量少换乘的工具
            # 时间复杂度：O(n!)，空间复杂度：O(n)，n 为路径长度
            # 难以进一步优化，因为需要遍历所有路径
            if node.value in map(lambda p: p.start, path):
                return
            if node == end_node:
                paths.append(path)
                return
            # 按照 node 给 edge 分组
            edges = defaultdict(list[Edge[Transport]])
            to_nodes = set()
            for edge in node.edges:
                edges[edge.to_node].append(edge)
                to_nodes.add(edge.to_node)
            for to_node in to_nodes:
                # 选择暂未出发，但是最近出发的交通工具
                if path:
                    available_transports = filter(
                        lambda e: time2int(e.value.start_time) >= time2int(path[-1].end_time),
                        edges[to_node])
                else:
                    available_transports = edges[to_node]
                try:
                    edge = min(available_transports, key=lambda e: time2int(e.value.start_time))
                except ValueError:
                    continue

                dfs(to_node, path + [edge.value])
                # for edge in edges[to_node]:
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
    def fastest_v2(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''基于Dijkstra思想，找到耗时最短的路径'''
        # todo: 需要统一开始的时间，不然图上的起始时间都不一样，无法比较
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue: queue.PriorityQueue[tuple[int, Node, list[Edge[Transport]]]] = queue.PriorityQueue()
        pri_queue.put((0, start_node, []))
        visited = set()
        while not pri_queue.empty():
            current_time, node, path = pri_queue.get()
            if node in visited:
                continue
            visited.add(node)
            if node == end_node:
                return [edge.value for edge in path if isinstance(edge.value, Transport)]
            # 给 edge 按照 node 分组
            edges: dict[Node, list[Edge[Transport]]] = defaultdict(list[Edge[Transport]])
            to_nodes = set()
            for edge in node.edges:
                edges[edge.to_node].append(edge)
                to_nodes.add(edge.to_node)
            # 优先选择加上等待时间，到达目的地最早的交通工具
            for to_node in to_nodes:
                if path:
                    edge = min(edges[to_node], key=lambda e: time_delta(path[-1].value.end_time, e.value.end_time))
                    pri_queue.put(
                        (time_delta(path[-1].value.end_time, edge.value.end_time), edge.to_node, path + [edge]))
                else:
                    edge = min(edges[to_node], key=lambda e: time2int(e.value.start_time))
                    pri_queue.put((current_time + time_delta(edge.value.start_time, edge.value.end_time), edge.to_node,
                                   path + [edge]))
        return []
    @staticmethod
    def transfer_count_least(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''深搜，暴力搜索所有路径，返回换乘次数最少的路径'''
        paths = RoutePlanner.get_all_paths(tm, start, end)
        paths = filter(RoutePlanner.time_reasonable, paths)
        return min(paths, key=RoutePlanner.calc_transfer_count)



tm = TransportMap(db.cities, db.transports)
