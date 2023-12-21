#!/usr/bin/env python3
import networkx as nx


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    n_rows = len(lines)
    n_cols = len(lines[0])

    G = nx.Graph()

    start = None
    for r in range(n_rows):
        for c in range(n_cols):
            # Record starting position
            if lines[r][c] == "S":
                start = (r, c)

            # Cannot walk over rocks
            if lines[r][c] == "#":
                continue

            # Look above and to the left. Right and down will be covered when we examine that cell.
            if r > 0 and lines[r - 1][c] != "#":
                G.add_edge((r - 1, c), (r, c))
            if c > 0 and lines[r][c - 1] != "#":
                G.add_edge((r, c - 1), (r, c))

    assert start is not None

    possible_starts = {start}
    for _ in range(64):
        next_starts = set()
        for u in possible_starts:
            next_starts.update(G.neighbors(u))
        possible_starts = next_starts
    print(len(possible_starts))


if __name__ == "__main__":
    main()
