import re

import numpy as np

inp = open('day18.txt').read().strip()


grid = np.full((1000, 1000), None, dtype=object)

start = cur = (500, 500)

for d, l, _ in re.findall(r'([UDLR]) (\d+) \(#([\dabcdef]{6})\)', inp):
    for _ in range(int(l)):
        match d:
            case 'U':
                grid[*cur] = 'U'
                cur = (cur[0]-1, cur[1])
                grid[*cur] = 'U'
            case 'D':
                grid[*cur] = 'D'
                cur = (cur[0]+1, cur[1])
                grid[*cur] = 'D'
            case 'L':
                cur = (cur[0], cur[1]-1)
                if grid[*cur] is None:
                    grid[*cur] = 1
            case 'R':
                cur = (cur[0], cur[1]+1)
                if grid[*cur] is None:
                    grid[*cur] = 1
assert start == cur
grid = np.transpose(grid[np.sum(grid != None,1) != 0])
grid = np.transpose(grid[np.sum(grid != None,1) != 0])
# print('\n'.join(''.join(map(lambda x: 'O' if x is True else '#' if x else ' ', line)) for line in grid))
oldgrid = grid.copy()
for r in range(len(grid)):
    fill = False
    wasjusttrue = None
    for c, val in enumerate(grid[r]):
        if grid[r, c] in ('U', 'D') and wasjusttrue != grid[r, c]:
            fill = not fill
        if fill:
            grid[r, c] = grid[r, c] or 1
        wasjusttrue = oldgrid[r, c] if grid[r, c] != 1 else wasjusttrue
        # print(r, c, fill, wasjusttrue, grid[r, c])

#print()
#print('\n'.join(''.join(map(lambda x: '#' if x else ' ', line)) for line in grid))

print((grid != None).sum())


start = cur = (0, 0)
points = [cur]
total_l = 0
for d, l, c in re.findall(r'([UDLR]) (\d+) \(#([\dabcdef]{6})\)', inp):
    d = 'RDLU'[int(c[-1])]
    l = int(c[:-1], 16)
    total_l += l
    match d:
        case 'U':
            cur = (cur[0]-l, cur[1])
        case 'D':
            cur = (cur[0]+l, cur[1])
        case 'L':
            cur = (cur[0], cur[1]-l)
        case 'R':
            cur = (cur[0], cur[1]+l)
    points.append(cur)
assert start == cur
total = 0
for i in range(len(points) - 2):
    total += points[i][0]*points[i + 1][1] - points[i + 1][0]*points[i][1]
# shoelace + pick
print((total_l // 2) + abs(total // 2) - 1 + 2)  # why +2???
