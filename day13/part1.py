#!/usr/bin/env python3
import typing

import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_grid(grid: list[str]):
    grid_arr = np.asarray([[1 if c == "#" else 0 for c in ln] for ln in grid], dtype=np.uint8)

    s = 0
    for idx in find_row_of_symmetry(grid_arr):
        s += 100 * (1 + idx)
    for idx in find_row_of_symmetry(grid_arr.T):
        s += 1 + idx

    return s


def find_row_of_symmetry(grid: np.array) -> typing.Generator[int, None, None]:
    # Find indices of possible symmetric rows
    possible_row_sym_idxs = np.nonzero(
        np.prod(np.where(grid[:-1, :] == grid[1:, :], 1, 0), axis=1)
    )[0]

    for row_idx in possible_row_sym_idxs:
        up_rows = range(row_idx, -1, -1)
        down_rows = range(row_idx+1, grid.shape[0])
        for up_idx, down_idx in zip(up_rows, down_rows):
            up, down = grid[up_idx], grid[down_idx]
            if np.any(up != down):
                break
        else:
            yield row_idx


def process_lines(lines: list[str]):
    grid = []
    s = 0
    for ln in lines:
        if ln == "":
            s += process_grid(grid)
            grid = []
        else:
            grid.append(ln)
    s += process_grid(grid)
    print(s)


if __name__ == "__main__":
    main()
