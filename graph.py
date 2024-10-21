from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")


class Node(Generic[T]):
    """图的节点类，归属于某个图"""

    @abstractmethod
    def __init__(self, value: T = None):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @property
    @abstractmethod
    def value(self) -> T:
        pass

    @property
    @abstractmethod
    def edges(self) -> Iterator["Edge"]:
        pass

    @abstractmethod
    def add_edge(self, node: "Node", value: U) -> "Edge":
        """从当前节点添加一条有向边到 node"""
        pass

    @abstractmethod
    def destroy(self):
        """从图上删除当前节点"""
        pass


class Edge(Generic[U]):
    """图的边类，归属于某个图"""

    @abstractmethod
    def __init__(self, from_node: Node, to_node: Node, value: U = None):
        pass
    @abstractmethod
    def __repr__(self):
        pass

    @property
    @abstractmethod
    def value(self) -> U:
        pass

    @property
    @abstractmethod
    def from_node(self) -> Node:
        pass

    @property
    @abstractmethod
    def to_node(self) -> Node:
        pass

    @abstractmethod
    def destroy(self):
        """从图上删除当前边"""
        pass

class Graph(ABC, Generic[T, U]):
    """图类，包含节点和边"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def add_node(self, value: T) -> Node:
        pass

    @abstractmethod
    def get_nodes(self, value: T) -> Iterator[Node]:
        """根据value查找节点，使用=运算法"""
        pass

    @abstractmethod
    def get_edges(self, value: U) -> Iterator[Edge]:
        """根据from_node和to_node查找边，使用=运算法"""
        pass

