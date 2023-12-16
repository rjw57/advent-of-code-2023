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
        n, _ = n_active(lines, r, c, dr, dc)
        if max_result is None or n > max_result:
            max_result = n
    print(max_result)


def n_active(lines, r, c, dr, dc):
    n_rows = len(lines)
    n_cols = len(lines[0])
    incoming = {(r, c, (dr, dc))}
    prior_incomings = set()
    while True:
        next_incoming = set()
        for row, col, (dr, dc) in incoming:
            square = lines[row][col]
            outgoings = set()
            match square:
                case ".":
                    # direction is preserved
                    outgoings.add((dr, dc))
                case "/":
                    outgoings.add((-dc, -dr))
                case "\\":
                    outgoings.add((dc, dr))
                case "|":
                    if dc == 0:
                        # straight through
                        outgoings.add((dr, dc))
                    else:
                        # pointy ends
                        outgoings.add((-1, 0))
                        outgoings.add((1, 0))
                case "-":
                    if dr == 0:
                        # straight through
                        outgoings.add((dr, dc))
                    else:
                        # pointy ends
                        outgoings.add((0, -1))
                        outgoings.add((0, 1))
                case _:
                    assert False, square
            for dr, dc in outgoings:
                next = (row + dr, col + dc, (dr, dc))
                if next[0] < 0 or next[1] < 0:
                    continue
                if next[0] >= n_rows or next[1] >= n_cols:
                    continue
                next_incoming.add(next)
        # remove existing incomings
        prior_incomings |= incoming
        new_incomings = next_incoming - prior_incomings
        if len(new_incomings) == 0:
            break
        incoming = new_incomings

    active = np.zeros((n_rows, n_cols), dtype=np.uint8)
    for r, c, _ in prior_incomings:
        active[r][c] = 1
    return np.sum(active.flat), incoming


if __name__ == "__main__":
    main()
