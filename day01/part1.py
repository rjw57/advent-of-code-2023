#!/usr/bin/env python3

def main():
    digit_map = {f"{d}": d for d in range(10)}

    sum = 0
    with open("input1.txt") as f:
        for ln in f.readlines():
            ln = ln.strip()
            digits = [digit_map[c] for c in ln if c in digit_map]
            sum += 10 * digits[0] + digits[-1]
    print(sum)


if __name__ == "__main__":
    main()
