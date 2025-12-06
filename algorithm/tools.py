"""
tools.py
========

This module provides utilities for computing a maximum planar subgraph
of an undirected graph.

Implemented:
    A depth-first search (DFS)–based backtracking algorithm for selecting the
    largest subset of edges that keeps the graph planar.

    Algorithm:

       DFS explores all combinations of including or excluding edges.
       At each step, the algorithm:
        1 Tries adding an edge.
        2 Checks planarity.
        3 Backtracks if necessary.
       The best (largest) planar edge set found is rebuilt into a graph
       structure.

Graph representation:
    Graphs are represented as adjacency dictionaries:
      {
        node1: {neighbor1, neighbor2, ...},
        node2: { ... },
        ...
      }

    Edges are stored as tuples (u, v).

Usage:
    Call `maximum_planar_subgraph(Graph)` where `Graph` is an adjacency dictionary.
    The function returns a new adjacency dictionary containing only the edges
    of the maximum planar subgraph.

Example:
    result = maximum_planar_subgraph(G)
"""

import networkx as nx


def add_edge(graph: dict[int, set[int]], u: int, v: int):
    graph[u].add(v)
    graph[v].add(u)


def remove_edge(graph: dict[int, set[int]], u: int, v: int):
    graph[u].remove(v)
    graph[v].remove(u)


def get_edges(graph: dict[int, set[int]]):
    """Return a list of all edges in the graph as tuples (u, v).

    Args:
        graph (dict[int, set[int]]): Adjacency dictionary.

    Returns:
        list[tuple[int,int]]: List of edges.
    """
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    return edges


def is_planar_nx(graph: dict[int, set[int]]) -> bool:
    """Check if a graph is planar using NetworkX.

    Args:
        graph (dict[int, set[int]]): Adjacency dictionary.
    """
    G = nx.Graph()
    for u, nbrs in graph.items():
        for v in nbrs:
            if u < v:
                G.add_edge(u, v)
    planar, _ = nx.check_planarity(G, counterexample=False)
    return planar


def dfs(graph: dict[int, set[int]],
        all_edges: list[tuple[int, int]],
        index: int,
        current: list[tuple[int,int]],
        subgraph: dict[str, list[tuple[int,int]]]):
    """Backtracking DFS to find the largest planar subgraph.

    Args:
        graph: Working adjacency dictionary (modified during DFS)
        all_edges: List of all edges of the original graph
        index: Current edge index in all_edges
        current: Candidate edges in current subgraph
        subgraph: Dictionary storing the best planar edges found {"edges": [...]}

    Updates subgraph["edges"] in place.
    """
    subgraph_list = subgraph["edges"]
    remaining = len(all_edges) - index

    # branch & bound
    if len(current) + remaining <= len(subgraph_list):
        return

    # if the end -> stop
    # if better then the best -> replace
    if index == len(all_edges):
        if len(current) > len(subgraph_list):
            subgraph["edges"] = current.copy()
        return

    u, v = all_edges[index]

    add_edge(graph, u, v)

    if is_planar_nx(graph):
        current.append((u, v))
        dfs(graph, all_edges, index + 1, current, subgraph)
        current.pop()

    remove_edge(graph, u, v)

    dfs(graph, all_edges, index + 1, current, subgraph)


def maximum_planar_subgraph(graph: dict[int, set[int]]) -> dict[int, set[int]]:
    """Compute the maximum planar subgraph of an undirected graph.

    This function performs a DFS-based backtracking algorithm to select
    the largest subset of edges such that the resulting graph remains planar.
    It returns a new adjacency dictionary containing only the edges
    of the maximum planar subgraph.

    Args:
        graph (dict[int, set[int]]): undirected graph as an adjacency dictionary.

    Returns:
        dict[int, set[int]]: Maximum planar subgraph.
    """
    graph_copy = {u: set() for u in graph}
    all_edges = get_edges(graph)

    planar = {"edges": []}
    dfs(graph_copy, all_edges, 0, [], planar)

    # build result
    result = {u: set() for u in graph}
    for u, v in planar["edges"]:
        result[u].add(v)
        result[v].add(u)

    return result
