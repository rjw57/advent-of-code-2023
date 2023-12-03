#!/usr/bin/env python3

def main():
    digit_map = {f"{d}": d for d in range(10)}
    digit_names = [None, "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    sum = 0
    with open("input2.txt") as f:
        for ln in f.readlines():
            ln = ln.strip()
            found_names = []
            for pos, dn in enumerate(ln):
                if dn in digit_map:
                    found_names.append((pos, digit_map[dn], dn))

            for d, dn in enumerate(digit_names):
                if dn is None:
                    continue
                pos = ln.find(dn)
                if pos >= 0:
                    found_names.append((pos, d, dn))
                pos = (ln[::-1]).find(dn[::-1])
                if pos >= 0:
                    found_names.append((len(ln) - pos - len(dn), d, dn))

            found_names.sort()
            sum += 10 * found_names[0][1] + found_names[-1][1]
    print(sum)


if __name__ == "__main__":
    main()
