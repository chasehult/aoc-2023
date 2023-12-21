import re
from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple

inp = open('day19.txt').read().strip()


class Rule(NamedTuple):
    attr: str
    num: int
    gt: bool
    to: str

    def check(self, part: dict[str, int]) -> bool:
        if self.num == part[self.attr]:
            return False
        return (part[self.attr] < self.num) != self.gt


class MoveRule(NamedTuple):
    to: str

    def check(self, part: dict[str, int]) -> bool:
        return True


@dataclass
class PartRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    @classmethod
    def new(cls) -> 'PartRange':
        return PartRange((1, 4000), (1, 4000), (1, 4000), (1, 4000))

    @classmethod
    def none(cls) -> 'PartRange':
        return PartRange((0, 0), (0, 0), (0, 0), (0, 0))

    def copy(self) -> 'PartRange':
        return PartRange(self.x, self.m, self.a, self.s)

    def split(self, rule) -> tuple['PartRange', 'PartRange']:
        """(true range, false range)"""
        if isinstance(rule, MoveRule):
            return self, self.none()
        mina, maxa = getattr(self, rule.attr)
        if rule.num <= mina:
            if rule.gt:
                return self, self.none()
            return self.none(), self
        elif maxa <= rule.num:
            if rule.gt:
                return self.none(), self
            return self, self.none()
        copy1 = self.copy()
        copy2 = self.copy()
        if rule.gt:
            setattr(copy1, rule.attr, (mina, rule.num))
            setattr(copy2, rule.attr, (rule.num + 1, maxa))
            return copy2, copy1

        setattr(copy1, rule.attr, (mina, rule.num - 1))
        setattr(copy2, rule.attr, (rule.num, maxa))
        return copy1, copy2

    def get_posses(self) -> int:
        posses = 1
        for attr in 'xmas':
            posses *= getattr(self, attr)[1] - getattr(self, attr)[0] + 1
        return posses

    def __bool__(self):
        return bool(self.get_posses())


wfs, ps = inp.split('\n\n')

workflows = defaultdict(list)

for name, rules in re.findall(r'([a-z]+)\{([^}]+?)}', wfs):
    rules = rules.split(',')
    for rulestr in rules:
        if re.fullmatch(r'A|R|[a-z]+', rulestr):
            rule = MoveRule(rulestr)
        else:
            attr, gt, num, to = re.findall(r'([xmas])([<>])(\d+):(A|R|[a-z]+)', rulestr)[0]
            rule = Rule(attr, int(num), gt == '>', to)
        workflows[name].append(rule)

parts = []
for partstr in ps.split('\n'):
    part = {}
    for attr, num in re.findall('([xmas])=(\d+)', partstr):
        part[attr] = int(num)
    parts.append(part)

accepted = 0
for part in parts:
    cur = 'in'

    going = True
    while going:
        for rule in workflows[cur]:
            if rule.check(part):
                if rule.to == 'R':
                    going = False
                    break
                elif rule.to == 'A':
                    going = False
                    accepted += sum(part.values())
                    break
                else:
                    cur = rule.to
                    break
print(accepted)


def createBranches(rulename, prange=PartRange.new()):
    if rulename == 'A':
        return prange.get_posses()
    if rulename == 'R':
        return 0

    accepted = 0
    for rule in workflows[rulename]:
        good, prange = prange.split(rule)
        if good:
            accepted += createBranches(rule.to, good)
        if not prange:
            break
    return accepted


print(createBranches('in'))
