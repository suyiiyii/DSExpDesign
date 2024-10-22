import queue

from adjacency_list_graph import AdjacencyListGraph
from graph import Graph, Node


def dijkstra(g: Graph[int, int], start: Node[int], end: Node[int]) -> int:
    """Dijkstra算法，返回从 start 到 end 的最短路径"""
    pri_queue = queue.PriorityQueue()
    pri_queue.put((0, start))
    visited = set()
    while not pri_queue.empty():
        distance, node = pri_queue.get()
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            return distance
        for edge in node.edges:
            pri_queue.put((distance + edge.value, edge.to_node))
    return -1


if __name__ == "__main__":
    g: Graph[int, int] = AdjacencyListGraph()
    n1 = g.add_node(1)
    n2 = g.add_node(2)
    n3 = g.add_node(3)
    n4 = g.add_node(4)
    n1.add_edge(n2, 12)
    n2.add_edge(n3, 23)
    n3.add_edge(n1, 31)
    n1.add_edge(n3, 13)
    n2.add_edge(n1, 21)
    n3.add_edge(n4, 34)
    print(dijkstra(g, n1, n4))
