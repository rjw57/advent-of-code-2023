#!/usr/bin/env python3
import re
import math


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    time_str, dist_str = lines[:2]
    assert time_str.startswith("Time:")
    assert dist_str.startswith("Distance:")
    time_str = re.sub(r"^Time:\s+", "", time_str)
    time_str = re.sub(r"\s+", "", time_str)
    dist_str = re.sub(r"^Distance:\s+", "", dist_str)
    dist_str = re.sub(r"\s+", "", dist_str)
    times = [int(v) for v in time_str.split(" ")]
    dists = [int(v) for v in dist_str.split(" ")]
    times_and_dists = list(zip(times, dists))

    way_prod = 1
    for time, dist in times_and_dists:
        best_t_b = 0.5 * time
        best_d = best_t_b * (time - best_t_b)
        a, b, c = 1, -time, dist
        x1 = (-b - math.sqrt(b*b - 4*a*c)) / (2*a) + 1e-10
        x2 = (-b + math.sqrt(b*b - 4*a*c)) / (2*a) - 1e-10
        n_ways = 1 + math.floor(x2) - math.ceil(x1)
        print(f"t: {time}, d: {dist}, best t_b: {best_t_b} best d: {best_d}, x1: {x1:.2f}, x2: {x2:.2f}, n ways: {n_ways}")
        way_prod *= n_ways
    print(way_prod)


# if race lasts t_d ms and button is held for t_b ms then boat goes at speed v = t_b mm/ms
#
# total distance d = = v * (t_d - t_b) = t_b * t_d - t_b^2
#
# dd/dt_b = t_d - 2 * t_b
#
# max d is at t_d = 2 * t_b => t_b = 0.5 * t_d
#
# If we need to go at least a distance d' then, at the boundary
#
# d = d' => t_b * t_d - t_b^2 = d' => t_b^2 - t_d * t_b + d' = 0
#
# can use quad formula to solve for t_b. Add/subtract epsilon to account for d = d' not actually
# winning.


if __name__ == "__main__":
    main()
