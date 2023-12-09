#!/usr/bin/env python3
import dataclasses
import re
import typing


@dataclasses.dataclass
class Range:
    start: int
    count: int

    def split(self, other: "Range"):
        if other.start >= self.start + self.count:
            # other is entirely off to the right
            return self, None, None
        if other.start + other.count <= self.start:
            # other is entirely off to the left
            return None, None, self
        if other.start <= self.start and other.start + other.count >= self.start + self.count:
            # other entirely covers us
            return None, self, None
        if other.start <= self.start:
            # other overlaps to the left
            overlap_count = other.start + other.count - self.start
            assert overlap_count < self.count, f"{overlap_count} {self!r} {other!r}"
            return (
                None,
                Range(start=self.start, count=overlap_count),
                Range(start=self.start + overlap_count, count=self.count - overlap_count),
            )
        # other overlaps to the right
        overlap_count = self.start + self.count - other.start
        assert overlap_count < self.count, f"{overlap_count} {self!r} {other!r}"
        return (
            Range(start=self.start, count=other.start - self.start),
            Range(start=other.start, count=overlap_count),
            None,
        )


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

    seed_ranges = []
    for m in range(0, len(seeds), 2):
        seed_start, seed_count = seeds[m : m + 2]
        seed_ranges.append(Range(seed_start, seed_count))

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
            map.append((Range(src_start, count), Range(dst_start, count)))
        maps[src] = (dst, map)

    src, ranges = "seed", seed_ranges
    while src != "location":
        dst, map = maps[src]
        out_ranges = []
        for src_rng, dst_rng in map:
            to_process = []
            for rng in ranges:
                left, mid, right = rng.split(src_rng)
                if left is not None:
                    to_process.append(left)
                if right is not None:
                    to_process.append(right)
                if mid is not None:
                    out_ranges.append(
                        Range(start=mid.start - src_rng.start + dst_rng.start, count=mid.count)
                    )
            ranges = to_process
        out_ranges.extend(ranges)
        ranges = out_ranges
        src = dst

    out_ranges.sort(key=lambda r: r.start)
    print(out_ranges[0].start)


if __name__ == "__main__":
    main()
