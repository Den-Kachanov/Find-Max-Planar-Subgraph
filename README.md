# Find-Max-Planar-Subgraph

An algorithmic tool for computing the maximum planar subgraph of an arbitrary undirected graph. ...

## Project description

A maximum planar subgraph is a subgraph that:
- is planar (can be drawn in the plane without edge crossings),
- contains the maximum possible number of edges among all planar subgraphs of the original graph,
- is NP-hard to compute in the general case.

*Used Algorithm???*

## Features

- Loading graphs from `.csv`
...

## Technologies used

- Python 3.11.3
...

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Den-Kachanov/Find-Max-Planar-Subgraph
```

2. Change directory:

```bash
cd Find-Max-Planar-Subgraph
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. How to use

```python
"""
Reading graph from the file.
Finding maximal planar graph.
Write it to the file
"""
from algorithm.maximal_planar_subgraph import find_maximal_planar_subgraph
from io.read_graph import read_graph
from io.write_graph import write_graph

# reading the graph
graph = read_graph("example.csv")
max_graph = find_maximal_planar_subgraph(graph)
write_graph(max_graph, "example_maximal_planar_graph.csv")
```

## Project structure

Find-Max-Planar-Subgraph/

│

├── algorithms/

│   ├── maximal_planar_subgraph.py

│   └── decompose_planar_subgraph.py

│

├── io/

│   ├── read_graph.py

│   └── write_graph.py

├── tests/

│   ├── test_maximal_subgraph.py

│   ├── test_planarity.py

│   └── test_read_write.py

│

├── main.py

├── requirements.txt

├── README.md

└── LICENSE

