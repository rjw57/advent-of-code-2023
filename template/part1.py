#!/usr/bin/env python3


def main():
    with open("example1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    pass


if __name__ == "__main__":
    main()
