#!/usr/bin/env python3
import networkx as nx


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    G = nx.DiGraph()

    for r, row in enumerate(lines):
        for c, cell in enumerate(row):
            if cell == "#":
                continue
            elif cell == ".":
                valid_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            elif cell == ">":
                valid_dirs = [(0, 1)]
            elif cell == "<":
                valid_dirs = [(0, -1)]
            elif cell == "^":
                valid_dirs = [(-1, 0)]
            elif cell == "v":
                valid_dirs = [(1, 0)]
            else:
                assert False, f"{(r, c)} {cell}"

            for dr, dc in valid_dirs:
                rp, cp = r + dr, c + dc
                if rp < 0 or rp >= len(lines) or cp < 0 or cp >= len(row):
                    continue
                if lines[rp][cp] == "#":
                    continue
                G.add_edge((r, c), (rp, cp))

    sr, sc = 0, lines[0].index(".")
    er, ec = len(lines) - 1, lines[-1].index(".")
    assert G.has_node((sr, sc))
    assert G.has_node((er, ec))

    max_steps = 0
    for path in nx.all_simple_paths(G, (sr, sc), (er, ec)):
        # A path with n nodes has n-1 steps
        max_steps = max(max_steps, len(path)-1)
    print(max_steps)


if __name__ == "__main__":
    main()
