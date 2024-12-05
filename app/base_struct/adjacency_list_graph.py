from typing import Iterator, Callable

from .graph import Graph, Node, Edge, U, T


class AdjacencyListEdge(Edge[U]):

    def __init__(self, from_node: "AdjacencyListNode[T]", to_node: "AdjacencyListNode[T]", value: U = None):
        self._graph: AdjacencyListGraph
        self._from_node: AdjacencyListNode[T] = from_node
        self._to_node: AdjacencyListNode[T] = to_node
        self._value: U = value

    def __repr__(self):
        return f"Edge({self._from_node}, {self._to_node}, {self._value})"

    @property
    def value(self) -> U:
        return self._value

    @property
    def from_node(self) -> "AdjacencyListNode[T]":
        return self._from_node

    @property
    def to_node(self) -> "AdjacencyListNode[T]":
        return self._to_node

    def destroy(self):
        self._from_node._remove_edge(self)


class AdjacencyListNode(Node[T]):

    def __init__(self, value: T = None):
        self._graph: AdjacencyListGraph = None
        self._value: T = value
        self._edge: set["AdjacencyListEdge[U]"] = set()

    def __repr__(self):
        return f"Node({self._value})"

    @property
    def value(self) -> T:
        return self._value

    @property
    def edges(self) -> Iterator["AdjacencyListEdge[U]"]:
        return iter(self._edge)

    @property
    def rev_edges(self) -> Iterator["Edge"]:
        return self._graph.get_edges_func(lambda x: x.to_node == self)

    def add_edge(self, node: "AdjacencyListNode[T]", value: U) -> "AdjacencyListEdge[U]":
        new_edge = AdjacencyListEdge(self, node, value)
        new_edge._graph = self._graph.get_edges_func(lambda x: x)
        self._edge.add(new_edge)
        return new_edge

    def _remove_edge(self, edge: "AdjacencyListEdge[U]"):
        self._edge.remove(edge)

    def destroy(self):
        # 删除其他节点到当前节点的边
        for edge in list(self.rev_edges):
            edge.destroy()
        # 删除当前节点到其他节点的边
        for edge in list(self.edges):
            edge.destroy()
        # 删除当前节点
        self._graph._nodes.remove(self)


class AdjacencyListGraph(Graph):

    def __init__(self):
        self._nodes: [AdjacencyListNode[T]] = []

    def __repr__(self):
        return f"Graph({self._nodes})"

    def add_node(self, value: T) -> AdjacencyListNode[T]:
        new_node = AdjacencyListNode(value)
        new_node._graph = self
        self._nodes.append(new_node)
        return new_node

    def get_nodes_func(self, func: Callable[[AdjacencyListNode[T]], bool]) -> Iterator[AdjacencyListNode[T]]:
        for node in self._nodes:
            if func(node):
                yield node

    def get_edges_func(self, func: Callable[[AdjacencyListEdge[U]], bool]) -> Iterator[AdjacencyListEdge[U]]:
        for node in self._nodes:
            for edge in node.edges:
                if func(edge):
                    yield edge

    def get_nodes(self, value: T) -> Iterator[AdjacencyListNode[T]]:
        return self.get_nodes_func(lambda x: x.value == value)

    def get_edges(self, value: U) -> Iterator[AdjacencyListEdge[U]]:
        return self.get_edges_func(lambda x: x.value == value)
