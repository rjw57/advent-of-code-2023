#!/usr/bin/env python3
import re
import typing


def main():
    process_lines(lines("./input1.txt"))


def lines(file: str):
    with open(file) as f:
        yield from (ln.strip() for ln in f.readlines())


def process_lines(lines: typing.Generator[str, None, None]):
    seeds_ln = next(lines)
    assert seeds_ln.startswith("seeds: ")
    seeds = [int(s) for s in seeds_ln.split(": ")[1].split(" ")]
    assert next(lines) == ""

    maps = {}
    while True:
        try:
            map_header = next(lines)
        except StopIteration:
            break
        m = re.match("([^-]+)-to-([^-]+) map:", map_header)
        assert m
        src, dst = m.group(1), m.group(2)

        map = []
        for map_ln in lines:
            if map_ln == "":
                break
            dst_start, src_start, count = (int(v) for v in map_ln.split(" "))
            map.append((src_start, dst_start, count))
        maps[src] = (dst, map)

    loc_nos = []
    for seed_n in seeds:
        src, n = "seed", seed_n
        while src != "location":
            dst, map = maps[src]
            for src_start, dst_start, count in map:
                if n >= src_start and n < src_start + count:
                    n = n - src_start + dst_start
                    break
            src = dst
        loc_nos.append(n)
    loc_nos.sort()
    print(loc_nos[0])


if __name__ == "__main__":
    main()
