#!/usr/bin/env python3

import re


def main():
    possible_spec = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    id_sum = 0
    with open("input1.txt") as f:
        for ln in f.readlines():
            ln = ln.strip()
            game_id_str, rest = ln.split(":")

            m = re.match("Game ([0-9]+)", game_id_str)
            assert m, game_id_str
            game_id = int(m.group(1))

            rounds = [
                {
                    result_str.strip().split(" ")[1]: int(result_str.strip().split(" ")[0])
                    for result_str in round_str.strip().split(",")
                }
                for round_str in rest.split(";")
            ]

            for round in rounds:
                round_possible = True
                for colour, count in round.items():
                    if possible_spec[colour] < count:
                        round_possible = False
                if not round_possible:
                    break
            else:
                id_sum += game_id

    print(id_sum)


if __name__ == "__main__":
    main()
