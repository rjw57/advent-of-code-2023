#!/usr/bin/env python3
import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    n_rows = len(lines)
    n_cols = len(lines[0])
    incoming = {(0, 0, (0, 1))}
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
    print(np.sum(active.flat))


if __name__ == "__main__":
    main()
