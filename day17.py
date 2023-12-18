from collections import defaultdict
from functools import cache
from typing import NamedTuple

import networkx
import numpy as np

inp = open('day17.txt').read().strip()

grid = np.array([[int(val) for val in line] for line in inp.split('\n')])

# @cache
# def build_lasts(cur, dir):
#     return [(cur[0] + dir[0] * x, cur[1] + dir[1] * x) for x in range(1, 4)]
#
#
# best = 99999999999999
#
#
# @cache
# def find_shortest(frm: tuple[int, int], to: tuple[int, int], sofar=0, past=None) -> int:
#     global best
#
#     if past is None:
#         past = ()
#
#     if frm == to:
#         if sofar < best:
#             print(sofar)
#             best = sofar
#         return 0
#
#     sofar += grid[*frm]
#     if frm in past or best < sofar:
#         return 99999999999
#     poss = []
#
#     if frm[0] != 0 and past[-3:] != build_lasts(frm, (1, 0)):
#         poss.append(find_shortest((frm[0] - 1, frm[1]), to, sofar, (*past, frm)))
#     if frm[0] != len(grid) - 1 and past[-3:] != build_lasts(frm, (-1, 0)):
#         poss.append(find_shortest((frm[0] + 1, frm[1]), to, sofar, (*past, frm)))
#     if frm[1] != 0 and past[-3:] != build_lasts(frm, (0, 1)):
#         poss.append(find_shortest((frm[0], frm[1] - 1), to, sofar, (*past, frm)))
#     if frm[1] != len(grid[0]) - 1 and past[-3:] != build_lasts(frm, (0, -1)):
#         poss.append(find_shortest((frm[0], frm[1] + 1), to, sofar, (*past, frm)))
#     return min(poss, default=0) + grid[*frm]
#
#
# print(find_shortest((0, 0), (len(grid) - 1, len(grid[0]) - 1)))

# class CtxPos(NamedTuple):
#     pos: tuple[int, int]
#     ctx: tuple[str, int]
#     past: list[tuple[int, int]]
#     dist: int
#
#     def move(self, dir) -> 'CtxPos | None':
#         if self.ctx[0] == dir:
#             new_ctx = (dir, self.ctx[1] + 1)
#         else:
#             new_ctx = (dir, 1)
#         match dir:
#             case 'U':
#                 new_pos = (self.pos[0] - 1, self.pos[1])
#             case 'D':
#                 new_pos = (self.pos[0] + 1, self.pos[1])
#             case 'L':
#                 new_pos = (self.pos[0], self.pos[1] - 1)
#             case 'R':
#                 new_pos = (self.pos[0], self.pos[1] + 1)
#             case _:
#                 raise Exception()
#
#         if new_ctx[1] > 3 \
#                 or not (0 <= new_pos[0] < len(grid)) \
#                 or not (0 <= new_pos[1] < len(grid[0])) \
#                 or opposites[dir] == self.ctx[0]:
#             return None
#
#         return CtxPos(new_pos, new_ctx, [*self.past, self.pos], self.dist + grid[*new_pos])


# cell_data = defaultdict(lambda: defaultdict(lambda: 99999999999))
# start = CtxPos((0, 0), ('X', 0), [], 0)
# queue = [start]
# known = 0
# frontier = 1
# best = 99999999999
#
# while queue:
#     cur = queue.pop()
#     if cur.dist > best:
#         continue
#     nexts = [out for d in 'UDLR' if (out := cur.move(d))]
#     for poss in nexts:
#         better = True
#         for dist in range(1, poss.ctx[1] + 1):
#             if cell_data[poss.pos][poss.ctx] <= poss.dist:
#                 better = False
#         if better:
#             cell_data[poss.pos][poss.ctx] = poss.dist
#             queue.append(poss)
#         if poss.pos == (len(grid) - 1, len(grid[0]) - 1):
#             if poss.dist < best:
#                 # print('---')
#                 new_grid = np.zeros(grid.shape, dtype=int)
#                 for old_pos in poss.past:
#                     new_grid[*old_pos] = 1
#                 # print('\n'.join(''.join(map(str, line)) for line in new_grid))
#                 best = poss.dist
#                 print(best)
# print(best)

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

