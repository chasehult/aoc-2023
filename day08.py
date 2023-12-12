import math

import numpy as np

x = open('day8.txt').read().strip()

direction, maps = x.split('\n\n')

paths = {}
for line in maps.split('\n'):
    name, lr = line.split(' = ')
    l, r = lr[1:-1].split(', ')
    paths[name] = (l, r)

steps = 0
cur = 'AAA'
while cur != 'ZZZ':
    path = paths[cur]
    d = direction[steps % len(direction)]
    cur = path[0] if d == 'L' else path[1]
    steps += 1
print(steps)

# steps = 0
# curs = np.array([n for n in paths if n.endswith('A')])
# seens = [set() for _ in curs]
# test_num = 5
# try:
#     while not all(n.endswith('Z') for n in curs):
#         for i, c in enumerate(curs):
#             seens[i].add(c)
#         if curs[test_num].endswith('Z'):
#             print(steps, curs[test_num])
#         nextcurs = []
#         d = direction[steps % len(direction)]
#         for cur in curs:
#             path = paths[cur]
#             nextcurs.append(path[0] if d == 'L' else path[1])
#         steps += 1
#         curs = nextcurs
# except KeyboardInterrupt:
#     print(seens)
# print(steps)

# I feel like this code wouldn't *always* work, but it worked for me
curs = np.array([n for n in paths if n.endswith('A')])
loop_time: list[int | None] = [None for _ in curs]
steps = 0
while not all(loop_time):
    for i, c in enumerate(curs):
        if c.endswith('Z') and loop_time[i] is None:
            loop_time[i] = steps
    nextcurs = []
    d = direction[steps % len(direction)]
    for cur in curs:
        path = paths[cur]
        nextcurs.append(path[0] if d == 'L' else path[1])
    steps += 1
    curs = nextcurs

lcm = 1
for t in loop_time:
    lcm = math.lcm(lcm, t)
print(lcm)
