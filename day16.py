from typing import NamedTuple

import numpy as np

inp = open('day16.txt').read().strip()

grid = np.array([list(line) for line in inp.split('\n')])


class Energy(NamedTuple):
    position: tuple[int, int]
    direction: tuple[int, int]


powered = np.zeros(grid.shape, dtype=int)
powered[0][0] = 1
energies = [Energy((0, 0), (1, 0))]
seens = []

while energies:
    pos, dir = energies.pop()
    if (pos, dir) in seens:
        continue
    seens.append((pos, dir))
    next_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if next_pos[0] < 0 or len(grid) <= next_pos[0] \
            or next_pos[1] < 0 or len(grid[0]) <= next_pos[1]:
        continue
    powered[*next_pos] = 1
    match grid[*next_pos]:
        case '.':
            energies.append(Energy(next_pos, dir))
        case '|':
            if dir[0]:
                energies.append(Energy(next_pos, dir))
            else:
                energies.append(Energy(next_pos, (1, 0)))
                energies.append(Energy(next_pos, (-1, 0)))
        case '-':
            if dir[1]:
                energies.append(Energy(next_pos, dir))
            else:
                energies.append(Energy(next_pos, (0, 1)))
                energies.append(Energy(next_pos, (0, -1)))
        case '/':
            energies.append(Energy(next_pos, (-dir[1], -dir[0])))
        case '\\':
            energies.append(Energy(next_pos, (dir[1], dir[0])))
print(powered.sum())


def get_powereds(start_pos, start_dir):
    seens = []
    powered = np.zeros(grid.shape)
    energies = [Energy(start_pos, start_dir)]

    while energies:
        pos, dir = energies.pop()
        if (pos, dir) in seens:
            continue
        seens.append((pos, dir))
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if next_pos[0] < 0 or len(grid) <= next_pos[0] \
                or next_pos[1] < 0 or len(grid[0]) <= next_pos[1]:
            continue
        powered[*next_pos] = 1
        match grid[*next_pos]:
            case '.':
                energies.append(Energy(next_pos, dir))
            case '|':
                if dir[0]:
                    energies.append(Energy(next_pos, dir))
                else:
                    energies.append(Energy(next_pos, (1, 0)))
                    energies.append(Energy(next_pos, (-1, 0)))
            case '-':
                if dir[1]:
                    energies.append(Energy(next_pos, dir))
                else:
                    energies.append(Energy(next_pos, (0, 1)))
                    energies.append(Energy(next_pos, (0, -1)))
            case '/':
                energies.append(Energy(next_pos, (-dir[1], -dir[0])))
            case '\\':
                energies.append(Energy(next_pos, (dir[1], dir[0])))
    return powered.sum()


m = 0
for r in range(len(grid)):
    a = get_powereds((r, -1), (0, 1))
    b = get_powereds((r, len(grid[0])), (0, -1))
    m = max(a, b, m)

for c in range(len(grid[0])):
    a = get_powereds((-1, c), (1, 0))
    b = get_powereds((len(grid), c), (-1, 0))
    m = max(a, b, m)

print(m)
