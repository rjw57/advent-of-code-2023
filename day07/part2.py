#!/usr/bin/env python3
import collections

# lower number == better
CARD_RANKS = {c: r for r, c in enumerate("J23456789TQKA"[::-1])}


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def calc_hand_rank(hand_cards: tuple[int]):
    assert len(hand_cards) == 5
    n_per_rank = collections.defaultdict(lambda: 0)
    for c in hand_cards:
        n_per_rank[c] += 1

    n_jokers = n_per_rank[CARD_RANKS["J"]]
    n_per_rank[CARD_RANKS["J"]] = 0

    if any(n + n_jokers >= 5 for n in n_per_rank.values()):
        # 5 of a kind, including jokers
        return 0
    if any(n + n_jokers >= 4 for n in n_per_rank.values()):
        # 4 of a kind
        return 1

    # Triples
    have_triple = False
    for c, n in n_per_rank.items():
        if n + n_jokers < 3:
            continue
        # can form a triple with c
        have_triple = True
        n_unused_jokers = n_jokers - (3 - n)
        for c2, n2 in n_per_rank.items():
            if c == c2:
                continue
            if n2 + n_unused_jokers >= 2:
                # there is a pair left => full house
                return 2
    if have_triple:
        # 3 of a kind
        return 3

    # Pairs
    have_pair = False
    for c, n in n_per_rank.items():
        if n + n_jokers < 2:
            continue
        # can form a pair with c
        have_pair = True
        n_unused_jokers = n_jokers - (2 - n)
        for c2, n2 in n_per_rank.items():
            if c == c2:
                continue
            if n2 + n_unused_jokers >= 2:
                # there is a pair left => two pair
                return 4
    if have_pair:
        # one pair
        return 5

    # high card
    return 6


def process_lines(lines: list[str]):
    hands = []
    for ln in lines:
        hand_str, bid_str = ln.split(" ")
        bid = int(bid_str)
        hand_cards = tuple(CARD_RANKS[c] for c in hand_str)
        hand_rank = calc_hand_rank(hand_cards)
        sorted_hand_str = ''.join(sorted(list(hand_str)))
        hands.append((hand_rank,) + hand_cards + (hand_str, sorted_hand_str, bid))
        # print(f"{hand_str!r}, {hand_rank}, {hand_cards!r}, {bid}")
        # print(f"{hand_str}, {hands[-1]}")
    hands.sort(reverse=True)
    winnings = 0
    for idx, hand in enumerate(hands):
        winnings += (idx + 1) * hand[-1]
    print(winnings)


if __name__ == "__main__":
    main()
