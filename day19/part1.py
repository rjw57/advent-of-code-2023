#!/usr/bin/env python3
import dataclasses
import itertools
import re
from typing import Literal, Optional, Iterable


@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_spec(cls, spec: str):
        kwargs = {}
        for vs in spec.split(","):
            k, v = vs.split("=")
            kwargs[k] = int(v)
        return cls(**kwargs)


@dataclasses.dataclass
class Predicate:
    lhs: Literal["x", "m", "a", "s"]
    rhs: int
    op: Literal[">", "<"]

    @classmethod
    def from_spec(cls, spec: str):
        m = re.match("^([xmas])([<>])([0-9]+)$", spec)
        assert m
        return cls(lhs=m.group(1), rhs=int(m.group(3)), op=m.group(2))

    def evaluate(self, part: Part) -> bool:
        lhs_v: int = getattr(part, self.lhs)
        match self.op:
            case ">":
                return lhs_v > self.rhs
            case "<":
                return lhs_v < self.rhs
            case _:
                assert False


@dataclasses.dataclass
class Rule:
    target: str
    predicate: Optional[Predicate] = None

    @classmethod
    def from_spec(cls, spec: str):
        if ":" not in spec:
            return cls(target=spec)
        pred_spec, target = spec.split(":")
        return cls(target=target, predicate=Predicate.from_spec(pred_spec))

    def evaluate(self, part: Part) -> Optional[str]:
        if self.predicate is None:
            return self.target
        if self.predicate.evaluate(part):
            return self.target
        return None


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def evaluate_workflow(rules: Iterable[Rule], part: Part) -> Optional[str]:
    for r in rules:
        t = r.evaluate(part)
        if t is not None:
            return t
    return None


def process_lines(lines: list[str]):
    line_iter = iter(lines)
    workflow_specs = list(itertools.takewhile(lambda l: l != "", line_iter))
    part_specs = list(line_iter)

    workflows = {}
    for s in workflow_specs:
        m = re.match("^([^{]+){([^}]*)}$", s)
        assert m
        name = m.group(1)
        rules = [Rule.from_spec(rs) for rs in m.group(2).split(",")]
        workflows[name] = rules

    out_sum = 0
    for s in part_specs:
        m = re.match("^{([^}]*)}$", s)
        assert m, f"{s!r}"
        p = Part.from_spec(m.group(1))

        wf = "in"
        while wf not in {"R", "A"}:
            wf = evaluate_workflow(workflows[wf], p)
            assert wf is not None

        if wf == "A":
            out_sum += p.x
            out_sum += p.m
            out_sum += p.a
            out_sum += p.s

    print(out_sum)


if __name__ == "__main__":
    main()
