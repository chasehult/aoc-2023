from collections import defaultdict

inp = open('day15.txt').read().strip()


def get_hash(s):
    cur = 0
    for c in s:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


total = 0
for s in inp.split(','):
    total += get_hash(s)
print(total)

hm = defaultdict(dict)
for s in inp.split(','):
    if '=' in s:
        l, v = s.split('=')
        hm[get_hash(l)][l] = int(v)
    if '-' in s:
        l = s[:-1]
        if l in hm[get_hash(l)]:
            del hm[get_hash(l)][l]

total = 0
for h, box in hm.items():
    for c, leng in enumerate(box.values()):
        total += (h+1) * (c+1) * leng
print(total)
