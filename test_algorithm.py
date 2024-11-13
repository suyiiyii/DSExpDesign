import pytest

from algorithm import dijkstra, topo_sort, kruskal
from graph import Graph
from test_graph import graph_implementations


@pytest.mark.parametrize("graph", graph_implementations)
def test_dijkstra(graph: type[Graph]):
    g: Graph[int, int] = graph()
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


@pytest.mark.parametrize("graph", graph_implementations)
def test_topo(graph: type[Graph]):
    g: Graph[str, int] = graph()
    a = g.add_node("A")
    b = g.add_node("B")
    c = g.add_node("C")
    d = g.add_node("D")
    e = g.add_node("E")
    f = g.add_node("F")
    a.add_edge(b, 1)
    b.add_edge(c, 1)
    c.add_edge(f, 1)
    a.add_edge(d, 1)
    d.add_edge(e, 1)
    e.add_edge(f, 1)

    ret = topo_sort(g)
    print(ret)
    # assert ret == [next(g.get_nodes("A")), next(g.get_nodes("B")), next(g.get_nodes("D")), next(g.get_nodes("C")),
    #                next(g.get_nodes("E")), next(g.get_nodes("F")), ]
    # 拓扑排序结果不唯一
    rank = {node: i for i, node in enumerate(ret)}
    assert rank[a] < rank[b]
    assert rank[b] < rank[c]
    assert rank[a] < rank[d]
    assert rank[d] < rank[e]
    assert rank[c] < rank[f]
    assert rank[e] < rank[f]


@pytest.mark.parametrize("graph", graph_implementations)
def test_prim(graph: type[Graph]):
    from algorithm import prim
    from graph import Graph
    from main import print_graph
    g: Graph[str, int] = graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")

    edges = ["A B 3",
             "A D 8",
             "A E 10",
             "B D 6",
             "D E 9",
             "E C 12",
             "B C 15"]
    for edge in edges:
        edge = edge.split()
        node1 = next(g.get_nodes(edge[0]))
        node2 = next(g.get_nodes(edge[1]))
        node1.add_edge(node2, int(edge[2]))
        node2.add_edge(node1, int(edge[2]))

    new_g = prim(g)
    print_graph(new_g)


@pytest.mark.parametrize("graph", graph_implementations)
def test_kruskal(graph: type[Graph]):
    from graph import Graph
    from main import print_graph
    g: Graph[str, int] = graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_node("D")
    g.add_node("E")

    edges = ["A B 3",
             "A D 8",
             "A E 10",
             "B D 6",
             "D E 9",
             "E C 12",
             "B C 15"]
    for edge in edges:
        edge = edge.split()
        node1 = next(g.get_nodes(edge[0]))
        node2 = next(g.get_nodes(edge[1]))
        node1.add_edge(node2, int(edge[2]))
        node2.add_edge(node1, int(edge[2]))

    new_g = kruskal(g)
    print_graph(new_g)
