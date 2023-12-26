#!/usr/bin/env python3
import networkx as nx


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    G = nx.Graph()

    for ln in lines:
        u, vs = ln.split(": ")
        for v in vs.split(" "):
            G.add_edge(u, v)

    edge_cut = nx.minimum_edge_cut(G)
    assert len(edge_cut) == 3

    for u, v in edge_cut:
        G.remove_edge(u, v)

    p = 1
    for s in nx.connected_components(G):
        p *= len(s)
    print(p)


if __name__ == "__main__":
    main()
