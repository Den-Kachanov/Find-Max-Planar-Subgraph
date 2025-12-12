"""
tools.py
========

This module provides utilities for computing the maximum planar subgraph
of an undirected graph using a DFS-based backtracking algorithm combined
with planarity checks via the LR-algorithm.

Implemented Algorithms:
----------------------

1. Maximum Planar Subgraph (DFS + Planarity)
   ------------------------------------------
   - Performs a depth-first search (DFS) over all subsets of edges.
   - At each step:
        1. Try adding the current edge to the candidate subgraph.
        2. Check if the resulting subgraph is planar using LR-algorithm.
        3. Backtrack if planarity is violated.
   - Keeps track of the largest planar subset of edges found.
   - Returns the adjacency dictionary representing the maximum planar subgraph.

2. Planarity Check (LR-algorithm)
   --------------------------------
   - LR-algorithm is a linear-time algorithm for checking graph planarity.
   - Uses DFS to classify tree and back edges.
   - Maintains 'fringes' (data structures tracking constraints from back edges).
   - Merges and prunes fringes to detect forbidden subdivisions (K5 or K3,3).
   - Returns True if the graph is planar, False otherwise.

3. Fringe and FringeOpposedSubset
   --------------------------------
   - `fringe`: represents a collection of fringe operations during LR-algorithm.
   - `fringe_opposed_subset`: represents opposed edge subsets for LR merges.
   - Fringe operations include merging, pruning, and maintaining left/right constraints.
   - These classes allow efficient management of planar constraints.

4. Utilities
   -----------
   - `add_edge(graph, u, v)`: Adds an edge to an adjacency dictionary.
   - `remove_edge(graph, u, v)`: Removes an edge from an adjacency dictionary.
   - `get_edges(graph)`: Returns a list of all edges as tuples (u, v).
   - `is_planar_lr(graph_dict)`: Converts adjacency dictionary to networkx.Graph and
     uses LR-algorithm to check planarity.

Graph Representation:
--------------------
- Graphs are represented as adjacency dictionaries:
    {
      node1: {neighbor1, neighbor2, ...},
      node2: { ... },
      ...
    }
- Edges are stored as tuples (u, v) for processing.
- Planarity check is performed via the LR-algorithm on a networkx.Graph object.

Usage:
------
result = maximum_planar_subgraph(G)
"""

from collections import defaultdict, deque
from itertools import islice

import networkx as nx


def is_planar(g):
    """
    Check if a NetworkX graph is planar using the LR-algorithm.

    This function performs a planarity check based on depth-first search (DFS)
    combined with the LR-algorithm. It first applies simple planarity rules:
        - Graphs with fewer than 5 nodes or fewer than 9 edges are always planar.
        - Graphs with more than 3*n - 6 edges (where n is the number of nodes)
          are non-planar according to Euler's formula.

    For other cases, it performs a DFS to classify edges into tree and back edges
    and uses the LR-algorithm to track planar constraints with fringes.

    Args:
        g (networkx.Graph): The graph to check for planarity.

    Returns:
        bool: True if the graph is planar, False otherwise.
    """
    if g.size() < 9 or g.order() < 5:
        return True

    # m > 3n - 6
    if g.size() > 3 * g.order() - 6:
        return False

    dfs_heights = defaultdict(lambda: -1)

    for v in g.nodes():
        if dfs_heights[v] < 0:
            dfs_heights[v] = 0

            if not lr_algorithm(g, v, dfs_heights):
                return False

    return True


def lr_algorithm(g, root, dfs_heights):
    """
    Apply the LR-algorithm for planarity testing starting from a root node.

    The LR-algorithm is used to check planarity of a connected component of a graph
    using a depth-first search (DFS) traversal. It tracks tree edges and back edges,
    and maintains "fringes" to represent constraints for embedding the graph in a plane
    without edge crossings.

    Algorithm steps:
        1. Perform DFS from the root node.
        2. Classify edges as tree edges or back edges.
        3. Track fringes of back edges to check if they can be embedded planar.
        4. Merge and prune fringes using LR rules.
        5. If any merge/prune operation fails, the graph is non-planar.

    Args:
        g (networkx.Graph): The graph to check (must be connected).
        root (int): The starting node for DFS.
        dfs_heights (defaultdict): Dictionary mapping node -> DFS height (depth),
                                   initialized with -1 for unvisited nodes.

    Returns:
        bool: True if the component is planar, False if a planarity conflict is found.
    """
    fringes = [[]]
    dfs_stack = [(root, iter(g[root]))]

    while dfs_stack:
        x, children = dfs_stack[-1]

        try:
            y = next(children)

            if dfs_heights[y] < 0:  # tree edge
                fringes.append([])
                dfs_heights[y] = dfs_heights[x] + 1
                dfs_stack.append((y, iter([u for u in g[y] if u != x])))

            else:
                if dfs_heights[x] > dfs_heights[y]:  # back edge
                    fringes[-1].append(fringe(dfs_heights[y]))

        except StopIteration:
            dfs_stack.pop()

            if len(fringes) > 1:
                try:
                    merge_fringes(fringes, dfs_heights[dfs_stack[-1][0]])
                except Exception:
                    return False

    return True


