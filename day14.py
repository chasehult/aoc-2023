inp = open('day14.txt').read().strip()

tran = '\n'.join(''.join(line) for line in zip(*inp.split('\n')))
while '.O' in tran:
    tran = tran.replace('.O', 'O.')
rolled = [''.join(line) for line in zip(*tran.split('\n'))]
total = 0
for c, row in enumerate(rolled):
    total += (len(rolled) - c) * row.count('O')
print(total)

def cycle(inp_g):
    tran = '\n'.join(''.join(line) for line in zip(*inp_g.split('\n')))
    while '.O' in tran:
        tran = tran.replace('.O', 'O.')
    tran = '\n'.join(''.join(line) for line in zip(*tran.split('\n')))
    while '.O' in tran:
        tran = tran.replace('.O', 'O.')
    tran = '\n'.join(''.join(line[::-1]) for line in zip(*tran.split('\n')))
    while '.O' in tran:
        tran = tran.replace('.O', 'O.')
    tran = '\n'.join(''.join(line[::-1]) for line in zip(*tran.split('\n')))
    while '.O' in tran:
        tran = tran.replace('.O', 'O.')
    tran = '\n'.join(''.join(line[::-1]) for line in zip(*tran.split('\n')))
    tran = '\n'.join(''.join(line[::-1]) for line in zip(*tran.split('\n')))
    return tran

def get_load(inp):
    inp = inp.split('\n')
    total = 0
    for c, row in enumerate(inp):
        total += (len(inp) - c) * row.count('O')
    return total

inps = []

while inp not in inps:
    inps.append(inp)
    inp = cycle(inp)
offset = inps.index(inp)
leng = len(inps) - offset

inp = inps[offset:][(1000000000-offset) % leng]
print(get_load(inp))
