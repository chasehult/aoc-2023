import re

x = open('day3.txt').read()
splitted = [*filter(None, x.split('\n'))]

total = 0
for r, line in enumerate(splitted):
    for num in re.finditer(r'\d+', line):
        for c in range(max(0, num.start()-1),
                       min(len(splitted[0]), num.end()+1)):
            for ro in (-1, 0, 1):
                if 0 <= r + ro < len(splitted):
                    if splitted[r+ro][c] not in '0987654321.':
                        total += int(num.group(0))
print(total)


nums = []
for r, line in enumerate(splitted):
    for num in re.finditer(r'\d+', line):
        nums.append((r-1, r+1, num.start()-1, num.end(), int(num.group())))

total = 0
for r, line in enumerate(splitted):
    for c, char in enumerate(line):
        if char != '*':
            continue
        counted = []
        for rs, re, cs, ce, n in nums:
            if rs <= r <= re and cs <= c <= ce:
                counted.append(n)
        if len(counted) == 2:
            total += counted[0] * counted[1]

print(total)
