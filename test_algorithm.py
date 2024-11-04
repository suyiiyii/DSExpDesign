from adjacency_list_graph import AdjacencyListGraph
from algorithm import dijkstra, topo_sort
from graph import Graph


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
    assert dst[0] == 47
    assert dst[1] == [n1, n3, n4]


def test_topo():
    g: Graph[str, int] = AdjacencyListGraph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")
    g.add_node("F")
    next(g.get_nodes("A")).add_edge(next(g.get_nodes("B")), 1)
    next(g.get_nodes("B")).add_edge(next(g.get_nodes("C")), 1)
    next(g.get_nodes("C")).add_edge(next(g.get_nodes("F")), 1)
    next(g.get_nodes("A")).add_edge(next(g.get_nodes("D")), 1)
    next(g.get_nodes("D")).add_edge(next(g.get_nodes("E")), 1)
    next(g.get_nodes("E")).add_edge(next(g.get_nodes("F")), 1)

    ret = topo_sort(g)
    print(ret)
    assert ret == [next(g.get_nodes("A")), next(g.get_nodes("B")), next(g.get_nodes("D")), next(g.get_nodes("C")),
                   next(g.get_nodes("E")), next(g.get_nodes("F")), ]
