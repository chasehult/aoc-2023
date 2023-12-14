import numpy as np

inp = open('day13_test.txt').read().strip()

total = 0
for terr in inp.split('\n\n'):
    terr = np.array([*map(list, terr.split('\n'))])
    for r in range(1, len(terr)):
        for ro in range(min(r, len(terr)-r)):
            if (terr[r+ro] != terr[r-ro-1]).any():
                break
        else:
            total += 100*r
    for c in range(1, len(terr[0])):
        for co in range(min(c, len(terr[0])-c)):
            if (terr[:,c+co] != terr[:,c-co-1]).any():
                break
        else:
            total += c
print(total)

total = 0
for terr in inp.split('\n\n'):
    terr = np.array([*map(list, terr.split('\n'))])
    for r in range(1, len(terr)):
        smdgs = 0
        for ro in range(min(r, len(terr)-r)):
            smdgs += (terr[r+ro] != terr[r-ro-1]).sum()
        if smdgs == 1:
            total += 100 * r
    for c in range(1, len(terr[0])):
        smdgs = 0
        for co in range(min(c, len(terr[0])-c)):
            smdgs += (terr[:,c+co] != terr[:,c-co-1]).sum()
        if smdgs == 1:
            total += c
print(total)
