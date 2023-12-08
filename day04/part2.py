#!/usr/bin/env python3
import re
from collections import defaultdict


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    cards_by_idx = {}
    for ln in lines:
        card_id_str, num_str = ln.split(":")
        m = re.match("Card +([0-9]+)", card_id_str)
        assert m
        card_idx = int(m.group(1))
        winning_str, have_str = num_str.split("|")
        winning_nos = {int(x) for x in winning_str.strip().split(" ") if x != ""}
        have_nos = {int(x) for x in have_str.strip().split(" ") if x != ""}
        cards_by_idx[card_idx] = len(winning_nos.intersection(have_nos))

    card_indices = list(range(1, len(cards_by_idx) + 1))
    processed_cards = defaultdict(lambda: 0)

    while len(card_indices) > 0:
        idx = card_indices.pop()
        n_winning = cards_by_idx[idx]
        processed_cards[idx] += 1
        for copy_idx in range(idx + 1, idx + 1 + n_winning):
            card_indices.append(copy_idx)

    print(sum(v for v in processed_cards.values()))


if __name__ == "__main__":
    main()
