#!/usr/bin/env python3
import networkx as nx
import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    G = nx.DiGraph()
    weights = np.asarray([[int(v) for v in ln] for ln in lines], dtype=np.int64)
    n_rows, n_cols = weights.shape

    # Each node in the graph is the row, column and entry direction (LRTB)
    for r in range(n_rows):
        for c in range(n_cols):
            for d in "LRTB":
                G.add_node((r, c, d))

    # Consider each *destination* node
    for r in range(n_rows):
        for c in range(n_cols):
            # from top
            weight = 0
            for dr in range(3):
                if r - dr - 1 < 0:
                    continue
                weight += weights[r - dr, c]
                for d in "LR":
                    G.add_edge((r - dr - 1, c, d), (r, c, "T"), weight=weight)

            # from left
            weight = 0
            for dc in range(3):
                if c - dc - 1 < 0:
                    continue
                weight += weights[r, c - dc]
                for d in "TB":
                    G.add_edge((r, c - dc - 1, d), (r, c, "L"), weight=weight)

            # from bottom
            weight = 0
            for dr in range(3):
                if r + dr + 1 >= n_rows:
                    continue
                weight += weights[r + dr, c]
                for d in "LR":
                    G.add_edge((r + dr + 1, c, d), (r, c, "B"), weight=weight)

            # from right
            weight = 0
            for dc in range(3):
                if c + dc + 1 >= n_cols:
                    continue
                weight += weights[r, c + dc]
                for d in "TB":
                    G.add_edge((r, c + dc + 1, d), (r, c, "R"), weight=weight)

    G.add_node((0, 0))
    G.add_node((n_rows - 1, n_cols - 1))

    for d in "LRTB":
        G.add_edge((0, 0), (0, 0, d), weight=0)
        G.add_edge((n_rows - 1, n_cols - 1, d), (n_rows - 1, n_cols - 1), weight=0)

    def dist_heuristic(n1, n2):
        dr, dc = n1[0] - n2[0], n1[1] - n2[1]
        return np.sqrt(dr * dr + dc * dc)

    print(nx.astar_path_length(G, (0, 0), (n_rows - 1, n_cols - 1), dist_heuristic, "weight"))


if __name__ == "__main__":
    main()
