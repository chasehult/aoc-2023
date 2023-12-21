import sys

import numpy as np

inp = open('day21.txt').read().strip()

steps = 26501365
# poses = np.array([[True if char == 'S' else False for char in line] for line in inp.split('\n')])
# walls = np.array([[True if char != '#' else False for char in line] for line in inp.split('\n')])
#
# for _ in range(64):
#     new_poses = np.full(poses.shape, False)
#     for x in range(len(poses)):
#         for y in range(len(poses[0])):
#             for xo in (-1, 0, 1):
#                 for yo in (-1, 0, 1):
#                     if 0 not in (xo, yo) or xo == yo == 0 \
#                             or not (0 <= x + xo < len(poses)) \
#                             or not (0 <= y + yo < len(poses[0])):
#                         continue
#                     if poses[x + xo][y + yo]:
#                         new_poses[x][y] = True
#     new_poses &= walls
#     poses = new_poses
#
# print(poses.sum())


# poses = np.array([[{0} if char == 'S' else set() for char in line]
#                   for line in inp.split('\n')], dtype=object)
# walls = np.array([[True if char == '#' else False for char in line]
#                   for line in inp.split('\n')])
# print(poses.shape)
# for _ in range(steps):
#     new_poses = np.array([[set() for _ in range(len(poses[0]))]
#                           for _ in range(len(poses))])
#     for x in range(len(poses)):
#         for y in range(len(poses[0])):
#             if (vals := poses[x, y]):
#                 if x + 1 == len(poses):
#                     new_poses[0, y].update({v + 1 for v in poses[x, y]})
#                 else:
#                     new_poses[x + 1, y].update(poses[x, y])
#                 if x - 1 == -1:
#                     new_poses[len(poses) - 1, y].update({v - 1 for v in poses[x, y]})
#                 else:
#                     new_poses[x - 1, y].update(poses[x, y])
#                 if y + 1 == len(poses[0]):
#                     new_poses[x, 0].update({v + 1j for v in poses[x, y]})
#                 else:
#                     new_poses[x, y + 1].update(poses[x, y])
#                 if y - 1 == -1:
#                     new_poses[x, len(poses[0]) - 1].update({v - 1j for v in poses[x, y]})
#                 else:
#                     new_poses[x, y - 1].update(poses[x, y])
#     new_poses[walls] = set()
#     poses = new_poses
#
# # print('\n'.join(''.join(str(len(poses[x][y])) if poses[x][y]
# #                         else '#' if walls[x][y] else '.'
# #                         for y in range(len(poses[0]))) for x in range(len(poses))))
# print(np.vectorize(len)(poses).sum())

walls = np.array([[True if char != '#' else False for char in line] for line in inp.split('\n')])
posses = np.array([[True if char == 'S' else False for char in line] for line in inp.split('\n')])
old = np.zeros(posses.shape)

while (old != posses).any():
    old = posses
    new_posses = posses.copy()
    for x in range(len(posses)):
        for y in range(len(posses[0])):
            if posses[x, y]:
                for xo in (-1, 0, 1):
                    for yo in (-1, 0, 1):
                        if 0 not in (xo, yo) or xo == yo == 0 \
                                or not (0 <= x + xo < len(posses)) \
                                or not (0 <= y + yo < len(posses[0])):
                            continue
                        new_posses[x + xo][y + yo] = True
    new_posses &= walls
    posses = new_posses

allowed = posses

order = (steps - (len(posses) // 2)) // len(posses)
odd_parity_mask = np.array([[(x + y) % 2 == 0 for y in range(len(posses[0]))] for x in range(len(posses))])
tl_triangle_mask = np.array([[(x + y) < (len(posses) // 2) for y in range(len(posses[0]))] for x in range(len(posses))])

inv = np.vectorize(lambda v: not v)


def repr_mask(mask):
    return '\n'.join(''.join('#' if val else '.' for val in line) for line in mask)


total = 0

# Tips
tip_mask = inv(odd_parity_mask) & inv(tl_triangle_mask) & np.rot90(inv(tl_triangle_mask))
for rot in range(4):
    total += (allowed & tip_mask).sum()
    tip_mask = np.rot90(tip_mask)

# Chunks
tri_mask = tl_triangle_mask.copy()
for rot in range(4):
    total += (allowed & odd_parity_mask & tri_mask).sum() * (order)
    total += (allowed & inv(odd_parity_mask) & inv(tri_mask)).sum() * (order - 1)
    tri_mask = np.rot90(tri_mask)

total += (allowed & odd_parity_mask).sum() * order ** 2
total += (allowed & inv(odd_parity_mask)).sum() * (order - 1) ** 2
print(total)
