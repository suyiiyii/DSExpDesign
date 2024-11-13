import pytest

from adjacency_list_graph import AdjacencyListGraph
from adjacency_matrix_graph import AdjacencyMatrixGraph
from graph import Graph

graph_implementations = [AdjacencyListGraph, AdjacencyMatrixGraph]  # Add other Graph implementations to this list


@pytest.mark.parametrize("graph", graph_implementations)
def test_main(graph: type[Graph]):
    g: Graph[int, int] = graph()
    n1 = g.add_node(1)
    n2 = g.add_node(2)
    n3 = g.add_node(3)
    n1.add_edge(n2, 12)
    n2.add_edge(n3, 23)
    n3.add_edge(n1, 31)
    n1.add_edge(n3, 13)
    n2.add_edge(n1, 21)
    print(list(n1.edges))
    assert len(list(n1.edges)) == 2
    n2.destroy()
    print(list(n1.edges))
    assert len(list(n1.edges)) == 1


@pytest.mark.parametrize("graph", graph_implementations)
def test_get_nodes(graph: type[Graph]):
    g: Graph[int, int] = graph()
    n1 = g.add_node(1)
    n2 = g.add_node(2)
    n3 = g.add_node(3)
    n4 = g.add_node(4)
    assert list(g.get_nodes(1)) == [n1]
    assert list(g.get_nodes(2)) == [n2]
    assert list(g.get_nodes(3)) == [n3]
    assert list(g.get_nodes(4)) == [n4]
    n1.destroy()
    assert list(g.get_nodes(1)) == []


@pytest.mark.parametrize("graph", graph_implementations)
def test_edges(graph: type[Graph]):
    g: Graph[int, int] = graph()
    n1 = g.add_node(2)
    n2 = g.add_node(2)
    n3 = g.add_node(3)
    n1.add_edge(n2, 12)
    n2.add_edge(n3, 23)
    n3.add_edge(n1, 31)
    n1.add_edge(n3, 13)
    n2.add_edge(n1, 21)
    assert len(list(n1.edges)) == 2
    assert len(list(n2.edges)) == 2
    assert len(list(n3.edges)) == 1
    assert {x.to_node for x in n1.edges} == {n2, n3}
    assert {x.to_node for x in n2.edges} == {n1, n3}
    assert {x.to_node for x in n3.edges} == {n1}
    n1.destroy()
    assert len(list(n1.edges)) == 0
    assert len(list(n2.edges)) == 1
    assert len(list(n3.edges)) == 0
    assert {x.to_node for x in n2.edges} == {n3}
    assert {x.to_node for x in n3.edges} == set()
    n2.destroy()
    assert len(list(n2.edges)) == 0
    assert len(list(n3.edges)) == 0
