#!/usr/bin/env python3
import typing


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def gen_packings(
    block_lens: list[int], slacks: list[int], total_slack: int
) -> typing.Generator[str, None, None]:
    # Yield packing if packing finished
    if len(slacks) == len(block_lens) + 1 and sum(slacks) == total_slack:
        s_parts = []
        for idx in range(len(block_lens)):
            s_parts.append("." * slacks[idx])
            s_parts.append("#" * block_lens[idx])
        s_parts.append("." * slacks[-1])
        yield "".join(s_parts)

    # If we have slacks for all possible places, return nothing
    if len(slacks) >= len(block_lens) + 1:
        return

    if len(slacks) == 0 or len(slacks) == len(block_lens):
        start_slack = 0
    else:
        start_slack = 1

    remaining_slack = total_slack - sum(slacks)
    if remaining_slack < start_slack:
        return

    new_slacks = slacks + [9]
    for additional_slack in range(start_slack, remaining_slack + 1):
        new_slacks[-1] = additional_slack
        yield from gen_packings(block_lens, new_slacks, total_slack)


def process_lines(lines: list[str]):
    match_sum = 0
    for ln in lines:
        pattern, spec = ln.split(" ")
        block_lens = [int(v) for v in spec.split(",")]
        total_slack = len(pattern) - sum(block_lens)

        fixed_idxs = [idx for idx, c in enumerate(pattern) if c != "?"]

        print(f"pattern: {pattern!r}, spec: {block_lens!r}")
        # print(pattern)
        match_count = 0
        for packing in gen_packings(block_lens, [], total_slack):
            if all(packing[idx] == pattern[idx] for idx in fixed_idxs):
                # print(packing)
                match_count += 1
        match_sum += match_count
        print(f"count: {match_count}")

    print(match_sum)


if __name__ == "__main__":
    main()