graph = networkx.DiGraph()

for x in range(len(grid)):
    for y in range(len(grid[0])):
        for dir in dirs:
            for count in range(1, 4):
                graph.add_node((x, y, dir, count))

for x, y, dir, count in graph.nodes:
    legal_dirs = [ndir for ndir in dirs if ndir != (-dir[0], -dir[1])]
    legal_dirs = [ndir for ndir in legal_dirs
                  if (0 <= x + ndir[0] < len(grid))
                  and (0 <= y + ndir[1] < len(grid[0]))]
    if count == 3 and dir in legal_dirs:
        legal_dirs.remove(dir)
    for ndir in legal_dirs:
        graph.add_edge((x, y, dir, count),
                       (x+ndir[0], y+ndir[1], ndir, 1 if ndir != dir else count+1),
                       weight=grid[x+ndir[0], y+ndir[1]])

start = (0, 0, None, 0)
graph.add_node(start)
graph.add_edge(start, (1, 0, (1, 0), 1), weight=grid[1, 0])
graph.add_edge(start, (0, 1, (0, 1), 1), weight=grid[0, 1])

# print(graph[(1, 0, (1, 0), 1)])
#{mid for mid, atlas in graph[monster.monster_id].items() for edge in atlas.values()}


def calc_path(path):
    last = path.pop(0)
    dist = 0
    for node in path:
        dist += graph.edges[last, node]['weight']
        last = node
    return dist

endpos = (len(grid) - 1, len(grid[0]) - 1)
best = 9999999999
for dir in dirs:
    for count in range(1, 4):
        print(dir, count)
        try:
            path = networkx.dijkstra_path(graph, start, (*endpos, dir, count))
            best = min(best, calc_path(path))
        except networkx.exception.NetworkXNoPath:
            pass
print(best)

graph = networkx.DiGraph()

for x in range(len(grid)):
    for y in range(len(grid[0])):
        for dir in dirs:
            for count in range(1, 11):
                graph.add_node((x, y, dir, count))

for x, y, dir, count in graph.nodes:
    legal_dirs = [ndir for ndir in dirs if ndir != (-dir[0], -dir[1])]
    legal_dirs = [ndir for ndir in legal_dirs
                  if (0 <= x + ndir[0] < len(grid))
                  and (0 <= y + ndir[1] < len(grid[0]))]
    if count == 10 and dir in legal_dirs:
        legal_dirs.remove(dir)
    elif count < 4:
        if dir in legal_dirs:
            legal_dirs = [dir]
        else:
            legal_dirs = []
    for ndir in legal_dirs:
        graph.add_edge((x, y, dir, count),
                       (x+ndir[0], y+ndir[1], ndir, 1 if ndir != dir else count+1),
                       weight=grid[x+ndir[0], y+ndir[1]])

start = (0, 0, None, 0)
graph.add_node(start)
graph.add_edge(start, (1, 0, (1, 0), 1), weight=grid[1, 0])
graph.add_edge(start, (0, 1, (0, 1), 1), weight=grid[0, 1])

# print(graph[(1, 0, (1, 0), 1)])
#{mid for mid, atlas in graph[monster.monster_id].items() for edge in atlas.values()}


def calc_path(path):
    last = path.pop(0)
    dist = 0
    for node in path:
        dist += graph.edges[last, node]['weight']
        last = node
    return dist

endpos = (len(grid) - 1, len(grid[0]) - 1)
best = 9999999999
for dir in [(0, 1), (1, 0)]:
    for count in range(4, 11):
        print(dir, count)
        try:
            path = networkx.dijkstra_path(graph, start, (*endpos, dir, count))
            best = min(best, calc_path(path))
        except networkx.exception.NetworkXNoPath:
            pass
print(best)
