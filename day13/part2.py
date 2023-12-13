#!/usr/bin/env python3
import typing

import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_grid(grid: list[str]):
    grid_arr = np.asarray([[1 if c == "#" else 0 for c in ln] for ln in grid], dtype=np.uint8)

    full_sym_rows = set(find_row_of_symmetry(grid_arr))
    full_sym_cols = set(find_row_of_symmetry(grid_arr.T))

    sym_lines = {("r", r) for r in full_sym_rows} | {("c", c) for c in full_sym_cols}

    new_lines = set()
    for missing_col in range(grid_arr.shape[1]):
        g = grid_arr[:, np.arange(grid_arr.shape[1]) != missing_col]
        sym_rows = set(find_row_of_symmetry(g))
        if sym_rows != full_sym_rows:
            for r in range(grid_arr.shape[0]):
                g2 = np.copy(grid_arr)
                g2[r, missing_col] = 1 - g2[r, missing_col]
                for sr in find_row_of_symmetry(g2):
                    new_lines.add(("r", sr))

    for missing_row in range(grid_arr.shape[0]):
        g = grid_arr[np.arange(grid_arr.shape[0]) != missing_row, :]
        sym_cols = set(find_row_of_symmetry(g.T))
        if sym_cols != full_sym_cols:
            for c in range(grid_arr.shape[1]):
                g2 = np.copy(grid_arr)
                g2[missing_row, c] = 1 - g2[missing_row, c]
                for sc in find_row_of_symmetry(g2.T):
                    new_lines.add(("c", sc))

    new_lines -= sym_lines

    s = 0
    for c, l in new_lines:
        if c == "r":
            s += 100 * (1 + l)
        else:
            s += 1 + l

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
