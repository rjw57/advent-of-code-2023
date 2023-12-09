#!/usr/bin/env python3


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    sum = 0
    for ln in lines:
        seqs = [[int(v) for v in ln.split(" ")]]
        while len(seqs[-1]) > 1:
            seqs.append([b-a for a, b in zip(seqs[-1][:-1], seqs[-1][1:])])
        assert seqs[-1] == [0]
        idx = len(seqs) - 2
        while idx >= 0:
            delta = seqs[idx+1][-1]
            seqs[idx].append(seqs[idx][-1] + delta)
            idx -= 1
        sum += seqs[0][-1]
    print(sum)


if __name__ == "__main__":
    main()
