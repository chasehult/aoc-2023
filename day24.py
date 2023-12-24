from os import urandom

import numpy as np
from z3 import z3

inp = open('day24.txt').read().strip()

TEST_AREA_MIN = 200000000000000
TEST_AREA_MAX = 400000000000000


class Hail:
    def __init__(self, p, v):
        self.px, self.py, self.pz = p
        self.vx, self.vy, self.vz = v
        self.p = np.array(p)
        self.v = np.array(v)

    def __contains__(self, other: 'Hail'):
        sm = (self.vy / self.vx)
        om = (other.vy / other.vx)
        sb = self.py - sm * self.px
        ob = other.py - om * other.px
        if (sm - om) == 0:
            return False

        x = (ob - sb) / (sm - om)
        y = sm * x + sb

        if (x - self.px) / self.vx < 0:
            return False
        if (x - other.px) / other.vx < 0:
            return False
        return TEST_AREA_MIN <= x <= TEST_AREA_MAX and TEST_AREA_MIN <= y <= TEST_AREA_MAX

    def collides_with(self, other: 'Hail'):
        if self.vx == other.vx:
            return other.px == self.px
        t = (other.px - self.px) / (self.vx - other.vx)
        if t < 0:
            return False
        return t == (other.py - self.py) / (self.vy - other.vy) == (other.pz - self.pz) / (self.vz - other.vz)

    def closest(self, other: 'Hail') -> float:
        pd = other.p - self.p
        vr = self.v - other.v
        dp = pd.dot(vr)
        print(dp)


    def __repr__(self):
        return f'Hail<{self.px}, {self.py}, {self.pz}, {self.vx}, {self.vy}, {self.vz}>'

    def __hash__(self):
        return hash((self.px, self.py, self.pz, self.vx, self.vy, self.vz))


class Rock(Hail):
    ...


hails = []
for line in inp.split('\n'):
    p, v = line.split(' @ ')
    p = [int(x) for x in p.split(', ')]
    v = [int(x) for x in v.split(', ')]
    hails.append(Hail(p, v))

total = 0
for i, h1 in enumerate(hails):
    for h2 in hails[i + 1:]:
        if h1 in h2:
            total += 1
print(total)

px = z3.Int('px')
py = z3.Int('py')
pz = z3.Int('pz')
vx = z3.Int('vx')
vy = z3.Int('vy')
vz = z3.Int('vz')

s = z3.Solver()

for c, hail in enumerate(hails[:3]):
    t = z3.Int(f't{c}')
    s.add(hail.vx * t + hail.px == vx * t + px)
    s.add(hail.vy * t + hail.py == vy * t + py)
    s.add(hail.vz * t + hail.pz == vz * t + pz)

s.check()
model = s.model()

print(sum(model[val].as_long() for val in [px, py, pz]))
