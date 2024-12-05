import os

from base_struct.adjacency_list_graph import AdjacencyListGraph
from base_struct.adjacency_matrix_graph import AdjacencyMatrixGraph
from base_struct.algorithm import dijkstra, topo_sort, prim, kruskal
from base_struct.graph import Graph


def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')
def add_node(g:Graph):
    """添加一个节点"""
    val = input("Please input the value of the node:")
    if val == "":
        print("Value cannot be empty")
        return
    if list(g.get_nodes_func(lambda x:x.value == val)):
        print("Node already exists")
        return
    g.add_node(val)

def add_edge(g:Graph):
    """添加一条边"""
    val = input("Please input the value of the edge:")
    node1 = input("Please input the value of the from node:")
    node2 = input("Please input the value of the to node:")
    node1 = list(g.get_nodes_func(lambda x:x.value == node1))
    node2 = list(g.get_nodes_func(lambda x:x.value == node2))
    if not val:
        print("Value cannot be empty")
        return
    if not node1:
        print("From node not found")
        return
    if not node2:
        print("To node not found")
        return
    if node1 and node2:
        node1[0].add_edge(node2[0], int(val))
    else:
        print("Node not found")


def del_node(g: Graph):
    """根据 value 删除节点"""
    val = input("Please input the value of the node:")
    node = list(g.get_nodes_func(lambda x: x.value == val))
    if not node:
        print("Node not found")
        return
    node[0].destroy()


def del_edge(g: Graph):
    """根据 value 删除边"""
    val = input("Please input the value of the edge:")
    node1 = input("Please input the value of the from node:")
    node2 = input("Please input the value of the to node:")
    node1 = list(g.get_nodes_func(lambda x: x.value == node1))
    node2 = list(g.get_nodes_func(lambda x: x.value == node2))
    if not val:
        print("Value cannot be empty")
        return
    if not node1:
        print("From node not found")
        return
    if not node2:
        print("To node not found")
        return
    if node1 and node2:
        for edge in list(node1[0].edges):
            if edge.to_node == node2[0] and edge.value == int(val):
                edge.destroy()
                return
        print("Edge not found")
    else:
        print("Node not found")

def get_edges_by_node(g:Graph):
    """根据节点获取边"""
    val = input("Please input the value of the node:")
    node = list(g.get_nodes_func(lambda x:x.value == val))
    if not node:
        print("Node not found")
        return
    print(f"Edges of node {val}:")
    for edge in node[0].edges:
        print(f" -> {edge.to_node.value} : {edge.value}")

def get_rev_edges_by_node(g:Graph):
    """根据节点获取反向边"""
    val = input("Please input the value of the node:")
    node = list(g.get_nodes_func(lambda x:x.value == val))
    if not node:
        print("Node not found")
        return
    print(f"Reverse edges of node {val}:")
    for edge in node[0].rev_edges:
        print(f" <- {edge.from_node.value} : {edge.value}")

def print_graph(g:Graph):
    """打印图"""
    print("Current graph:")
    nodes = list(g.get_nodes_func(lambda x:x))
    if not nodes:
        print("Empty graph")
        return
    for node in nodes:
        print(f"Node {node.value}:")
        if not list(node.edges):
            print("  No edges")
        for edge in node.edges:
            print(f"  -> {edge.to_node.value} : {edge.value}")

def run_dij(g:Graph):
    """运行Dijkstra算法"""
    start = input("Please input the value of the start node:")
    end = input("Please input the value of the end node:")
    start = list(g.get_nodes_func(lambda x:x.value == start))
    end = list(g.get_nodes_func(lambda x:x.value == end))
    if not start:
        print("Start node not found")
        return
    if not end:
        print("End node not found")
        return
    if start and end:
        dst,path = dijkstra(g, start[0], end[0])
        if dst == -1:
            print("No path found")
            return
        print(f"Shortest distance from {start[0].value} to {end[0].value} is {dst}")
        print("Path:")
        print(" -> ".join([node.value for node in path]))
    else:
        print("Node not found")

def run_topo(g:Graph):
    """运行拓扑排序"""
    ans = topo_sort(g)
    print("Topological order:")
    print(" -> ".join([node.value for node in ans]))


def run_prim(g: Graph):
    """运行Prim算法"""
    new_g = prim(g)
    print("New graph:")
    print_graph(new_g)


def run_kruskal(g: Graph):
    """运行Kruskal算法"""
    new_g = kruskal(g)
    print("New graph:")
    print_graph(new_g)

if __name__ == "__main__":

    impls = [AdjacencyListGraph, AdjacencyMatrixGraph]
    for i, impl in enumerate(impls):
        print(f"{i}: {impl.__name__}")
    idx = input("Please input the index of the implementation you want to test: ")

    if idx not in ["0", "1"]:
        print("Invalid index")
        exit(1)
    g: Graph[str, int] = impls[int(idx)]()

    while True:
        # clear_console()
        print("\n\n\n")
        print_graph(g)
        print()
        method = [add_node, add_edge, del_node, del_edge,get_edges_by_node,get_rev_edges_by_node, run_dij, run_topo, run_prim, run_kruskal]
        for i, m in enumerate(method):
            print(f"{i}: {m.__name__}")
        idx = input("Please input the index of the method you want to test: ")
        if idx not in [str(i) for i in range(len(method))]:
            print("Invalid index")
            continue
        method[int(idx)](g)


