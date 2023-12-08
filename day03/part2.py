#!/usr/bin/env python3

import re


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    numbers = []
    rows = []
    for y, ln in enumerate(lines):
        row = [None] * len(ln)
        sections = re.split("([0-9]+)", ln)
        x = 0
        for section in sections:
            try:
                v = int(section)
            except ValueError:
                x += len(section)
                continue

            row[x : x + len(section)] = [len(numbers)] * len(section)
            numbers.append(v)

            x += len(section)
        rows.append(row)

    ratio_sum = 0
    for y, ln in enumerate(lines):
        for x, c in enumerate(ln):
            if c != "*":
                continue

            adjacent_number_idxs = set()
            for dx in [-1, 0, 1]:
                xp = x + dx
                if xp < 0 or xp >= len(row):
                    continue
                for dy in [-1, 0, 1]:
                    yp = y + dy
                    if yp < 0 or yp >= len(rows):
                        continue
                    adjacent_number_idx = rows[yp][xp]
                    if adjacent_number_idx is not None:
                        adjacent_number_idxs.add(adjacent_number_idx)

            adjacent_numbers = [numbers[idx] for idx in adjacent_number_idxs]
            if len(adjacent_numbers) == 2:
                ratio_sum += adjacent_numbers[0] * adjacent_numbers[1]

    print(ratio_sum)


if __name__ == "__main__":
    main()
