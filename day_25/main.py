import networkx as nx

def parse_input(filename):
    with open(filename) as f:
        graph = nx.Graph()
        for l in f:
            node, edges = l.strip().split(": ")
            for edge in edges.split():
                graph.add_edge(node, edge)
    return graph

def part_one(graph):
    cuts = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(cuts)
    clusters = nx.connected_components(graph)
    cl = list(clusters)
    return len(cl[0]) * len(cl[1])

if __name__ == "__main__":
    input_path = "./day_25/input.txt"
    graph = parse_input(input_path)
    print("---Part One---")
    print(part_one(graph))