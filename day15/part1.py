#!/usr/bin/env python3


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def hash(s: str):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v &= 0xff
    return v


def process_lines(lines: list[str]):
    ivs = "".join(lines).strip().split(",")
    print(sum(hash(v) for v in ivs))


if __name__ == "__main__":
    main()
