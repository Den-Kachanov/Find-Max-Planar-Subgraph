"""
Module contains functions to read graphs from
`.csv` or `.dot` files
"""

import re


def read_graph_from_dot(filename: str) -> tuple[dict[int, set[int]], bool]:
    """
    Reads graph from .dot file

    Args:
        filename (str): File name or path to the file

    Returns:
        tuple[dict[int, set[int]], bool]:
            First element is the graph
            Second element states the type of graph: True - directed, False - undirected

    """
    graph = {}
    is_directed = False

    with open(filename, 'r', encoding='UTF-8') as file:
        content = file.read()

        if 'digraph' in content:
            is_directed = True
            edge_pattern = r'(\d+)\s*->\s*(\d+)'
        else:
            is_directed = False
            edge_pattern = r'(\d+)\s*--\s*(\d+)'

        edges = re.findall(edge_pattern, content)

        for v1, v2 in edges:
            v1, v2 = int(v1), int(v2)

            if is_directed:
                if v1 not in graph:
                    graph[v1] = set()
                graph[v1].add(v2)

            else:
                if v1 not in graph:
                    graph[v1] = set()
                if v2 not in graph:
                    graph[v2] = set()

                graph[v1].add(v2)
                graph[v2].add(v1)

    return graph, is_directed


def read_graph_from_csv(filename):
    """
    Reads graph from .csv file

    Args:
        filename (str): File name or path to the file

    Returns:
        tuple[dict[int, set[int]], bool]:
            First element is the graph
            Second element states the type of graph: True - directed, False - undirected


    """
    graph = {}
    edges = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 2:
                continue

            v1, v2 = map(int, parts)
            edges.append((v1, v2))

    is_directed = False
    for v1, v2 in edges:
        if (v2, v1) not in edges:
            is_directed = True
            break

    for v1, v2 in edges:
        if v1 not in graph:
            graph[v1] = set()
        graph[v1].add(v2)

        if not is_directed:
            if v2 not in graph:
                graph[v2] = set()
            graph[v2].add(v1)

    return graph, is_directed
