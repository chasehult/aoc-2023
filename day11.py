import numpy as np

inp = open('day11.txt').read().strip()

space = np.array([[int(v == '.') for v in line] for line in inp.split('\n')])

r_spaces = []
for r in range(len(space)):
    if space[r].all():
        r_spaces.append(r)

c_spaces = []
for c in range(len(space[0])):
    if space[:, c].all():
        c_spaces.append(c)

print(r_spaces, c_spaces)

galaxies = []
for x in range(len(space)):
    for y in range(len(space[0])):
        if not space[x][y]:
            galaxies.append((x, y))


def calc(expan):
    total = 0
    for c1, (g1x, g1y) in enumerate(galaxies):
        for c2, (g2x, g2y) in enumerate(galaxies[c1+1:], c1+1):
            dist = abs(g1x - g2x) + abs(g1y - g2y)
            for r in range(min(g1x, g2x), max(g1x, g2x)):
                if r in r_spaces:
                    dist += expan - 1
            for c in range(min(g1y, g2y), max(g1y, g2y)):
                if c in c_spaces:
                    dist += expan - 1
            total += dist
    return total

print(calc(2))
print(calc(1000000))
