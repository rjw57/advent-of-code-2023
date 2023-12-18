#!/usr/bin/env python3
import shapely


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    coords = [(0,0)]
    for ln in lines:
        px, py = coords[-1]
        dir, n_str, _ = ln.split(" ")
        n = int(n_str)
        match dir:
            case "R":
                coords.append((px+n, py))
            case "L":
                coords.append((px-n, py))
            case "U":
                coords.append((px, py+n))
            case "D":
                coords.append((px, py-n))
            case _:
                assert False, f"{dir!r}"

    p = shapely.Polygon(coords)

    # The area includes the 1 metre square containing the edge.
    for dx in (-0.5, 0, 0.5):
        for dy in (-0.5, 0, 0.5):
            p = p.union(shapely.Polygon([
                (x+dx, y+dy)
                for x, y in coords
            ]))

    print(int(p.area))


if __name__ == "__main__":
    main()
