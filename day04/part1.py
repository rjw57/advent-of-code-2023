#!/usr/bin/env python3
import re


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    score_sum = 0
    for ln in lines:
        card_id_str, num_str = ln.split(":")
        m = re.match("Card +([0-9]+)", card_id_str)
        assert m
        winning_str, have_str = num_str.split("|")
        winning_nos = {int(x) for x in winning_str.strip().split(" ") if x != ""}
        have_nos = {int(x) for x in have_str.strip().split(" ") if x != ""}
        match_nos = winning_nos.intersection(have_nos)

        if len(match_nos) == 0:
            continue
        score_sum += 1<<(len(match_nos)-1)
    print(score_sum)


if __name__ == "__main__":
    main()
