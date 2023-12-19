#!/usr/bin/env python3
import dataclasses
import itertools
import re
from typing import Iterable, Literal, Optional


@dataclasses.dataclass
class Range:
    start: int  # inclusive
    end: int  # exclusive

    def clone(self) -> "Range":
        return Range(start=self.start, end=self.end)

    def is_empty(self) -> bool:
        return self.end - self.start == 0

    def contains(self, v: int) -> bool:
        return v >= self.start and v < self.end

    def split(self, value: int) -> ("Range", "Range", "Range"):
        # Default to left, containing and right ranges being empty.
        left = Range(start=value, end=value)
        containing, right = left.clone(), left.clone()

        if not self.contains(value):
            # range is entirely one side or other of value
            if self.start < value:
                left = self.clone()
            else:
                right = self.clone()
        else:
            # range contains the value
            left = Range(start=self.start, end=value)
            containing = Range(start=value, end=value + 1)
            right = Range(start=value + 1, end=self.end)

        assert left.size() + containing.size() + right.size() == self.size(), (
            f"{value}: {self} ({self.size()}) => {left} "
            f"({left.size()}), {containing} ({containing.size()}), "
            f"{right} ({right.size()}) "
            f"= {left.size() + containing.size() + right.size()}"
        )
        return left, containing, right

    def size(self) -> int:
        return self.end - self.start


@dataclasses.dataclass
class PartFamily:
    ranges: dict[str, Range]

    def clone(self) -> "PartFamily":
        return PartFamily(ranges={**self.ranges})

    def non_empty(self) -> bool:
        return any(not r.is_empty() for r in self.ranges.values())

    def is_empty(self) -> bool:
        return all(r.is_empty() for r in self.ranges.values())

    def size(self) -> int:
        s = 1
        for r in self.ranges.values():
            s *= r.size()
        return s


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

    def evaluate(self, part_family: PartFamily) -> (PartFamily, PartFamily):
        lhs_range = part_family.ranges[self.lhs]
        left, containing, right = lhs_range.split(self.rhs)
        if self.op == "<":
            match_range = left
            if containing.is_empty():
                non_match_range = right
            else:
                non_match_range = Range(start=containing.start, end=right.end)
        elif self.op == ">":
            match_range = right
            if containing.is_empty():
                non_match_range = left
            else:
                non_match_range = Range(start=left.start, end=containing.end)

        assert match_range.size() + non_match_range.size() == lhs_range.size()

        match_family, non_match_family = part_family.clone(), part_family.clone()
        match_family.ranges[self.lhs] = match_range
        non_match_family.ranges[self.lhs] = non_match_range
        assert match_family.size() + non_match_family.size() == part_family.size(), (
            f"{part_family} ({part_family.size()}) => "
            f"{match_family} ({match_family.size()}) + "
            f"{non_match_family} ({non_match_family.size()})"
        )

        return match_family, non_match_family


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

    def evaluate(self, part_family: PartFamily) -> (PartFamily, PartFamily):
        if self.predicate is None:
            match_family = part_family.clone()
            non_match_family = PartFamily(
                ranges={
                    "x": Range(start=0, end=0),
                    "m": Range(start=0, end=0),
                    "a": Range(start=0, end=0),
                    "s": Range(start=0, end=0),
                }
            )
        else:
            match_family, non_match_family = self.predicate.evaluate(part_family)

        assert match_family.size() + non_match_family.size() == part_family.size()
        return match_family, non_match_family


def main():
    with open("input1.txt") as f:
        process_lines([ln.strip() for ln in f.readlines()])


def evaluate_workflow(
    rules: Iterable[Rule], part_family: PartFamily
) -> list[tuple[str, PartFamily], ...]:
    result = []

    match_size = 0
    family_size = part_family.size()
    for r in rules:
        match_family, part_family = r.evaluate(part_family)
        if match_family.non_empty():
            result.append((r.target, match_family))
            match_size += match_family.size()
        else:
            assert match_family.size() == 0

    # Some rule must have matched everything so remaining family must be empty
    assert part_family.is_empty()
    assert match_size == family_size

    return result


def process_lines(lines: list[str]):
    line_iter = iter(lines)
    workflow_specs = list(itertools.takewhile(lambda ln: ln != "", line_iter))

    workflows = {}
    for s in workflow_specs:
        m = re.match("^([^{]+){([^}]*)}$", s)
        assert m
        name = m.group(1)
        rules = [Rule.from_spec(rs) for rs in m.group(2).split(",")]
        workflows[name] = rules

    all_parts = PartFamily(
        ranges={
            "x": Range(start=1, end=4001),
            "m": Range(start=1, end=4001),
            "a": Range(start=1, end=4001),
            "s": Range(start=1, end=4001),
        }
    )

    to_evaluate = [("in", all_parts)]
    all_parts_size = all_parts.size()
    accepted_families = []
    rejected_families = []

    while len(to_evaluate) > 0:
        wf, family = to_evaluate.pop()
        family_size = family.size()
        v_size_sum = 0
        for k, v in evaluate_workflow(workflows[wf], family):
            v_size_sum += v.size()
            if k == "A":
                accepted_families.append(v)
            elif k == "R":
                rejected_families.append(v)
            else:
                to_evaluate.append((k, v))
        assert v_size_sum == family_size

    accepted_size = sum(f.size() for f in accepted_families)
    rejected_size = sum(f.size() for f in rejected_families)
    assert accepted_size + rejected_size == all_parts_size
    print(accepted_size)


if __name__ == "__main__":
    main()
