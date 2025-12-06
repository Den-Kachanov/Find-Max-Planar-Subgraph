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
    Call `maximum_planar_subgraph(G)` where `G` is an adjacency dictionary.
    The function returns a new adjacency dictionary containing only the edges
    of the maximum planar subgraph.

Example:
    result = maximum_planar_subgraph(G)
"""

from itertools import combinations

# tests


def is_complete(graph: dict[int, set[int]], nodes: list[int]) -> bool:
    """
    Check if the given subset of nodes forms a complete graph.

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.
        nodes (list[int]): Subset of nodes to check.

    Returns:
        bool: True if every pair of nodes in `nodes` is connected by an edge.
    """
    for u, v in combinations(nodes, 2):
        if not has_node(graph, u, v):
            return False
    return True


def is_K5(graph: dict[int, set[int]]) -> bool:
    """
    Check if the graph contains a K5 subgraph (complete graph on 5 nodes).

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.

    Returns:
        bool: True if a K5 subgraph exists, False otherwise.
    """
    vertices = list(graph.keys())

    # all combinations
    for nodes in combinations(vertices, 5):
        # contains K5 -> True
        if is_complete(graph, nodes):
            return True

    return False


def is_biclique(graph: dict[int, set[int]], A: list[int], B: list[int]) -> bool:
    """
    Check if the sets of nodes A and B form a complete bipartite subgraph.

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.
        A (list[int]): First partition of nodes.
        B (list[int]): Second partition of nodes.

    Returns:
        bool: True if every node in A is connected to every node in B.
    """
    # Going through all u-v
    for u in A:
        for v in B:
            # if mismatch -> False
            if not has_node(graph, u, v):
                return False

    return True


def is_K33(graph: dict[int, set[int]]) -> bool:
    """
    Check if the graph contains a K3,3 subgraph (complete bipartite graph
    with partitions of size 3).

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.

    Returns:
        bool: True if a K3,3 subgraph exists, False otherwise.
    """
    vertices = list(graph.keys())

    # all combinations
    for nodes in combinations(vertices, 6):
        # try all ways to split 6 nodes into 2 groups of 3
        for A in combinations(nodes, 3):
            B = tuple(sorted(set(nodes) - set(A)))
            # if makes biclique -> contains K3
            if is_biclique(graph, A, B):
                return True

    return False


def is_planar(graph: dict[int, set[int]]) -> bool:
    """
    Check if a graph is planar using Kuratowski's theorem.

    The graph is non-planar if it contains either K5 or K3,3 as a subgraph.

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.

    Returns:
        bool: True if the graph is planar, False otherwise.
    """
    return not (is_K5(graph) or is_K33(graph))

# graph manipulations


def add_node(graph: dict[int, set[int]], u: int, v: int):
    """
    Add a node between nodes `u`-`v` in the undirected `graph`.

    Args:
        G (dict[int, set[int]]): Graph represented as an adjacency dictionary.
        u (int): One endpoint of the node.
        v (int): The other endpoint of the node.

    Returns:
        None.
        Modifies G in place.
    """
    graph[u].add(v)
    graph[v].add(u)


def remove_node(graph: dict[int, set[int]], u: int, v: int):
    """Remove node from the graph.

    Remove node `u`--`v` from graph G.

    Args:
        G (dict[int, set[int]]): Graph represented as an adjacency dictionary.
        u (int): One endpoint of the node.
        v (int): The other endpoint of the node.

    Returns:
        None.
        Modifies G in place.
    """
    graph[u].remove(v)
    graph[v].remove(u)


def has_node(graph: dict[int, set[int]], u: int, v: int) -> bool:
    """
    Check whether the node exists in a graph.

    Args:
        G (dict[int, set[int]]): Graph represented as an adjacency dictionary.
        u (int): One endpoint of the edge.
        v (int): The other endpoint of the edge.

    Returns:
        bool: True if the edge (u, v) exists, False otherwise.
    """
    return v in graph.get(u, set())


def get_nodes(graph: dict[int, set[int]]):
    """
    Return a list of all edges in the graph in canonical form (u < v).

    Args:
        graph (dict[int, set[int]]): Graph represented as an adjacency dictionary.

    Returns:
        list[tuple[int, int]]: List of nodes as tuples (u, v) with u < v.
    """
    result = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                result.append((u, v))
    return result


# DFS
def dfs(
        graph: dict[int, set[int]],
        all_edges: list[tuple[int]],
        index: int,
        current: list[int],
        subgraph: dict[str, list[int]]):
    """Dfs algorithm.

    This function performs backtracking over all edges of the input graph.

    At each step it tries two possibilities:
        1. Include the current edge (and keep it only if the graph stays planar).
        2. Exclude the current edge.

    The best solution (maximum number of edges that keep the graph planar)
    is stored inside `subgraph["edges"]`.

    The `graph` is modified temporarily during the search and
    restored via backtracking.

    Args:

        graph (dict[int, set[int]]):
            The working graph (adjacency dictionary) modified during DFS.

        all_edges (list[tuple[int, int]]):
            List of all edges of the original graph.
            DFS iterates through this list deciding
            to include/exclude each edge.

        index (int):
            Current position in `all_edges` indicating which edge we are
            deciding on.

        current (list[tuple[int, int]]):
            The list of edges included so far in the current candidate
            planar subgraph.

        subgraph (dict[str, list[tuple[int, int]]]):
            A dictionary holding the best planar edge set found so far.
            Expected format: {"edges": [...]}.

    Returns:
        None
        The function updates `subgraph["edges"]` in place.
    """
    subgraph_list = subgraph["edges"]

    # branch & bound:
    #   subgraph_list cannot exceed current solution
    #   even if all remaining edges are added

    # remaining edges
    left = len(all_edges) - index

    # check branch & bound logic
    if len(current) + left <= len(subgraph_list):
        return

    # if all edges iterated -> update edges if needed
    if index == len(all_edges):

        # end of the function
        # better than the one before -> save it
        if len(current) > len(subgraph_list):
            subgraph["edges"] = current.copy()

        return

    # try adding the node
    u, v = all_edges[index]
    add_node(graph, u, v)

    # check whether graph is planar
    if is_planar(graph):
        # add
        current.append((u, v))
        # recursive
        dfs(graph, all_edges, index + 1, current, subgraph)
        # remove
        current.pop()

    # remove node
    remove_node(graph, u, v)

    # go for another
    dfs(graph, all_edges, index + 1, current, subgraph)


def maximum_planar_subgraph(graph: dict[int, set[int]]) -> dict[int, set[int]]:
    """Find maximum planar subgraph of a graph.

    This function creates a deep copy of the input graph, enumerates all
    edges, and uses a DFS-based backtracking search to select the largest
    set of edges that keeps the graph planar.

    Args:
        graph (dict[int, set[int]]):
            The input graph represented as an adjacency dictionary.

    Returns:
        dict[int, set[int]]:
            A new adjacency dictionary representing the
            maximum planar subgraph of the input graph.
    """
    # deep copy of the graph
    graph_copy = {u: set(vs) for u, vs in graph.items()}

    # all possible edges from original graph
    all_edges = get_nodes(graph_copy)

    # starting point
    # dfs is destructive function
    # changes planar["edges"]
    planar = {"edges": []}
    dfs(graph_copy, all_edges, 0, [], planar)

    # build the planar graph
    result = {u: set() for u in graph}

    for u, v in planar["edges"]:
        result[u].add(v)
        result[v].add(u)

    # return the subgraph
    return result
