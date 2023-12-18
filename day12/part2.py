#!/usr/bin/env python3
import functools

from tqdm import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


@functools.cache
def n_matches(pattern: str, block_lens: tuple[int]) -> int:
    # No blocks, entire pattern must allow spaces.
    if len(block_lens) == 0:
        return 0 if "#" in pattern else 1

    if sum(block_lens) + len(block_lens) - 1 > len(pattern):
        # no room
        return 0

    # One block
    if len(block_lens) == 1:
        n_possible = 0
        block_len = block_lens[0]
        if len(pattern) < block_len:
            return 0
        for n in range(0, len(pattern) - block_len + 1):
            if "#" in pattern[:n]:
                continue
            if "." in pattern[n : n + block_len]:
                continue
            if "#" in pattern[n + block_len :]:
                continue
            n_possible += 1
        return n_possible

    # Two blocks
    if len(block_lens) == 2:
        b1, b2 = block_lens
        if len(pattern) < b1 + b2 + 1:
            return 0
        n_possible = 0
        for b1_idx in range(0, len(pattern)):
            if b1_idx + b1 > len(pattern):
                continue
            if "#" in pattern[b1_idx + b1 : b1_idx + b1 + 1]:
                continue
            if "#" in pattern[:b1_idx]:
                continue
            if "." in pattern[b1_idx : b1_idx + b1]:
                continue

            for b2_idx in range(b1_idx + b1 + 1, len(pattern)):
                if b2_idx + b2 > len(pattern):
                    continue
                if "#" in pattern[b1_idx + b1 + 1 : b2_idx]:
                    continue
                if "." in pattern[b2_idx : b2_idx + b2]:
                    continue
                if "#" in pattern[b2_idx + b2 :]:
                    continue
                n_possible += 1
        return n_possible

    # Three or more blocks, divide and conquer.
    middle_block_idx = len(block_lens) >> 1
    m = block_lens[middle_block_idx]
    left_blocks = block_lens[:middle_block_idx]
    right_blocks = block_lens[middle_block_idx + 1 :]

    # The middle block must be a space, the block, and the space. Where can that start?
    n_possible = 0
    for n in range(0, len(pattern) - m - 2 + 1):
        if pattern[n] == "#":
            continue
        if "." in pattern[n + 1 : n + 1 + m]:
            continue
        if pattern[n + m + 1] == "#":
            continue
        left = pattern[:n]
        right = pattern[n + m + 2 :]
        n_possible += n_matches(left, left_blocks) * n_matches(right, right_blocks)

    return n_possible


def process_lines(lines: list[str]):
    match_sum = 0
    for ln in tqdm(lines):
        pattern, spec = ln.split(" ")
        pattern = "?".join([pattern] * 5)
        spec = ",".join([spec] * 5)

        block_lens = tuple(int(v) for v in spec.split(","))
        if len(block_lens) == 0:
            continue

        match_count = n_matches(pattern, block_lens)
        match_sum += match_count

    print(match_sum)


if __name__ == "__main__":
    main()
