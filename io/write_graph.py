"""
Module contains functions to write graphs to
`.csv` or `.dot` files
"""


def write_graph_to_csv(graph: dict[int, set[int]], filename: str, is_directed: bool = False):
    """
    Writes graph to `.csv` file

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
