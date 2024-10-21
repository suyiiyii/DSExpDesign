from graph import Graph, Node, Edge, U, T
from adjacency_list_graph import AdjacencyListNode, AdjacencyListEdge, AdjacencyListGraph


if __name__ == "__main__":
    g :Graph[int,int] = AdjacencyListGraph()
    n1 = g.add_node(1)
    n2 = g.add_node(2)
    n3 = g.add_node(3)
    n1.add_edge(n2, 12)
    n2.add_edge(n3, 23)
    n3.add_edge(n1, 31)
    n1.add_edge(n3, 13)
    n2.add_edge(n1, 21)
    print(list(n1.edges))
    # n2.destroy()
    # print(list(n1.edges))