def merge_fringes(fringes, dfs_height):
    """
    Merge the topmost fringe with its parent fringe and prune it according to LR rules.

    In the LR planarity testing algorithm, each node maintains a fringe that represents
    back edges. When DFS finishes exploring a subtree, the fringe of the subtree is
    merged with the fringe of its parent. After merging, the fringe is pruned to remove
    back edges that do not satisfy planarity constraints.

    Args:
        fringes (list[list[fringe]]): A stack of fringe lists for the DFS tree.
        dfs_height (int): The DFS height of the parent node (used for pruning).

    Raises:
        Exception: If the merge or prune operation violates LR constraints (handled outside).

    Side Effects:
        Modifies the `fringes` list in-place, merging and pruning the topmost fringe.
    """

    mf = get_merged_fringe(fringes.pop())

    if mf is not None:
        mf.prune(dfs_height)
        if mf.fops:
            fringes[-1].append(mf)


def get_merged_fringe(upper_fringes):
    """
    Merge a list of fringes into a single fringe according to LR planarity rules.

    In the LR planarity algorithm, multiple fringes may need to be combined when
    backtracking from a DFS subtree. This function sorts the fringes (based on
    their DFS low and high values) and merges them sequentially into one.

    Args:
        upper_fringes (list[fringe]): A list of `fringe` objects to merge.

    Returns:
        fringe | None: The merged fringe if `upper_fringes` is not empty; otherwise None.

    Side Effects:
        The original `upper_fringes` list is not modified; a new merged `fringe` is returned.
    """
    if len(upper_fringes) > 0:
        upper_fringes.sort()
        new_fringe = upper_fringes[0]
        for f in islice(upper_fringes, 1, len(upper_fringes)):
            new_fringe.merge(f)
        return new_fringe

class fringe:
    """
    Represents a fringe used in the LR planarity testing algorithm.

    A fringe tracks sets of edges encountered during a depth-first search (DFS)
    to detect planarity violations. Each fringe contains one or more
    `fringe_opposed_subset` objects stored in a deque (`fops`). 

    The class supports merging fringes, pruning invalid edges, and maintaining
    the LR-algorithm constraints for planarity.

    Attributes:
        fops (deque[fringe_opposed_subset]): A deque of fringe_opposed_subset objects
            representing left/right opposed edge sets for planarity checking.

    Methods:
        __init__(dfs_h=None):
            Initializes a fringe with an optional starting DFS height.
        __lt__(other):
            Compares fringes by DFS low/high values for sorting.
        __repr__():
            Returns a string representation for debugging (with terminal colors).
        merge(other):
            Merges another fringe into this one following LR planarity rules.
        prune(dfs_height):
            Prunes edges violating LR conditions at the specified DFS height.
        _merge_t_alike_edges():
            Merges edges in the fringe that are alike (same side).
        _merge_t_opposite_edges_into(other):
            Merges opposite edges into another fringe according to LR rules.
        _align_duplicates(dfs_h):
            Adjusts edges to avoid duplicate entries when merging fringes.
        _swap_side():
            Swaps left/right sides of the fringe_opposed_subset if needed.
        _make_onion_structure(other):
            Arranges nested edges into an "onion" structure for planarity.
        __lr_condition(dfs_height):
            Checks whether left/right edges violate LR conditions at a given DFS height.
    """

    __slots__ = ['fops']

    def __init__(self, dfs_h=None):
        """
        Initialize a fringe object.

        Args:
            dfs_h (int, optional): The DFS height to initialize the first fringe_opposed_subset.
                                   If None, creates an empty fringe.
        """
        self.fops = deque() if dfs_h is None else deque([fringe_opposed_subset(dfs_h)])

    def __lt__(self, other):
        """
        Compare fringes by their lowest and highest DFS heights for sorting.

        Returns True if this fringe is considered "less than" the other.
        """
        diff = self.L.l_lo - other.L.l_lo
        if diff != 0:
            return diff < 0
        return self.H.l_hi < other.H.l_hi

    @property
    def H(self):
        """Return the first fringe_opposed_subset (highest)."""
        return self.fops[0]

    @property
    def L(self):
        """Return the last fringe_opposed_subset (lowest)."""
        return self.fops[-1]

    def merge(self, other):
        """
        Merge another fringe into this one following LR algorithm rules.

        This involves merging alike edges, merging opposite edges, and
        forming an 'onion' structure to maintain planarity constraints.
        """
        other._merge_t_alike_edges()
        self._merge_t_opposite_edges_into(other)
        if not self.H.right:
            other._align_duplicates(self.L.l_hi)
        else:
            self._make_onion_structure(other)
        if other.H.left:
            self.fops.appendleft(other.H)

    def _merge_t_alike_edges(self):
        """
        Merge alike edges (same side) within the fringe.

        Raises:
            Exception: If the highest subset has right edges (invalid state).
        """
        if self.H.right:
            raise Exception
        for f in islice(self.fops, 1, len(self.fops)):
            if f.right:
                raise Exception
            self.H.left.extend(f.left)
        self.fops = deque([self.fops[0]])

    def _merge_t_opposite_edges_into(self, other):
        """
        Merge opposite edges of this fringe into another fringe.

        Args:
            other (fringe): Target fringe to merge opposite edges into.
        """
        while (not self.H.right and self.H.l_hi > other.H.l_lo):
            other.H.right.extend(self.H.left)
            self.fops.popleft()

    def _align_duplicates(self, dfs_h):
        """
        Align duplicates when merging fringes to avoid repeated edges.

        Args:
            dfs_h (int): DFS height used for detecting duplicates.
        """
        if self.H.l_lo == dfs_h:
            self.H.left.pop()
            self._swap_side()

    def _swap_side(self):
        """
        Swap the left and right sides of the highest fringe_opposed_subset
        if necessary to maintain LR ordering constraints.
        """
        if not self.H.left or (self.H.right and self.H.l_lo > self.H.r_lo):
            self.H.c[0], self.H.c[1] = self.H.c[1], self.H.c[0]

    def _make_onion_structure(self, other):
        """
        Arrange nested edges into an 'onion' structure to preserve planarity.

        Args:
            other (fringe): Fringe being merged that may require nesting.
        
        Raises:
            Exception: If the onion structure cannot be created (planarity violated).
        """
        lo, hi = (0, 1) if self.H.l_hi < self.H.r_hi else (1, 0)
        if other.H.l_lo < self.H.c[lo][0]:
            raise Exception
        elif other.H.l_lo < self.H.c[hi][0]:
            self.H.c[lo].extendleft(reversed(other.H.left))
            self.H.c[hi].extendleft(reversed(other.H.right))
            other.H.left.clear()
            other.H.right.clear()

    def prune(self, dfs_height):
        """
        Remove edges from the fringe that violate LR conditions at a given DFS height.

        Args:
            dfs_height (int): The current DFS height to prune against.
        """

        left_, right_ = self.__lr_condition(dfs_height)
        while self.fops and (left_ or right_):
            if left_:
                self.H.left.popleft()
            if right_:
                self.H.right.popleft()
            if not self.H.left and not self.H.right:
                self.fops.popleft()
            else:
                self._swap_side()
            if self.fops:
                left_, right_ = self.__lr_condition(dfs_height)

    def __lr_condition(self, dfs_height):
        """
        Check whether the highest fringe_opposed_subset has left or right edges
        violating LR conditions at the given DFS height.

        Args:
            dfs_height (int): DFS height to check against.

        Returns:
            tuple(bool, bool): (left_violation, right_violation)
        """
        return (self.H.left and self.H.l_hi >= dfs_height,
                self.H.right and self.H.r_hi >= dfs_height)


