#!/usr/bin/env python3
import numpy as np

ROCK_MAP = {".": 0, "O": 1, "#": 2}


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    rock_grid = np.asarray([[ROCK_MAP[c] for c in r] for r in lines])

    while True:
        rock_spaces = np.logical_and(rock_grid[:-1, :] == 0, rock_grid[1:, :] == 1)
        rs, cs = np.nonzero(rock_spaces)
        if len(rs) == 0:
            break
        for r, c in zip(rs, cs):
            rock_grid[r, c] = 1
            rock_grid[r + 1, c] = 0

    s = 0
    for r_idx, r in enumerate(rock_grid):
        s += (rock_grid.shape[0] - r_idx) * np.sum(r == 1)
    print(s)


if __name__ == "__main__":
    main()
