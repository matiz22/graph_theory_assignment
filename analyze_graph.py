import networkx as nx
import matplotlib.pyplot as plt
import statistics

# Dataset: https://snap.stanford.edu/data/ego-Facebook.html

# --- CONFIGURATION ---
FILENAME = "facebook_combined.txt"


def load_graph(filepath: str) -> nx.Graph:
    """Loads a graph from a text file containing an edge list.

    Args:
        filepath: The path to the edge list file.

    Returns:
        A NetworkX Graph object.
    """
    print(f"Wczytywanie danych z pliku {filepath}...")
    return nx.read_edgelist(filepath, create_using=nx.Graph(), nodetype=int)


def get_and_print_stats(graph: nx.Graph) -> tuple[list[int], float, float]:
    """Calculates, prints basic properties, and returns stats for plotting.

    Args:
        graph: The NetworkX graph to analyze.

    Returns:
        A tuple containing:
        - List of degrees (int)
        - Average degree (float)
        - Median degree (float)
    """
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    density = nx.density(graph)

    degrees = [deg for node, deg in graph.degree()]

    avg_degree = statistics.mean(degrees)
    median_degree = statistics.median(degrees)
    max_degree = max(degrees)

    print("\n--- DANE O GRAFIE ---")
    print(f"Liczba węzłów: {num_nodes}")
    print(f"Liczba krawędzi: {num_edges}")
    print(f"Gęstość grafu: {density:.4f}")
    print(f"Średnia liczba znajomych: {avg_degree:.2f}")
    print(f"Mediana liczby znajomych: {median_degree}")
    print(f"Maksymalna liczba znajomych: {max_degree}")
    print("--------------------------------------\n")

    return degrees, avg_degree, median_degree


def plot_degree_distribution(
    degrees: list[int], avg_degree: float, median_degree: float
) -> None:
    """Plots the degree distribution histogram using pre-calculated stats.

    Args:
        degrees: A list of integer degrees for all nodes.
        avg_degree: Pre-calculated average degree.
        median_degree: Pre-calculated median degree.
    """
    max_degree = max(degrees)

    plt.figure(figsize=(10, 6))

    plt.hist(
        degrees, bins=40, range=(0, 200), color="skyblue", edgecolor="black", alpha=0.7
    )

    plt.axvline(
        avg_degree,
        color="red",
        linestyle="dashed",
        linewidth=2,
        label=f"Średnia: {avg_degree:.1f}",
    )
    plt.axvline(
        median_degree,
        color="green",
        linestyle="dashed",
        linewidth=2,
        label=f"Mediana: {median_degree}",
    )

    plt.title("Rozkład liczby znajomych (Zbliżenie na zakres 0-200)")
    plt.xlabel("Liczba znajomych")
    plt.ylabel("Liczba osób")
    plt.legend()
    plt.grid(axis="y", alpha=0.5)

    plt.text(
        x=150,
        y=100,
        s=f"Wykres ucięty.\nMax liczba znajomych: {max_degree}",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    plt.show()


def main() -> None:
    try:
        G = load_graph(FILENAME)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {FILENAME}")
        return

    degrees, avg_degree, median_degree = get_and_print_stats(G)
    plot_degree_distribution(degrees, avg_degree, median_degree)


if __name__ == "__main__":
    main()
