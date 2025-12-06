"""
Cli for the project.

How to run:
```
python3 main.py show graph.dot
```
"""

import argparse

import matplotlib.pyplot as plt
import networkx as nx
from algorithm import tools
from graph_rw import read_graph, write_graph
from networkx.drawing.nx_pydot import graphviz_layout


def load_graph(file: str):
    """Load_graph loads file as a graph.

    Loads .dot file as a graph

    Args:
        file (str): Path to file

    Returns:
        [type]: [description]
    """
    # Reads a .dot file and returns a NetworkX graph
    try:
        return nx.drawing.nx_pydot.read_dot(file)
    except FileNotFoundError:
        print(f"Cannot find {file}")
        exit(1)


def save_graph_picture(G, file):
    """save_graph_picture.

    Saves graph to picture

    Args:
        G: graph
        file (str): Where to save
    """
    pos = graphviz_layout(G, prog="dot")

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue")

    try:
        plt.savefig(file, dpi=150, bbox_inches="tight")
    except PermissionError:
        print(f"Do not have permission to write {file}")
    plt.close()


def main():
    """Run file.

    Main functionality of the module

    """
    parser = argparse.ArgumentParser(prog="Find maximum planar subgraph")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # compute
    compute_parser = subparsers.add_parser("compute")
    compute_parser.add_argument("graph_file", help="File that contain graph")
    compute_parser.add_argument("output_graph_file", help="File to write the maximum planar subgraph")
    compute_parser.add_argument("--csv", action="store_true", help="Specify that input is from .csv file")

    # show
    show_parser = subparsers.add_parser("picture", help="Create a picture of the graph (matplotlib + networkx)")
    show_parser.add_argument("dot_file", help="The dot file that contains graph")
    show_parser.add_argument("png_file", help="File to save to the picture")

    # convert
    to_dot_parser = subparsers.add_parser("to_dot", help="From .csv to .dot")
    to_csv_parser = subparsers.add_parser("to_csv", help="From .dot to .csv")

    args = parser.parse_args()

    if args.command == "compute":
        try:
            if args.csv:
                graph, _ = read_graph.read_graph_from_csv(args.graph_file)

            else:
                graph, _ = read_graph.read_graph_from_dot(args.graph_file)

        except FileNotFoundError:
            print(f"Cannot find {args.graph_file}")
            exit(1)

        planar_subgraph = tools.maximum_planar_subgraph(graph)
        try:
            write_graph.write_graph_to_dot(planar_subgraph, args.output_graph_file)
        except PermissionError:
            print(f"Do not have permission to write {args.output_graph_file}")

    elif args.command == "picture":
        G = load_graph(args.dot_file)
        save_graph_picture(G, args.png_file)

    elif args.command == "to_dot":
        ...
    elif args.command == "to_csv":
        ...


if __name__ == "__main__":
    main()
