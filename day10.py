import re

x = open('day10.txt').read().strip()

grid = x.split('\n')
grid2 = [*map(list, grid[:])]
animal_pos = None
for i, row in enumerate(grid):
    if 'S' in row:
        animal_pos = i, row.index('S')
assert animal_pos is not None

pos = animal_pos
total_len = 0
dire = (0, 1)
outside = (1, 0)
while True:
    match grid[pos[0]][pos[1]]:
        case '-':
            dire = dire
        case 'S':
            dire = dire
        case '|':
            dire = dire
        case 'F':
            if dire == (-1, 0):
                dire = (0, 1)
            else:
                dire = (1, 0)
        case 'J':
            if dire == (1, 0):
                dire = (0, -1)
            else:
                dire = (-1, 0)
        case '7':
            if dire == (-1, 0):
                dire = (0, -1)
            else:
                dire = (1, 0)
        case 'L':
            if dire == (1, 0):
                dire = (0, 1)
            else:
                dire = (-1, 0)

    pos = pos[0] + dire[0], pos[1] + dire[1]
    grid2[pos[0]][pos[1]] = 'S'
    total_len += 1
    if pos == animal_pos:
        break

print(total_len // 2)

grid = [*map(list, grid[:])]
for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid2[x][y] != 'S':
            grid[x][y] = '.'

pos = animal_pos
dire = (0, 1)
outside = (1, 0)
outside_dir = -1j
while True:
    outside = (dire[0] + dire[1] * 1j) * outside_dir
    outside = int(outside.real), int(outside.imag)
    if 0 <= pos[0] + outside[0] < len(grid) \
            and 0 <= pos[1] + outside[1] < len(grid[0]) \
            and grid[pos[0] + outside[0]][pos[1] + outside[1]] == '.':
        grid[pos[0] + outside[0]][pos[1] + outside[1]] = 'V'
    match grid[pos[0]][pos[1]]:
        case '-':
            dire = dire
        case 'S':
            dire = dire
        case '|':
            dire = dire
        case 'F':
            if dire == (-1, 0):
                dire = (0, 1)
            else:
                dire = (1, 0)
        case 'J':
            if dire == (1, 0):
                dire = (0, -1)
            else:
                dire = (-1, 0)
        case '7':
            if dire == (-1, 0):
                dire = (0, -1)
            else:
                dire = (1, 0)
        case 'L':
            if dire == (1, 0):
                dire = (0, 1)
            else:
                dire = (-1, 0)

    outside = (dire[0] + dire[1] * 1j) * outside_dir
    outside = int(outside.real), int(outside.imag)
    if 0 <= pos[0] + outside[0] < len(grid) \
            and 0 <= pos[1] + outside[1] < len(grid[0]) \
            and grid[pos[0] + outside[0]][pos[1] + outside[1]] == '.':
        grid[pos[0] + outside[0]][pos[1] + outside[1]] = 'V'
    pos = pos[0] + dire[0], pos[1] + dire[1]
    grid2[pos[0]][pos[1]] = 'S'
    total_len += 1
    if pos == animal_pos:
        break

for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x][y] == 'V':
            for xo in (-1, 0, 1):
                for yo in (-1, 0, 1):
                    if 0 <= x + xo < len(grid) \
                            and 0 <= y + yo < len(grid[0]) \
                            and grid[x + xo][y + yo] == '.':
                        grid[x + xo][y + yo] = 'V'

print('\n'.join(''.join(line) for line in grid).count('V'))
