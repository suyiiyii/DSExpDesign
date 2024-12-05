from typing import Iterator, Callable

from .graph import Graph, Node, Edge, U, T


class AdjacencyMatrixEdge(Edge):
    def __init__(self, from_node: "AdjacencyMatrixNode", to_node: "AdjacencyMatrixNode", value: U = None):
        self._graph: AdjacencyMatrixGraph
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
        self._graph.remove_edge(self)


class AdjacencyMatrixNode(Node):

    def __init__(self, value: T = None):
        self._graph: AdjacencyMatrixGraph = None
        self.id: int = -1
        self._value: T = value

    def __repr__(self):
        return f"Node({self._value})"

    @property
    def value(self) -> T:
        return self._value

    @property
    def edges(self) -> Iterator["AdjacencyMatrixEdge"]:
        for edge in self._graph._data[self.id]:
            yield from edge

    @property
    def rev_edges(self) -> Iterator["Edge"]:
        for i in range(self._graph._cnt):
            if self._graph._data[i][self.id]:
                yield from self._graph._data[i][self.id]

    def add_edge(self, node: "AdjacencyMatrixNode", value: U) -> "AdjacencyMatrixEdge":
        return self._graph.add_edge(self, node, value)

    def destroy(self):
        self._graph.remove_node(self)


class AdjacencyMatrixGraph(Graph):

    def __init__(self):
        self._nodes: list[AdjacencyMatrixNode] = []
        self._data: list[list[set[AdjacencyMatrixEdge]]] = []  # 支持重边的邻接矩阵
        self._cnt: int = 0

    def __repr__(self):
        return f"Graph({self._nodes})"

    def add_node(self, value: T) -> AdjacencyMatrixNode:
        new_node = AdjacencyMatrixNode(value)
        new_node._graph = self
        self._nodes.append(new_node)
        new_node.id = self._cnt  # 为新的节点赋予编号
        self._cnt += 1
        for row in self._data:  # 拓展邻接矩阵
            row.append(set())
        self._data.append([set() for _ in range(self._cnt)])
        return new_node

    def add_edge(self, from_node: AdjacencyMatrixNode, to_node: AdjacencyMatrixNode, value: U) -> AdjacencyMatrixEdge:
        new_edge = AdjacencyMatrixEdge(from_node, to_node, value)
        new_edge._graph = self
        self._data[from_node.id][to_node.id].add(new_edge)
        return new_edge

    def remove_node(self, node: AdjacencyMatrixNode):
        """从图上删除当前节点"""
        # 邻接矩阵，不方便缩表，所以删除所有边，然后删除节点
        # 删除当前节点到其他节点的边
        for edge in list(node.edges):
            edge.destroy()
        # 删除其他节点到当前节点的边
        for edge in list(node.rev_edges):
            edge.destroy()
        self._nodes.remove(node)

    def remove_edge(self, edge: AdjacencyMatrixEdge = None):
        """从图上删除当前节点到另一个节点的所有边"""
        for edge1 in self._data[edge.from_node.id][edge.to_node.id]:
            if edge is not None and edge == edge1:
                self._data[edge.from_node.id][edge.to_node.id].remove(edge1)
                return

    def get_edges_func(self, func: Callable[[AdjacencyMatrixEdge], U]) -> U:
        for row in self._data:
            for edge_set in row:
                for edge in edge_set:
                    if func(edge):
                        yield edge

    def get_nodes_func(self, func: Callable[[T], bool]) -> Iterator[Node]:
        for node in self._nodes:
            if func(node):
                yield node
