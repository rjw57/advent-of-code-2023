#!/usr/bin/env python3

import re


def main():
    power_sum = 0
    with open("input1.txt") as f:
        for ln in f.readlines():
            ln = ln.strip()
            game_id_str, rest = ln.split(":")

            m = re.match("Game ([0-9]+)", game_id_str)
            assert m, game_id_str

            rounds = [
                {
                    result_str.strip().split(" ")[1]: int(result_str.strip().split(" ")[0])
                    for result_str in round_str.strip().split(",")
                }
                for round_str in rest.split(";")
            ]

            min_count = {"red": 0, "blue": 0, "green": 0}
            for round in rounds:
                for colour, count in round.items():
                    min_count[colour] = max(min_count[colour], count)

            power_sum += min_count["red"] * min_count["blue"] * min_count["green"]

    print(power_sum)


if __name__ == "__main__":
    main()
