#!/usr/bin/env python3
import itertools
import math
import re


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    lr_inst = lines[0]
    assert lines[1] == ""
    lines = lines[2:]

    nodes = {}
    for ln in lines:
        m = re.match(r"^([^ ]+) = \(([^,]+), ([^ ]+)\)$", ln)
        assert m, f"{ln!r}"
        nodes[m.group(1)] = (m.group(2), m.group(3))

    steps = []
    for start_node in nodes.keys():
        if start_node[-1] != "A":
            continue
        n_steps = 0
        node = start_node
        for dir in itertools.cycle(lr_inst):
            assert dir in ["L", "R"], f"{dir!r}"
            next = nodes[node][0 if dir == "L" else 1]

            node = next
            n_steps += 1
            if node[-1] == "Z":
                break
        print(start_node, n_steps)
        steps.append(n_steps)
    print(math.lcm(*steps))


if __name__ == "__main__":
    main()
