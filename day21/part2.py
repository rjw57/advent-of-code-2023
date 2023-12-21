#!/usr/bin/env python3
import numpy as np
from tqdm import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    n_rows = len(lines)
    n_cols = len(lines[0])
    assert n_rows == n_cols
    assert n_rows % 2 == 1

    plot_locs = set()

    start_loc = None
    for r in range(n_rows):
        for c in range(n_cols):
            # Record starting position
            if lines[r][c] == "S":
                start_loc = (r, c)

            # Cannot walk over rocks
            if lines[r][c] == "#":
                continue

            # Record this as a plot location.
            plot_locs.add((r, c))

    assert start_loc is not None
    assert start_loc[0] == n_rows//2
    assert start_loc[1] == n_cols//2

    possible_starts = {start_loc: {start_loc}}

    n_total_steps = 26501365
    remainder = n_total_steps % n_rows
    print(n_total_steps % n_rows)
    assert n_total_steps % n_rows == (n_rows - 1) / 2

    counts = []
    n_steps = remainder + 4 * n_rows # see below for we we do this many steps
    for _ in tqdm(range(n_steps)):
        next_starts = {}
        for (r, c), mirrored_locs in possible_starts.items():
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr = (r + n_rows + dr) % n_rows
                nc = (c + n_cols + dc) % n_cols
                if (nr, nc) not in plot_locs:
                    continue
                new_mirrored_locs = next_starts.get((nr, nc), set())
                for mr, mc in mirrored_locs:
                    new_mirrored_locs.add((mr + dr, mc + dc))
                next_starts[(nr, nc)] = new_mirrored_locs
        possible_starts = next_starts
        counts.append(sum(len(v) for v in possible_starts.values()))

    # Rationale for the following: after n_rows steps, a "diamond" is formed containing full grids
    # within itself and the same repeating pattern of grids for the edges. There will be 4 fixed
    # patterns (the "points" of the diamond) and four patterns repeated by the number of multiples
    # of n_rows steps we've made (the "perimeter" of the diamond) with an enclosed interior.
    #
    # We don't now what the number of plots within each set of patterns is but we do know that they
    # are fixed so the total number of plots is
    #
    #   (plots in diamond points) + N * (plots in edges) + N^2 * (plots in interior)
    #
    # Where N is number of steps / width of the grid. This is a quadratic and so we can use the
    # difference method to solve for the result.

    # Strip the first count and step count since that's the corner case where there are no internal
    # plots.
    counts = np.asarray(counts)[(n_total_steps % n_rows) - 1 :: n_rows][1:]
    steps = np.arange(1, n_steps + 1)[(n_total_steps % n_rows - 1) :: n_rows][1:]

    # Compute second order difference.
    first_order_diff = np.diff(counts)
    second_order_diff = np.diff(first_order_diff)

    # If our model is correct, the second order difference should be constant.
    assert second_order_diff[-2] == second_order_diff[-1]

    # How many more steps would we need to perform?
    n_more_steps = n_total_steps - steps[-1]
    assert n_more_steps % n_rows == 0
    n_more_iterations = n_more_steps // n_rows

    # Compute next values in the sequence.
    n = counts[-1]
    first_delta = first_order_diff[-1]
    second_delta = second_order_diff[-1]
    for _ in range(n_more_iterations):
        first_delta += second_delta
        n += first_delta
    print(n)


if __name__ == "__main__":
    main()
