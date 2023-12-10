#!/usr/bin/env python3
import itertools
import typing

import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def follow(
    lines: list[str], start: tuple[int, int], dir: tuple[int, int]
) -> list[tuple[int, int]]:
    n_rows = len(lines)
    n_cols = len(lines[0])

    path = [start]
    while True:
        next = tuple(path[-1][n] + dir[n] for n in range(2))
        if next[0] < 0 or next[0] >= n_rows:
            break
        if next[1] < 0 or next[1] >= n_cols:
            break
        c = lines[next[0]][next[1]]

        if c == "S":
            break
        elif c == "|":
            # dir is unchanged
            assert dir[0] != 0, f"{dir!r}"
        elif c == "-":
            # dir is unchanged
            assert dir[1] != 0, f"{dir!r}"
        elif c == "F":
            if dir == (-1, 0):
                dir = (0, 1)
            elif dir == (0, -1):
                dir = (1, 0)
            else:
                assert False, f"{path!r} {next!r} {dir!r}"
        elif c == "7":
            if dir == (-1, 0):
                dir = (0, -1)
            elif dir == (0, 1):
                dir = (1, 0)
            else:
                assert False, f"{path[-3:]!r} {next!r} {dir!r}"
        elif c == "J":
            if dir == (1, 0):
                dir = (0, -1)
            elif dir == (0, 1):
                dir = (-1, 0)
            else:
                assert False, f"{dir!r}"
        elif c == "L":
            if dir == (1, 0):
                dir = (0, 1)
            elif dir == (0, -1):
                dir = (-1, 0)
            else:
                assert False, f"{path!r} {next!r} {dir!r}"

        path.append(next)
    return path


def process_lines(lines: list[str]):
    starting_pt: typing.Optional[tuple[int, int]] = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                starting_pt = (y, x)
    assert starting_pt is not None

    n_rows = len(lines)
    n_cols = len(lines[0])

    y, x = starting_pt
    paths = []
    for dy in [-1, 0, 1]:
        yp = y + dy
        if yp < 0 or yp >= n_rows:
            continue
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            xp = x + dx
            if xp < 0 or xp >= n_cols:
                continue
            if dx != 0 and dy != 0:
                continue
            c = lines[starting_pt[0] + dy][starting_pt[1] + dx]
            if c == ".":
                continue
            elif c == "|" and dx != 0:
                continue
            elif c == "-" and dy != 0:
                continue
            elif c == "F" and (dx != -1 or dy != -1):
                continue
            elif c == "7" and (dx != 1 or dy != -1):
                continue
            elif c == "L" and (dx != -1 or dy != 1):
                continue
            elif c == "J" and (dx != 1 or dy != 1):
                continue
            paths.append(follow(lines, starting_pt, (dy, dx)))

    min_dists = np.inf * np.ones((n_rows, n_cols))
    for dist, steps in enumerate(itertools.zip_longest(*paths)):
        for step in steps:
            if step is None:
                continue
            y, x = step
            min_dists[y, x] = min(min_dists[y, x], dist)
    print(min_dists)
    print(np.max(min_dists[np.isfinite(min_dists)]))


if __name__ == "__main__":
    main()
