#!/usr/bin/env python3
import collections
import re

import networkx as nx


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    G = nx.DiGraph()
    G.add_node("button")
    G.add_edge("button", "broadcaster", state="X")
    for ln in lines:
        m = re.match(r"^([%&]?)([^ ]+) -> (.*)$", ln)
        assert m
        kind, name, outputs_str = m.groups()
        G.add_node(name, kind=kind)
        for output in outputs_str.split(", "):
            G.add_edge(name, output)

    # Initialise edges
    for _, _, d in G.edges(data=True):
        d["state"] = "X"

    # Initialise nodes
    for n, d in G.nodes(data=True):
        kind = d.get("kind")
        if kind == "%":
            # flip-flip
            d["state"] = False
        elif kind == "&":
            # conjunction
            d["state"] = {p: "L" for p in G.predecessors(n)}

    n_h_sent, n_l_sent = 0, 0

    for _ in range(1000):
        # Push the button
        pulse_queue = collections.deque([("button", "broadcaster", "L")])

        while len(pulse_queue) > 0:
            u, v, level = pulse_queue.popleft()

            if level == "H":
                n_h_sent += 1
            else:
                n_l_sent += 1

            node_d = G.nodes[v]
            kind = node_d.get("kind")
            if v == "broadcaster":
                for dest in G.successors(v):
                    pulse_queue.append((v, dest, level))
            elif kind == "%":
                # flip-flop
                if level == "L":
                    node_d["state"] = not node_d["state"]
                    for dest in G.successors(v):
                        pulse_queue.append((v, dest, "H" if node_d["state"] else "L"))
            elif kind == "&":
                # conjunction
                node_d["state"][u] = level
                if all(s == "H" for s in node_d["state"].values()):
                    out = "L"
                else:
                    out = "H"
                for dest in G.successors(v):
                    pulse_queue.append((v, dest, out))

    print(n_h_sent, n_l_sent, n_h_sent * n_l_sent)


if __name__ == "__main__":
    main()
