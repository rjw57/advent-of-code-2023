#!/usr/bin/env python3
import numpy as np
import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def expand_rows(map: np.array):
    new_rows = []
    for r in map:
        new_rows.append(r)
        if r.sum() == 0:
            new_rows.append(r)
    return np.vstack(new_rows)


def process_lines(lines: list[str]):
    galaxy_map = np.zeros((len(lines), len(lines[0])), dtype=np.int8)
    for row_idx, ln in enumerate(lines):
        for col_idx, c in enumerate(ln):
            galaxy_map[row_idx, col_idx] = 0 if c == "." else 1

    expanded_map = expand_rows(expand_rows(galaxy_map.T).T)
    galaxy_locs = list(zip(*np.nonzero(expanded_map)))
    dist_sum = 0
    for p1_idx, p1 in tqdm.tqdm(enumerate(galaxy_locs)):
        for p2_idx, p2 in enumerate(galaxy_locs[p1_idx + 1 :]):
            dist = np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])
            dist_sum += dist

    print(dist_sum)


if __name__ == "__main__":
    main()
