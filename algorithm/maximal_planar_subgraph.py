"""
Contains algroithm for finding maximal planar graph
"""


def tree_of_undir_graph(graph: dict[int, set[int]]) -> dict[int, set[int]] | None:
    """
    Creates a tree of an undirected graph

    Args:
        graph (dict[int, set[int]]): The graph

    Returns:
        dict[int, set[int]]: The tree of the graph
    """

    # check whether graph is in needed format

    if not isinstance(graph, dict):
        return None

    for key, value in graph.items():
        if not (isinstance(key, int) and
                isinstance(value, set) and
                all(isinstance(v, int) for v in value)):
            return None

    # visited vertices
    visited = set()
    # skeleton
    skeleton = {node: set() for node in graph}

    # pick arbitrary start node
    start = list(skeleton.keys())[0]

    # using stack method
    stack = [start]
    visited.add(start)

    # while stack is not empty
    while stack:
        # poping element from the stack
        u = stack.pop()

        # going through each element connected with vertice
        for v in graph[u]:

            # if covered before -> skip
            if v not in visited:
                # marked as visited
                visited.add(v)

                # add edge u-v
                skeleton[u].add(v)
                skeleton[v].add(u)

                # appending to the stack
                stack.append(v)

    return skeleton

def

def check_planarity(graph: dict[int, set[int]]) -> bool:
    """
    Checks whether graph is planar

    Args:
        graph (dict[int, set[int]]): The graph to check

    Returns:
        bool: planarity
    """
    {
        1: {2, 3, 4},
        2: {1, 4},
        3: {1},
        4: {1, 2}
    }

    graph_copy = {v: n.copy() for v, n in graph.items()}

    # going through graph
    for vertice, nodes in graph_copy.items():
        # if vertice does not have 2 nodes => cannot subdivide
        if len(nodes) <= 1:
            continue

        for second_nodes in nodes:
            if vertice in second_nodes and len(second_nodes) != 1:
                subdivide_graph(graph_copy, vertice)


def remove_subdivision(graph: dict[int, set[int]], vertice: int):
    """
    'Removes' subdivision in graph by a vertice

    Example:
    ```
    1 --- 2   -2       1
    |     |   ==>    /   \\
    4 --- 3         4 --- 3
    ```

    Args:
        graph (dict[int, set[int]]): Graph
        vertice (int): Vertice
    """
    if vertice not in graph:
        return None
    neighbors = graph[vertice]
    if len(neighbors) != 2:
        return
    neighbor_list = list(neighbors)
    u, v = neighbor_list[0], neighbor_list[1]
    # Delete node from graph
    del graph[vertice]
    # Delete node from its neighbors
    if u in graph:
        graph[u].discard(vertice)
    if v in graph:
        graph[v].discard(vertice)
    # Add edge between neighbors (if they are not loop)
    if u != v and u in graph and v in graph:
        graph[u].add(v)
        graph[v].add(u)
