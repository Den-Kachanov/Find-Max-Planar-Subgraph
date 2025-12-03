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
from algorithm.maximal_planar_subgraph import find_maximal_planar_subgraph
from io.read_graph import read_graph
from io.write_graph import write_graph

# reading the graph
graph = read_graph("example.csv")
max_graph = find_maximal_planar_subgraph(graph)
write_graph(max_graph, "example_maximal_planar_graph.csv")
```

## Project structure<br>
Find-Max-Planar-Subgraph/<br>
│<br>
├── algorithms/<br>
│   ├── maximal_planar_subgraph.py<br>
│   └── decompose_planar_subgraph.py<br>
│<br>
├── io/<br>
│   ├── read_graph.py<br>
│   └── write_graph.py<br>
├── tests/<br>
│   ├── test_maximal_subgraph.py<br>
│   ├── test_planarity.py<br>
│   └── test_read_write.py<br>
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
