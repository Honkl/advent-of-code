import time
from typing import List

import networkx


def build(nodes: List[List[str]]) -> networkx.Graph:
    graph_nodes = []
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):

            symbol = nodes[i][j]
            if symbol in [".", ">", "<", "^", "v"]:
                name = f"{i}-{j}"
                graph_nodes.append(name)

    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            symbol = nodes[i][j]
            node = f"{i}-{j}"
            if symbol in [".", ">", "<", "^", "v"]:
                neighbours = [f"{i + 1}-{j}", f"{i - 1}-{j}", f"{i}-{j + 1}", f"{i}-{j - 1}"]
                for n in neighbours:
                    e = tuple(sorted([node, n]))
                    if n in graph_nodes and e not in edges:
                        edges.append(e)

    g = networkx.Graph()
    g.add_nodes_from(graph_nodes)
    for e in edges:
        g.add_edge(e[0], e[1], weight=1)

    # Optimize graph to remove 2-edge nodes, not the cleanest, but it'll do
    change = True
    while change:
        # print(g)
        change = False
        for n in g.nodes:
            connected_edges = [e for e in g.edges if n in e]
            if len(connected_edges) == 2:
                n1 = connected_edges[0][0] if connected_edges[0][1] == n else connected_edges[0][1]
                n2 = connected_edges[1][0] if connected_edges[1][1] == n else connected_edges[1][1]
                w1 = g.get_edge_data(*connected_edges[0])["weight"]
                w2 = g.get_edge_data(*connected_edges[1])["weight"]
                g.add_edge(n1, n2, weight=w1 + w2)
                g.remove_node(n)
                change = True
                break

    return g


if __name__ == '__main__':
    start = time.time()

    with open("input.txt", "r") as f:
        data = [list(line.strip()) for line in f]

    start_i = 0
    start_j = 1
    final_i = len(data) - 1
    final_j = len(data[-1]) - 2
    print(f"Starting position: {final_i, final_j, data[final_i][final_j]}")

    g = build(data)
    print(g)

    paths = networkx.all_simple_edge_paths(g, f"{start_i}-{start_j}", f"{final_i}-{final_j}")

    max_path = 0
    for p in paths:
        total_weight = sum(g.get_edge_data(*e)["weight"] for e in p)
        if total_weight > max_path:
            max_path = total_weight

    print(f"Max path: {max_path}")
    print(f"Runtime: {time.time() - start}")
