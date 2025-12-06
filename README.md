# Find-Max-Planar-Subgraph

An algorithmic tool for computing the maximum planar subgraph of an arbitrary undirected graph.

## Project description

A maximum planar subgraph is a subgraph that:
- is planar (can be drawn in the plane without edge crossings),
- contains the maximum possible number of edges among all planar subgraphs of the original graph,
- is NP-hard to compute in the general case.

## Algorithms implented

* DFS with backtracking
* Branch-and-bound
* Kuratowski's theorem

## Time complexity

Worst case: O(2^E)

## Features

- Loading graphs from `.csv` and `.dot`
- Creating picture of the graph (.png)
- Converting between`.csv` and `.dot`

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

Using cli:

* For .dot files:
```bash
python3 main.py compute example.dot result.dot
python3 main.py picture result.dot result.png
```

* For .csv files:
```bash
python3 main.py compute example.csv result.dot --csv
python3 main.py picture result.dot result.png
```

* Through python:

```python
"""
Reading graph from the file.
Finding maximal planar graph.
Write it to the file
"""
from Find_Max_Planar_Subgraph.algorithm import tools
from Find_Max_Planar_Subgraph.graph_rw import read_graph, write_graph

# reading the graph
graph, is_directed = read_graph.read_graph_from_csv("example.dot")
print(f"{graph=}")
planar = tools.maximum_planar_subgraph(graph)
print(f"{planar=}")
write_graph.write_graph_to_csv(planar, "example_planar.dot")
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
