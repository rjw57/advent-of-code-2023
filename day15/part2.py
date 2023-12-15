#!/usr/bin/env python3
from collections import defaultdict


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def hash(s: str):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v &= 0xFF
    return v


def process_lines(lines: list[str]):
    ivs = "".join(lines).strip().split(",")
    hm = defaultdict(list)
    for iv in ivs:
        if "-" in iv:
            assert iv[-1] == "-"
            op = "-"
            iv = iv[:-1]
            arg = None
        elif "=" in iv:
            op = "="
            iv, arg_s = iv.split("=")
            arg = int(arg_s)
        else:
            assert False

        box = hash(iv)
        contents = hm[box]

        if op == "=":
            new_contents = []
            changed = False
            for label, lens in contents:
                if label == iv:
                    new_contents.append((iv, arg))
                    changed = True
                else:
                    new_contents.append((label, lens))
            if not changed:
                new_contents.append((iv, arg))
            hm[box] = new_contents
        elif op == "-":
            new_contents = []
            for label, lens in contents:
                if label != iv:
                    new_contents.append((label, lens))
            hm[box] = new_contents

    s = 0
    for box_idx in range(256):
        for lens_idx, (_, foc) in enumerate(hm[box_idx]):
            s += (1 + box_idx) * (lens_idx + 1) * foc
    print(s)


if __name__ == "__main__":
    main()
