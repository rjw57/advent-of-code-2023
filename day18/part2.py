#!/usr/bin/env python3
import shapely


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    coords = [(0,0)]
    for ln in lines:
        px, py = coords[-1]
        _, _, instr = ln.split(" ")
        n = int(instr[2:7], 16)
        dir = instr[7]
        match dir:
            case "0":
                coords.append((px+n, py))
            case "2":
                coords.append((px-n, py))
            case "3":
                coords.append((px, py+n))
            case "1":
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