# fringe opposed subset

class fringe_opposed_subset:
    """
    Represents a subset of edges in a fringe for the LR planarity algorithm.

    Each subset maintains two opposed sequences of DFS heights:
    - left (c[0]): DFS heights of edges on the left side.
    - right (c[1]): DFS heights of edges on the right side.

    This class is used to track opposed edges during planarity testing
    and supports convenient access to high/low DFS heights.

    Attributes:
        c (list[deque[int]]): List of two deques [left, right] storing DFS heights.
    """

    __slots__ = ['c']

    def __init__(self, h):
        self.c = [deque([h]), deque()]

    @property
    def left(self):
        """
        Get the left sequence of DFS heights.

        Returns:
            deque[int]: DFS heights of left edges.
        """
        return self.c[0]

    @property
    def right(self):
        """
        Get the right sequence of DFS heights.

        Returns:
            deque[int]: DFS heights of right edges.
        """
        return self.c[1]

    @property
    def l_lo(self):
        """
        Get the lowest DFS height on the left side.

        Returns:
            int: The last element of the left deque.
        """
        return self.c[0][-1]

    @property
    def l_hi(self):
        """
        Get the highest DFS height on the left side.

        Returns:
            int: The first element of the left deque.
        """
        return self.c[0][0]

    @property
    def r_lo(self):
        """
        Get the lowest DFS height on the right side.

        Returns:
            int: The last element of the right deque.
        """
        return self.c[1][-1]

    @property
    def r_hi(self):
        """
        Get the highest DFS height on the right side.

        Returns:
            int: The first element of the right deque.
        """
        return self.c[1][0]



def add_edge(graph: dict[int, set[int]], u: int, v: int):
    """adds edge to graph"""
    graph[u].add(v)
    graph[v].add(u)


def remove_edge(graph: dict[int, set[int]], u: int, v: int):
    """removes edge to graph"""
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

def is_planar_lr(graph_dict: dict[int, set[int]]) -> bool:
    """
    Connects adjacency dictionary to LR-algorithm.

    Args:
        graph_dict (dict[int, set[int]]): adjacency dictionary of the graph.

    Returns:
        bool: True if planar, False otherwise.
    """
    G = nx.Graph()
    for u, neighbors in graph_dict.items():
        for v in neighbors:
            if u < v:
                G.add_edge(u, v)
    return is_planar(G)


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

    if is_planar_lr(graph):
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
