# Find-Max-Planar-Subgraph

An algorithmic tool for computing the maximum planar subgraph of an arbitrary undirected graph.

## Project description

A maximum planar subgraph is a subgraph that:
- is planar (can be drawn in the plane without edge crossings),
- contains the maximum possible number of edges among all planar subgraphs of the original graph,
- is NP-hard to compute in the general case.

## Algorithms implented

* Kuratowski's theorem
* Wagner's theorem

## Features

- Loading graphs from `.csv`
- Writing graphs to `.csv`

## Technologies used

- Python 3.11.3

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
from algorithm.tools import find_maximal_planar_subgraph
from graph_rw.read_graph import read_graph_from_csv
from graph_rw.write_graph import write_graph_to_csv

# reading the graph
graph = read_graph_from_csv("example.csv")
max_graph = find_maximal_planar_subgraph(graph)
write_graph_to_csv(max_graph, "example_maximal_planar_graph.csv")
```

## Project structure<br>
Find-Max-Planar-Subgraph/<br>
│<br>
├── algorithms/<br>
│   └── tools.py<br>
│<br>
├── graph_rw/<br>
│   ├── read_graph.py<br>
│   └── write_graph.py<br>
│<br>
├── main.py<br>
├── requirements.txt<br>
├── README.md<br>
└── LICENSE<br>

## Team
**[Denys Kachanov](https://github.com/Den-Kachanov)**

**[Solomiia Leshchuk](https://github.com/solosun0308-stack)**

**[Solomiya Lesivtsiv](https://github.com/Solomiya-Lesivtsiv)**

**[Olesia Shlapak](https://github.com/shlapakolesia)**

**[Kateryna Zinchuk](https://github.com/Kateryna-zin)**
