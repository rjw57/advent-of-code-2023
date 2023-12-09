#!/usr/bin/env python3
import collections

# lower number == better
CARD_RANKS = {c: r for r, c in enumerate("23456789TJQKA"[::-1])}


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def calc_hand_rank(hand_cards: tuple[int]):
    assert len(hand_cards) == 5
    n_per_rank = collections.defaultdict(lambda: 0)
    for c in hand_cards:
        n_per_rank[c] += 1

    if any(n == 5 for n in n_per_rank.values()):
        # 5 of a kind
        return 0
    if any(n == 4 for n in n_per_rank.values()):
        # 4 of a kind
        return 1

    n_pairs = sum(1 if n == 2 else 0 for n in n_per_rank.values())

    if any(n == 3 for n in n_per_rank.values()):
        if n_pairs > 0:
            # full house
            return 2
        # 3 of a kind
        return 3
    if n_pairs == 2:
        # two pair
        return 4
    if n_pairs == 1:
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
