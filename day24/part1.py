#!/usr/bin/env python3
import numpy as np


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def path_intersect(p0, v0, p1, v1):
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    #
    # where: xy1 = p0 + v0, xy2 = p0, xy3 = p1 + v1, xy4 = p1

    # (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    denom = (v0[0] * v1[1]) - (v0[1] * v1[0])
    if denom == 0:
        return np.nan * np.ones((2,))

    x1, y1 = p0 + v0
    x2, y2 = p0
    x3, y3 = p1 + v1
    x4, y4 = p1

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return np.asarray([px, py])


def process_lines(lines: list[str]):
    paths = []
    for ln in lines:
        pos_s, vel_s = ln.split(" @ ")
        pos = np.asarray([int(v) for v in pos_s.split(", ")], dtype=np.longdouble)
        vel = np.asarray([int(v) for v in vel_s.split(", ")], dtype=np.longdouble)
        paths.append((pos[:2], vel[:2]))

    min_coord, max_coord = 200000000000000, 400000000000000
    n_intersect = 0
    for u in range(len(paths)):
        p0, v0 = paths[u]
        for v in range(u+1, len(paths)):
            p1, v1 = paths[v]
            intersection = path_intersect(p0, v0, p1, v1)
            if np.any(np.isnan(intersection)):
                continue
            if np.any(intersection < min_coord):
                continue
            if np.any(intersection > max_coord):
                continue
            t0 = (intersection - p0) / v0
            if np.any(t0 < 0):
                continue
            t1 = (intersection - p1) / v1
            if np.any(t1 < 0):
                continue
            n_intersect += 1

    print(n_intersect)


if __name__ == "__main__":
    main()
