import queue
from collections import defaultdict

from .base_struct.adjacency_list_graph import AdjacencyListGraph
from .base_struct.graph import Graph, Node, Edge
from .models import City, Transport
from .store import db
from .time_segment import TimeSegment


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
    """将时间字符串转换为整数"""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m


def calc_total_cost(path: list[Transport], start_time: str = '') -> (int, int):
    '''计算路径的总花费和总时间，如果传入了start_time，则计算从start_time开始的的总时间'''
    total_price = sum(map(lambda x: x.price, path))
    if start_time:
        ts = TimeSegment(start_time, start_time) + TimeSegment(path[0].start_time, path[0].end_time)
    else:
        ts = TimeSegment(path[0].start_time, path[0].end_time)
    for t in path[1:]:
        ts += TimeSegment(t.start_time, t.end_time)

    return total_price, ts.total_time

class RoutePlanner:
    """静态类，路径规划的具体实现"""

    @staticmethod
    def plan(tm: TransportMap, start: str, end: str, strategy: str, start_time: str = "") -> tuple[
        list[Transport], int, int]:
        if strategy == "cheapest":
            path = RoutePlanner.cheapest(tm, start, end)
            cost = calc_total_cost(path)
            return path, cost[0], cost[1]
        elif strategy == "fastest":
            path = RoutePlanner.fastest_v3(tm, start, end, start_time)
            cost = calc_total_cost(path, start_time)
            return path, cost[0], cost[1]
        elif strategy == "leastTransfers":
            path = RoutePlanner.transfer_count_least_v2(tm, start, end)
            cost = calc_total_cost(path)
            return path, cost[0], cost[1]
        else:
            raise ValueError("Unknown strategy")

    @staticmethod
    def cheapest(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''Dijkstra算法，不需要考虑时间，只考虑价格'''
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
                        lambda e: time2int(e.value.start_time_int) >= time2int(path[-1].end_time),
                        edges[to_node])
                else:
                    available_transports = edges[to_node]
                try:
                    edge = min(available_transports, key=lambda e: time2int(e.value.start_time_int))
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
        return min(paths, key=lambda ts: (time2int(ts[-1].end_time_int) - time2int(ts[0].start_time_int)))

    @staticmethod
    def fastest_v2(tm: TransportMap, start: str, end: str, start_time: int | str | TimeSegment) -> list[Transport]:
        '''基于Dijkstra思想，找到耗时最短的路径'''
        if not isinstance(start_time, TimeSegment):
            start_time = TimeSegment(start_time, start_time)
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue: queue.PriorityQueue[tuple[TimeSegment, Node, list[Edge[Transport]]]] = queue.PriorityQueue()
        pri_queue.put((start_time, start_node, []))
        visited = set()
        while not pri_queue.empty():
            current_time, node, path = pri_queue.get()
            if node in visited:
                continue
            visited.add(node)
            if node == end_node:
                return [edge.value for edge in path if isinstance(edge.value, Transport)]
            for edge in node.edges:
                pri_queue.put(
                    (current_time + TimeSegment(edge.value.start_time, edge.value.end_time), edge.to_node,
                     path + [edge]))
        return []

    @staticmethod
    def fastest_v3(tm: TransportMap, start: str, end: str, start_time: int | str | TimeSegment) -> list[Transport]:
        '''基于Dijkstra思想，找到耗时最短的路径'''
        if not isinstance(start_time, TimeSegment):
            start_time = TimeSegment(start_time, start_time)
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue: queue.PriorityQueue[tuple[TimeSegment, Node, list[Edge[Transport]]]] = queue.PriorityQueue()
        pri_queue.put((start_time, start_node, []))
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
                def calc_real_cost_time(edge: Edge[Transport]) -> TimeSegment:
                    '''计算实际的时间'''
                    return current_time + TimeSegment(edge.value.start_time, edge.value.end_time)

                edge = min(edges[to_node], key=lambda e: calc_real_cost_time(e))
                pri_queue.put(
                    (calc_real_cost_time(edge), edge.to_node, path + [edge]))
        return []
    @staticmethod
    def transfer_count_least(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''深搜，暴力搜索所有路径，返回换乘次数最少的路径'''
        paths = RoutePlanner.get_all_paths(tm, start, end)
        paths = filter(RoutePlanner.time_reasonable, paths)
        return min(paths, key=RoutePlanner.calc_transfer_count)

    @staticmethod
    def transfer_count_least_v2(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''Dijkstra算法'''
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue = queue.PriorityQueue()
        pri_queue.put((0, start_node, []))
        visited = set()
        while not pri_queue.empty():
            distance, node, path = pri_queue.get()
            if node in visited:
                continue
            visited.add(node)
            if node == end_node:
                return [edge.value for edge in path if isinstance(edge.value, Transport)]
            for edge in node.edges:
                if path:
                    pri_queue.put((distance + (edge.value.run_id != path[-1].value.run_id), edge.to_node, path + [edge]))
                else:
                    pri_queue.put((distance, edge.to_node, path + [edge]))
        return []

    @staticmethod
    def transfer_count_least_v3(tm: TransportMap, start: str, end: str) -> list[Transport]:
        '''弃用，基于Dijkstra思想，找到耗时最短的路径'''
        start_node = tm.data.get_node(start)
        end_node = tm.data.get_node(end)
        pri_queue: queue.PriorityQueue[tuple[int, Node, list[Edge[Transport]]]] = queue.PriorityQueue()
        pri_queue.put((0, start_node, []))
        visited = set()
        while not pri_queue.empty():
            transfer_times, node, path = pri_queue.get()
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
                def calc_transfer(edge: Edge[Transport]) -> int:
                    '''计算换乘次数'''
                    if path:
                        return transfer_times + (edge.value.run_id != path[-1].value.run_id)
                    else:
                        return transfer_times
                # 错误的方法，在换乘数最小的条件下，此时不清楚一条路是否比另一条路更优
                edge = min(edges[to_node], key=lambda e: calc_transfer(e))
                pri_queue.put(
                    (calc_transfer(edge), edge.to_node, path + [edge]))
        return []

tm = TransportMap(db.cities, db.transports)
