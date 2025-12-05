import networkx as nx
import matplotlib.pyplot as plt

# Dataset: https://snap.stanford.edu/data/ego-Facebook.html

# --- CONFIGURATION ---
FILENAME = "facebook_combined.txt"
SHOW_NEIGHBORS = True
MAX_NEIGHBORS = 20
NODE_START = 0
NODE_END = 4038


def load_graph(filepath: str) -> nx.Graph:
    """Loads a graph from a text file containing an edge list.

    Args:
        filepath: The path to the edge list file (e.g., 'facebook_combined.txt').

    Returns:
        A NetworkX Graph object containing the nodes and edges from the file.
    """
    return nx.read_edgelist(filepath, create_using=nx.Graph(), nodetype=int)


def get_path_subgraph(
    graph: nx.Graph,
    path: list[int],
    show_neighbors: bool = True,
    max_neighbors: int = 20,
) -> nx.Graph:
    """Creates a subgraph containing the shortest path and optional immediate neighbors.

    This function isolates the relevant nodes to keep the visualization readable.

    Args:
        graph: The full NetworkX graph.
        path: A list of node IDs representing the shortest path.
        show_neighbors: If True, includes neighbors of the path nodes in the subgraph.
        max_neighbors: Maximum number of neighbors to include per node.

    Returns:
        A NetworkX SubGraph containing the selected nodes and edges.
    """
    nodes_to_draw = set(path)

    if show_neighbors:
        for node in path:
            neighbors = list(graph.neighbors(node))
            nodes_to_draw.update(neighbors[:max_neighbors])

    return graph.subgraph(nodes_to_draw)


def draw_network(
    subgraph: nx.Graph, path: list[int], title: str = "Network Visualization"
) -> None:
    """Visualizes the subgraph using Matplotlib, highlighting the shortest path.

    Nodes and edges belonging to the shortest path are colored red and enlarged.
    Context nodes (neighbors) are colored gray and kept smaller.

    Args:
        subgraph: The graph subset to visualize.
        path: A list of node IDs representing the main path to highlight.
        title: The title of the plot.
    """
    node_colors = []
    node_sizes = []

    for node in subgraph.nodes():
        if node in path:
            node_colors.append("red")
            node_sizes.append(300)
        else:
            node_colors.append("lightgray")
            node_sizes.append(50)

    path_edges = list(zip(path, path[1:]))
    edge_colors = []
    edge_widths = []

    for u, v in subgraph.edges():
        if (u, v) in path_edges or (v, u) in path_edges:
            edge_colors.append("red")
            edge_widths.append(2.0)
        else:
            edge_colors.append("#e0e0e0")
            edge_widths.append(0.5)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(subgraph, k=0.5, seed=42)

    nx.draw_networkx_edges(
        subgraph, pos, edge_color=edge_colors, width=edge_widths, alpha=0.7
    )
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_sizes)

    labels = {node: str(node) for node in path}
    nx.draw_networkx_labels(
        subgraph, pos, labels=labels, font_size=10, font_weight="bold"
    )

    plt.title(title)
    plt.axis("off")
    plt.show()


def main() -> None:
    try:
        G = load_graph(FILENAME)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {FILENAME}")
        return

    try:
        print(f"Szukanie najkrótszej ścieżki między {NODE_START} a {NODE_END}...")
        path = nx.shortest_path(G, source=NODE_START, target=NODE_END)
        print(f"Znaleziono ścieżkę! Długość (liczba krawędzi): {len(path)-1}")
    except nx.NetworkXNoPath:
        print("Nie istnieje żadna ścieżka między wybranymi węzłami.")
        return
    except nx.NodeNotFound:
        print("Jeden z wybranych węzłów nie istnieje w grafie.")
        return

    subgraph = get_path_subgraph(
        G, path, show_neighbors=SHOW_NEIGHBORS, max_neighbors=MAX_NEIGHBORS
    )
    draw_network(
        subgraph, path, title=f"Najkrótsza ścieżka: {NODE_START} -> {NODE_END}"
    )


if __name__ == "__main__":
    main()
