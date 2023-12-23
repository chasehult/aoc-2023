import re
import uuid
from collections import defaultdict
from copy import copy, deepcopy
from typing import Literal

inp = open('day22.txt').read().strip()


class Range:
    def __init__(self, frm: int, to: int):
        self.frm = min(frm, to)
        self.to = max(frm, to)

    def __contains__(self, other: 'int | Range'):
        if isinstance(other, int):
            return self.frm <= other <= self.to
        else:
            return not (self.to < other.frm or other.to < self.frm)

    def __add__(self, other: int):
        return Range(self.frm + other, self.to + other)

    def __sub__(self, other: int):
        return Range(self.frm - other, self.to - other)

    def __repr__(self):
        return f'[{self.frm}, {self.to}]'

    def __copy__(self):
        return Range(self.frm, self.to)

    def __eq__(self, other: 'Range'):
        return self.frm == other.frm and self.to == other.to

    def __hash__(self):
        return hash((self.frm, self.to))


class Block:
    def __init__(self, x: Range, y: Range, z: Range, id: uuid.UUID = None):
        self.x = x
        self.y = y
        self.z = z
        self.id = id or uuid.uuid4()

    def change_attr(self, attr: Literal['x', 'y', 'z'], val: int) -> 'Block':
        match attr:
            case 'x':
                return Block(self.x + val, self.y, self.z)
            case 'y':
                return Block(self.x, self.y + val, self.z)
            case 'z':
                return Block(self.x, self.y, self.z + val)
            case _:
                raise Exception(attr)

    def __contains__(self, item: 'Block'):
        assert isinstance(item, Block)
        return (self.x in item.x and self.y in item.y and self.z in item.z)

    def __repr__(self):
        return f'Block<{self.x}, {self.y}, {self.z}>'

    def __copy__(self):
        return Block(copy(self.x), copy(self.y), copy(self.z), self.id)

    def __eq__(self, other: 'Block'):
        return self.id == other.id and self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(self.id)


blocks = []
for line in inp.split('\n'):
    xf, yf, zf, xt, yt, zt = re.fullmatch(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line).groups()
    blocks.append(Block(Range(int(xf), int(xt)),
                        Range(int(yf), int(yt)),
                        Range(int(zf), int(zt))))


def fall(blocks):
    blocks = deepcopy(blocks)
    oldblocks = None
    while blocks != oldblocks:
        oldblocks = [copy(block) for block in blocks]
        for block in blocks:
            if 1 in block.z:
                continue
            block.z -= 1
            for other_block in blocks:
                if block == other_block:
                    continue
                if block in other_block:
                    block.z += 1
                    break
    return blocks


def does_fall(blocks):
    newblocks = deepcopy(blocks)
    for block in newblocks:
        if 1 in block.z:
            continue
        block.z += -1
        for other_block in newblocks:
            if block is other_block:
                continue
            if block in other_block:
                block.z += 1
                break
        else:
            return True
    return False


blocks = fall(blocks)
print("Finished initial fall")

total = 0
for i, block in enumerate(blocks):
    blocks.remove(block)
    if not does_fall(blocks):
        total += 1
    blocks.insert(i, block)
print(total)

# def num_affected(blocks):
#     newblocks = deepcopy(blocks)
#     moved = set()
#     for block in newblocks:
#         if 1 in block.z:
#             continue
#         block.z += -1
#         for other_block in newblocks:
#             if block == other_block:
#                 continue
#             if block in other_block:
#                 block.z += 1
#                 break
#         else:
#             moved.add(block.id)
#     return len(moved)
#
#
# total = 0
# for i, block in enumerate(blocks):
#     if i % 10 == 0:
#         print(i)
#     blocks.remove(block)
#     total += num_affected(blocks)
#     blocks.insert(i, block)
# print(total)

supported = defaultdict(set)
for block in blocks:
    block.z -= 1
    for block2 in blocks:
        if block == block2:
            continue
        if block in block2:
            supported[block].add(block2)
    block.z += 1


def get_falls(block):
    seen = {block}
    last = None
    while seen != last:
        last = copy(seen)
        for block2, supports in supported.items():
            if not (supports - seen):
                seen.add(block2)
    return len(seen) - 1


total = 0
for i, block in enumerate(blocks):
    if i % 10 == 0:
        print(i)
    falls = get_falls(block)
    total += falls
print(total)
