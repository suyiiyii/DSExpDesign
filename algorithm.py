import queue

from graph import Graph, Node


def dijkstra(g: Graph[int, int], start: Node[int], end: Node[int]) -> (int,list[Node[int]]):
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
            return distance,path
        for edge in node.edges:
            pri_queue.put((distance + edge.value, edge.to_node, path + [edge.to_node]))
    return -1,[]


def topo_sort(g:Graph) -> list:
    """拓扑排序 返回一个拓扑排序后的节点列表"""
    in_degree = {}
    for node in g.get_nodes_func(lambda x:x):
        in_degree[node] = 0
    for node in g.get_nodes_func(lambda x:x):
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
