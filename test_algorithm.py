from adjacency_list_graph import AdjacencyListGraph
from graph import Graph
from main import dijkstra


def test_dijkstra():
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
    dst = dijkstra(g, n1, n4)
    assert dst == 47
