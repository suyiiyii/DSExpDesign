import queue

from graph import Graph, Node


def dijkstra(g: Graph[int, int], start: Node[int], end: Node[int]) -> (int, list[Node[int]]):
    """Dijkstra算法，返回从 start 到 end 的最短路径"""
    pri_queue = queue.PriorityQueue()
    pri_queue.put((0, start, [start]))
    visited = set()
    while not pri_queue.empty():
        distance, node, path = pri_queue.get()
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            return distance, path
        for edge in node.edges:
            pri_queue.put((distance + edge.value, edge.to_node, path + [edge.to_node]))
    return -1, []


def topo_sort(g: Graph) -> list:
    """拓扑排序 返回一个拓扑排序后的节点列表"""
    in_degree = {}
    for node in g.get_nodes_func(lambda x: True):
        in_degree[node] = 0
    for node in g.get_nodes_func(lambda x: True):
        for edge in node.edges:
            in_degree[edge.to_node] += 1
    que = []
    ans = []
    for node in in_degree:
        if in_degree[node] == 0:
            que.append(node)
    while que:
        node = que.pop(0)
        ans.append(node)
        for edge in node.edges:
            in_degree[edge.to_node] -= 1
            if in_degree[edge.to_node] == 0:
                que.append(edge.to_node)
    return ans


def prim(g: Graph[any, int]) -> Graph[any, int]:
    """Prim算法，返回最小生成树"""
    nodes = list(g.get_nodes_func(lambda x: True))
    if not nodes:
        return None
    new_g = g.__class__()
    start_node = nodes[0]
    visited = {start_node}
    for node in nodes:
        new_g.add_node(node.value)
    while len(visited) < len(nodes):
        min_edge = None
        for node in visited:
            for edge in node.edges:
                if edge.to_node not in visited and (min_edge is None or edge.value < min_edge.value):
                    min_edge = edge
        if min_edge is None:
            break
        visited.add(min_edge.to_node)
        from_node = next(new_g.get_nodes(min_edge.from_node.value))
        to_node = next(new_g.get_nodes(min_edge.to_node.value))
        from_node.add_edge(to_node, min_edge.value)
    return new_g

def kruskal(g: Graph[any, int]) -> Graph[any, int]:
    """Kruskal算法，返回最小生成树"""
    nodes = list(g.get_nodes_func(lambda x: True))
    edges = list(g.get_edges_func(lambda x: True))
    new_g = g.__class__()
    for node in nodes:
        new_g.add_node(node.value)
    # 初始化并查集
    parent = {}
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        parent[find(x)] = find(y)
    def same(x, y):
        return find(x) == find(y)

    edges.sort(key=lambda x: x.value)
    for edge in edges:
        if not same(edge.from_node, edge.to_node):
            from_node = next(new_g.get_nodes(edge.from_node.value))
            to_node = next(new_g.get_nodes(edge.to_node.value))
            from_node.add_edge(to_node, edge.value)
            union(edge.from_node, edge.to_node)
    return new_g
