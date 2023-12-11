#!/usr/bin/env python3
import numpy as np
import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def rows_to_expand(map: np.array):
    row_idxs = []
    for row_idx, r in enumerate(map):
        if r.sum() == 0:
            row_idxs.append(row_idx)
    return row_idxs


def process_lines(lines: list[str]):
    galaxy_map = np.zeros((len(lines), len(lines[0])), dtype=np.int8)
    for row_idx, ln in enumerate(lines):
        for col_idx, c in enumerate(ln):
            galaxy_map[row_idx, col_idx] = 0 if c == "." else 1

    row_locs = np.arange(0, galaxy_map.shape[0])
    col_locs = np.arange(0, galaxy_map.shape[0])

    for r_idx in rows_to_expand(galaxy_map):
        row_locs[r_idx:] += 1000000-1
    for c_idx in rows_to_expand(galaxy_map.T):
        col_locs[c_idx:] += 1000000-1

    galaxy_locs = list(zip(*np.nonzero(galaxy_map)))
    dist_sum = 0
    for p1_idx, map_p1 in tqdm.tqdm(enumerate(galaxy_locs)):
        p1 = (row_locs[map_p1[0]], col_locs[map_p1[1]])
        for p2_idx, map_p2 in enumerate(galaxy_locs[p1_idx + 1 :]):
            p2 = (row_locs[map_p2[0]], col_locs[map_p2[1]])
            dist = np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])
            dist_sum += dist

    print(dist_sum)


if __name__ == "__main__":
    main()
