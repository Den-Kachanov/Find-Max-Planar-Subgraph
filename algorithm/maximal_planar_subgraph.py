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
