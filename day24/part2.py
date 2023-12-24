#!/usr/bin/env python3
import numpy as np
import sympy as sp


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    paths = []
    # problem is over constrained so we only need to look at the first few
    for ln in lines[:4]:
        pos_s, vel_s = ln.split(" @ ")
        pos = np.asarray([int(v) for v in pos_s.split(", ")])
        vel = np.asarray([int(v) for v in vel_s.split(", ")])
        paths.append((pos, vel))

    # For a given stone with position p_i and velocity v_i, then we express the intersection of the
    # stone with the thrown rock as:
    #
    # p_R + t_i * v_R = p_i + t_i * v_i => p_R + t_i * v_R - p_i - t_i * v_i = 0
    p_R = [sp.Symbol(f"p_R_{i}") for i in range(3)]
    v_R = [sp.Symbol(f"v_R_{i}") for i in range(3)]

    constraints = []
    for idx, (p, v) in enumerate(paths):
        t = sp.Symbol(f"t_{idx}")
        for k in range(3):
            constraints.append(p_R[k] + t * v_R[k] - p[k] - t * v[k])

    solution = sp.solve(constraints)[0]
    print(sum(solution[p] for p in p_R))


if __name__ == "__main__":
    main()
