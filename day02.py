x = open('day2.txt').read()

total = 0
for line in x.split('\n'):
    if not line:
        continue
    gno, cubes = line.split(': ')
    lid = int(gno[5:])

    works = True
    for pull in cubes.split('; '):
        v = {'blue': 0, 'red': 0, 'green': 0}
        for color in pull.split(', '):
            n, c = color.split(' ')
            v[c] += int(n)
        if not (v['red'] <= 12 and v['green'] <= 13 and v['blue'] <= 14):
            works = False
    if works:
        total += lid
print(total)

total = 0
for line in x.split('\n'):
    if not line:
        continue
    gno, cubes = line.split(': ')
    lid = int(gno[5:])

    v = {'blue': 0, 'red': 0, 'green': 0}
    for pull in cubes.split('; '):
        for color in pull.split(', '):
            n, c = color.split(' ')
            v[c] = max(v[c], int(n))
    total += v['blue'] * v['red'] * v['green']
print(total)
