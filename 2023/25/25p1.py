import time

import networkx

if __name__ == '__main__':
    start = time.time()

    g = networkx.Graph()

    with open("input.txt", "r") as f:
        for line in f:
            source, destinations = line.split(":")
            destinations = [x.strip() for x in destinations.strip().split(" ")]

            for v in [source] + destinations:
                if v not in g.nodes:
                    g.add_node(v)

            for d in destinations:
                g.add_edge(source, d)

    print(g)
    cut = networkx.minimum_edge_cut(g)
    print(cut)

    for e in cut:
        g.remove_edge(e[0], e[1])

    components = list(networkx.connected_components(g))
    assert len(components) == 2, len(components)
    result = len(components[0]) * len(components[1])

    print(result)
    print(time.time() - start)
