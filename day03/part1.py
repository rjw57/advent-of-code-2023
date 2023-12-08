#!/usr/bin/env python3

import re


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    rows = []
    for ln in lines:
        rows.append([[c, False] for c in ln])

    for y, row in enumerate(rows):
        for x, (c, _) in enumerate(row):
            if c not in ".0123456789":
                for dx in [-1, 0, 1]:
                    xp = x + dx
                    if xp < 0 or xp >= len(row):
                        continue
                    for dy in [-1, 0, 1]:
                        yp = y + dy
                        if yp < 0 or yp >= len(rows):
                            continue
                        rows[yp][xp][1] = True

    part_sum = 0
    for y, ln in enumerate(lines):
        sections = re.split("([0-9]+)", ln)
        x = 0
        for section in sections:
            try:
                v = int(section)
            except ValueError:
                x += len(section)
                continue

            is_adjacent = False
            for dx, _ in enumerate(section):
                is_adjacent = is_adjacent or rows[y][x+dx][1]

            if is_adjacent:
                part_sum += v

            x += len(section)

    print(part_sum)


if __name__ == "__main__":
    main()
