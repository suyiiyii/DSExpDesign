from typing import Iterator, cast

from graph import Graph, Node, Edge, U, T


class AdjacencyListEdge(Edge):

    def __init__(self, from_node: Node, to_node: Node, value: U = None):
        self._from_node = from_node
        self._to_node = to_node
        self._value = value

    def __repr__(self):
        return f"Edge({self._from_node}, {self._to_node}, {self._value})"

    @property
    def value(self) -> U:
        return self._value

    @property
    def from_node(self) -> Node:
        return self._from_node

    @property
    def to_node(self) -> Node:
        return self._to_node

    def destroy(self):
        for edge in self._from_node.edges:
            if edge.to_node == self._to_node:
                node = cast(AdjacencyListNode, self._from_node)
                node.remove_edge(edge)
                break


class AdjacencyListNode(Node):

    def __init__(self, value: T = None):
        self._value: T = value
        self._edge: ["Edge[U]"] = []

    def __repr__(self):
        return f"Node({self._value})"

    @property
    def value(self) -> T:
        return self._value

    @property
    def edges(self) -> Iterator["Edge"]:
        return iter(self._edge)

    def add_edge(self, node: "Node", value: U) -> "Edge":
        new_edge = AdjacencyListEdge(self, node, value)
        self._edge.append(new_edge)
        return new_edge

    def remove_edge(self, edge: "Edge"):
        self._edge.remove(edge)

    def destroy(self):
        self._edge.clear()


class AdjacencyListGraph(Graph):

    def __init__(self):
        self._nodes: ["Node[T]"] = []

    def __repr__(self):
        return f"Graph({self._nodes})"

    def add_node(self, value: T) -> Node:
        new_node = AdjacencyListNode(value)
        self._nodes.append(new_node)
        return new_node

    def get_nodes(self, value: T) -> Iterator[Node]:
        for node in self._nodes:
            if node.value == value:
                yield node

    def get_edges(self, value: U) -> Iterator[Edge]:
        for node in self._nodes:
            for edge in node.edges:
                if edge.value == value:
                    yield edge
