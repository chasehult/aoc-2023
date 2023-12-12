from collections import defaultdict
from typing import NamedTuple

x = open('day5.txt').read()

seeds, *groups = x.split('\n\n')
seeds = [*map(int, seeds[7:].split(' '))]


def first():
    maps = defaultdict(lambda: defaultdict(list))
    for group in groups:
        header, *lines = group.split('\n')
        from_c, _, to_c = header[:-5].split('-')
        for dst, src, rng in [map(int, l.split()) for l in lines if l]:
            maps[from_c][to_c].append((src, src + rng - 1, dst))

    cur = 'seed'
    curs = seeds[:]
    while cur != 'location':
        next_c = {*maps[cur].keys()}.pop()
        poss = []
        for cs in curs:
            matched = False
            for r_frm, r_to, dst in maps[cur][next_c]:
                if r_frm <= cs <= r_to:
                    poss.append(cs - r_frm + dst)
                    matched = True
            if not matched:
                poss.append(cs)
        curs = poss
        cur = next_c
    return min(curs)


print(first())


# print(maps['seed']['soil'])
# sranges = [(seeds[x], seeds[x]+seeds[x+1]-1) for x in range(0, len(seeds), 2)]
# cur = 'seed'
# curs = sranges[:]
# while cur != 'location':
#     next_c = {*maps[cur].keys()}.pop()
#     print(cur)
#     print(curs)
#     poss = []
#     for cs_frm, cs_to in curs:
#         print(cs_frm, cs_to)
#         assert cs_frm <= cs_to
#         matched = []
#         for r_frm, r_to, dst in maps[cur][next_c]:
#             if r_frm <= cs_frm and cs_to <= r_to:
#                 print('in', cs_frm, cs_to, r_frm, r_to, dst)
#                 poss.append((cs_frm-r_frm+dst, cs_to-r_frm+dst))
#                 matched.append((cs_frm, cs_to))
#             elif r_frm > cs_frm and cs_to > r_to:
#                 print('out', cs_frm, cs_to, r_frm, r_to, dst)
#                 poss.append((dst, r_to-r_frm+dst))
#                 matched.append((r_frm, r_to))
#             elif r_frm <= cs_frm <= r_to:
#                 print('frm', cs_frm, cs_to, r_frm, r_to, dst)
#                 poss.append((cs_frm-r_frm+dst, r_to-r_frm+dst))
#                 print(poss[-1])
#                 matched.append((cs_frm, r_to))
#             elif r_frm <= cs_to <= r_to:
#                 print('to', cs_frm, cs_to, r_frm, r_to, dst)
#                 poss.append((dst, cs_to-r_frm+dst))
#                 print(poss[-1])
#                 matched.append((r_frm, cs_to))
#         print('trns', poss)
#         print('matched', matched)
#         rngs = []
#         ign = 0
#         for c, (rng_frm, rng_to) in enumerate(sorted(matched)):
#             if ign:
#                 ign -= 1
#                 continue
#             newto = rng_to
#             for c2, (rng_frm2, rng_to2) in enumerate(sorted(matched[c:]), 1):
#                 if rng_frm2 < newto:
#                     if newto < rng_to2:
#                         newto = rng_to2
#                     ign = c2
#             rngs.append((rng_frm, newto))
#         print('new_matched', rngs)
#         last = cs_frm
#         for rng_frm, rng_to in rngs:
#             if not (last == cs_frm == rng_frm):
#                 poss.append((last, max(rng_frm-1, cs_frm)))
#             if cs_to <= rng_to:
#                 break
#             last = min(rng_to+1, cs_to)
#         else:
#             poss.append((last, cs_to))
#         print()
#     curs = list(set(poss))
#     cur = next_c
#
# print(curs)
# print(min(curs)[0])


class Range(NamedTuple):
    frm: int
    to: int

    def __add__(self, other):
        return Range(self.frm + other, self.to + other)

    @classmethod
    def from_offset(cls, frm, off):
        return cls(frm, frm + off - 1)


class Transformation(NamedTuple):
    rng: Range
    offset: int

    @classmethod
    def from_offset(cls, to, frm, off):
        return cls(Range.from_offset(frm, off), to-frm)


def do_transformation(rng: Range, trans: list[Transformation]) -> list[Range]:
    used = []
    new_ranges = []
    r_frm, r_to = rng
    for (t_frm, t_to), t_off in trans:
        if r_frm <= t_frm and t_to <= r_to:
            used_rng = Range(t_frm, t_to)
        elif r_frm > t_frm and t_to > r_to:
            used_rng = Range(r_frm, r_to)
        elif r_frm <= t_frm <= r_to:
            used_rng = Range(t_frm, r_to)
        elif r_frm <= t_to <= r_to:
            used_rng = Range(r_frm, t_to)
        else:
            continue
        new_ranges.append(used_rng + t_off)
        used.append(used_rng)

    # add unused x->x transforms
    last = r_frm
    for u_frm, u_to in sorted(used):
        if u_frm != r_frm:
            new_ranges.append(Range(last, u_frm - 1))
        last = u_to + 1
    if last <= r_to:
        new_ranges.append(Range(last, r_to))
    return new_ranges


def main():
    maps = defaultdict(list)
    next_cs = {}
    for group in groups:
        header, *lines = group.split('\n')
        from_c, _, to_c = header[:-5].split('-')
        next_cs[from_c] = to_c
        for trns in [map(int, l.split()) for l in lines if l]:
            maps[from_c].append(Transformation.from_offset(*trns))

    cur = 'seed'
    curs = [Range.from_offset(*seeds[x:x + 2]) for x in range(0, len(seeds), 2)]
    while cur != 'location':
        next_c = next_cs[cur]
        poss = []
        for cs in curs:
            poss.extend(do_transformation(cs, maps[cur]))
        curs = poss
        cur = next_c
    return min(curs, key=lambda x: x.frm)[0]


if __name__ == '__main__':
    print(main())
