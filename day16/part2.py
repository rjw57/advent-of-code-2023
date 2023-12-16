#!/usr/bin/env python3
import numpy as np
from tqdm import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    n_rows = len(lines)
    n_cols = len(lines[0])

    starting_configs = set()
    for r in range(n_rows):
        starting_configs.add((r, 0, 0, 1))
        starting_configs.add((r, n_cols-1, 0, -1))
    for c in range(n_cols):
        starting_configs.add((0, c, 1, 0))
        starting_configs.add((n_rows-1, c, -1, 0))

    max_result = None
    for r, c, dr, dc in tqdm(starting_configs):
        n = n_active(lines, r, c, dr, dc)
        if max_result is None or n > max_result:
            max_result = n
    print(max_result)


def n_active(lines, r, c, dr, dc):
    n_rows = len(lines)
    n_cols = len(lines[0])

    active_wavefronts = {(r, c, dr, dc)}
    previous_wavefronts = set()

    while len(active_wavefronts) > 0:
        next_wavefronts = set()
        for row, col, dr, dc in active_wavefronts:
            square = lines[row][col]
            next_wavefront_dirs = set()
            match square:
                case ".":
                    # direction is preserved
                    next_wavefront_dirs.add((dr, dc))
                case "/":
                    next_wavefront_dirs.add((-dc, -dr))
                case "\\":
                    next_wavefront_dirs.add((dc, dr))
                case "|":
                    if dc == 0:
                        # straight through
                        next_wavefront_dirs.add((dr, dc))
                    else:
                        # pointy ends
                        next_wavefront_dirs.add((-1, 0))
                        next_wavefront_dirs.add((1, 0))
                case "-":
                    if dr == 0:
                        # straight through
                        next_wavefront_dirs.add((dr, dc))
                    else:
                        # pointy ends
                        next_wavefront_dirs.add((0, -1))
                        next_wavefront_dirs.add((0, 1))
                case _:
                    assert False, square
            for dr, dc in next_wavefront_dirs:
                next_wavefront = (row + dr, col + dc, dr, dc)
                if next_wavefront[0] < 0 or next_wavefront[1] < 0:
                    continue
                if next_wavefront[0] >= n_rows or next_wavefront[1] >= n_cols:
                    continue
                next_wavefronts.add(next_wavefront)

        # Only wavefronts we've not previously considered need to be processed
        previous_wavefronts |= active_wavefronts
        active_wavefronts = next_wavefronts - previous_wavefronts

    active = np.zeros((n_rows, n_cols), dtype=np.uint8)
    for r, c, _, _ in previous_wavefronts:
        active[r][c] = 1
    return np.sum(active.flat)


if __name__ == "__main__":
    main()
