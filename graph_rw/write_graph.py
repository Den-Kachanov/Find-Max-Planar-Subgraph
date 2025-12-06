"""
Module contains functions to write graphs to
`.csv` or `.dot` files
"""


def write_graph_to_csv(graph: dict[int, set[int]], filename: str, is_directed: bool = False):
    """
    Writes graph to `.csv` file.

    Args:
        graph (dict[int, set[int]]): The graph to write
        filename (str): File name or path to it
        is_directed (bool): Type of the graph (default: `False`)
    """

    with open(filename, 'w', encoding='utf-8') as file:

        if is_directed:
            for v1, neighbors in sorted(graph.items()):
                for v2 in sorted(neighbors):
                    file.write(f"{v1},{v2}\n")

        else:
            written_edges = set()

            for v1, neighbors in sorted(graph.items()):
                for v2 in sorted(neighbors):
                    edge = tuple(sorted((v1, v2)))

                    if edge not in written_edges:
                        file.write(f"{edge[0]},{edge[1]}\n")
                        written_edges.add(edge)


def write_graph_to_dot(graph: dict[int, set[int]], filename: str, is_directed: bool = False):
    """
    Writes the graph to a `.dot` file.

    Args:
        graph (dict[int, set[int]]): The graph to write.
        filename (str): Path to the output .dot file.
        is_directed (bool): Whether the graph is directed (default: False).
    """
    # Choose graph type: digraph for directed, graph for undirected
    graph_type = "digraph" if is_directed else "graph"
    # Choose edge symbol: -> for directed, -- for undirected
    edge_symbol = "->" if is_directed else "--"

    with open(filename, 'w', encoding='utf-8') as file:
        # Write DOT header
        file.write(f"{graph_type} planar {{\n")

        if is_directed:
            for u, neighbors in sorted(graph.items()):
                for v in sorted(neighbors):
                    file.write(f"    {u} {edge_symbol} {v};\n")

        else:
            written_edges = set()
            for u, neighbors in sorted(graph.items()):
                for v in sorted(neighbors):
                    edge = tuple(sorted((u, v)))
                    if edge not in written_edges:
                        file.write(f"    {edge[0]} {edge_symbol} {edge[1]};\n")
                        written_edges.add(edge)

        # Close DOT graph
        file.write("}\n")
