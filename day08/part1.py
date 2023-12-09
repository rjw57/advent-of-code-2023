#!/usr/bin/env python3
import itertools
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

    node = "AAA"
    n_steps = 0
    for dir in itertools.cycle(lr_inst):
        assert dir in ["L", "R"], f"{dir!r}"
        next = nodes[node][0 if dir == "L" else 1]
        print(f"{node!r} -> {next!r}")

        node = next
        n_steps += 1
        if node == "ZZZ":
            break
    print(n_steps)


if __name__ == "__main__":
    main()
