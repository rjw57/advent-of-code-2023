#!/usr/bin/env python3
import typing

import numpy as np
from pointInside import cn_PnPoly

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
            path.append(next)
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
    n_rows = len(lines)
    n_cols = len(lines[0])

    starting_pt: typing.Optional[tuple[int, int]] = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                starting_pt = (y, x)
    assert starting_pt is not None

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
            elif c == "F" and (dy, dx) not in [(-1, 0), (0, -1)]:
                continue
            elif c == "7" and (dy, dx) not in [(-1, 0), (0, 1)]:
                continue
            elif c == "J" and (dy, dx) not in [(1, 0), (0, 1)]:
                continue
            elif c == "L" and (dy, dx) not in [(1, 0), (0, -1)]:
                continue
            paths.append(follow(lines, starting_pt, (dy, dx)))

    paths.sort(reverse=True, key=len)
    path = paths[0]
    assert path[0] == path[-1]
    inside = np.zeros((n_rows, n_cols), dtype=np.int32)
    flags = np.ones_like(inside)
    for y, x in path:
        flags[y, x] = 0
    for y in range(n_rows):
        for x in range(n_cols):
            if flags[y, x] == 0:
                continue
            if cn_PnPoly((y, x), path):
                inside[y, x] = 1
    print(np.sum(inside * flags))


if __name__ == "__main__":
    main()
