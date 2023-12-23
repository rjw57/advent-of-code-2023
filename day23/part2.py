#!/usr/bin/env python3
import networkx as nx
import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def graph_from_grid(grid: np.array) -> nx.Graph:
    G = nx.Graph()

    valid_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 0:
                continue
            for dr, dc in valid_dirs:
                rp, cp = r + dr, c + dc
                if rp < 0 or rp >= grid.shape[0] or cp < 0 or cp >= grid.shape[1]:
                    continue
                if grid[rp, cp] == 0:
                    continue
                if G.has_edge((r, c), (rp, cp)):
                    continue
                G.add_edge((r, c), (rp, cp), weight=1)

    # Prune "removable" nodes where there is only one path
    while True:
        n_pruned = 0
        for n in list(G.nodes):
            if not G.has_node(n) or G.degree(n) != 2:
                continue
            weight = sum(d["weight"] for _, _, d in G.edges(n, data=True))
            n1, n2 = G.neighbors(n)
            G.remove_node(n)
            G.add_edge(n1, n2, weight=weight)
            n_pruned += 1
        if n_pruned == 0:
            break

    return G


def brute_force_longest_path(G: nx.Graph, start: tuple[int, int], end: tuple[int, int]) -> int:
    assert G.has_node(start)
    assert G.has_node(end)

    longest_length = 0
    n_nodes = len(G.nodes)
    for path in nx.all_simple_edge_paths(G, start, end):
        length = sum(G.edges[e]["weight"] for e in path)
        if length > longest_length:
            longest_length = length
            print(f"best: {length} using {len(path) + 1}/{n_nodes} nodes")
    return longest_length


def process_lines(lines: list[str]):
    is_path = np.asarray([[0 if c == "#" else 1 for c in row] for row in lines], dtype=np.uint8)
    start = (0, lines[0].index("."))
    end = (len(lines) - 1, lines[-1].index("."))
    G = graph_from_grid(is_path)
    G.nodes[start]["fillcolor"] = "darkseagreen"
    G.nodes[start]["style"] = "filled"
    G.nodes[end]["fillcolor"] = "lightpink"
    G.nodes[end]["style"] = "filled"
    for _, _, d in G.edges(data=True):
        d["label"] = str(d["weight"])
    nx.drawing.nx_pydot.write_dot(G, "problem.dot")
    print(brute_force_longest_path(G, start, end))


if __name__ == "__main__":
    main()
