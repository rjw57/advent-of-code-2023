#!/usr/bin/env python3
import networkx as nx
import numpy as np
from tqdm import tqdm


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def process_lines(lines: list[str]):
    cuboids = []
    for ln in lines:
        start_s, end_s = ln.split("~")
        cuboids.append(
            (tuple(int(v) for v in start_s.split(",")), tuple(int(v) for v in end_s.split(",")))
        )

    projections = []
    for s, e in cuboids:
        dx = e[0] - s[0]
        dy = e[1] - s[1]
        assert dx == 0 or dy == 0
        locs = set()
        if dx == 0:
            length = 1 + np.abs(e[1] - s[1])
            for d in range(length):
                locs.add((s[0], s[1] + d * np.sign(dy)))
        else:
            length = 1 + np.abs(e[0] - s[0])
            for d in range(length):
                locs.add((s[0] + d * np.sign(dx), s[1]))

        projections.append(locs)

    # G will hold "is under" edges
    underG = nx.DiGraph()

    for u, cu in enumerate(tqdm(cuboids)):
        uz = max(cu[0][2], cu[1][2])
        uh = 1 + np.abs(cu[1][2] - cu[0][2])
        underG.add_node(u, h=uh)
        for v, cv in enumerate(cuboids):
            # Is v under u or at the same level?
            if min(cv[0][2], cv[1][2]) <= uz:
                # yes, it can't be over u.
                continue

            # Do projections intersect?
            if len(projections[u].intersection(projections[v])) == 0:
                continue

            underG.add_edge(u, v)

    # Which bricks are on the floor?
    to_process = set(n for n in underG.nodes if len(list(underG.predecessors(n))) == 0)
    for n in to_process:
        underG.nodes[n]["z"] = 1

    # Pile blocks atop each other.
    while len(to_process) > 0:
        next_to_process = set()
        for u in to_process:
            nz = underG.nodes[u]["z"] + underG.nodes[u]["h"]
            for v in underG.successors(u):
                d = underG.nodes[v]
                d["z"] = max(d.get("z", 0), nz)
                next_to_process.add(v)
        to_process = next_to_process

    for n, d in underG.nodes(data=True):
        d["label"] = f"{n}\\nh={d['h']}\\nz={d['z']}"

    # Form a graph which represents "directly supports"
    supportG = underG.copy()
    for u, v in underG.edges:
        uz = underG.nodes[u]["z"]
        vz = underG.nodes[v]["z"]
        assert vz > uz
        # A block is directly supported if it is resting on the under block.
        if vz - uz != underG.nodes[u]["h"]:
            supportG.remove_edge(u, v)

    # nx.drawing.nx_pydot.write_dot(supportG, "support-graph.dot")

    n_disintegratable = 0
    for u in supportG.nodes:
        # is this the only supporter of at least one successor node?
        if not any(supportG.in_degree(v) == 1 for v in supportG.successors(u)):
            # no, it can be disintegrated
            n_disintegratable += 1

    print(n_disintegratable)


if __name__ == "__main__":
    main()
