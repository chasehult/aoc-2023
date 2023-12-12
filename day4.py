import re
from collections import defaultdict

x = open('day4.txt').read()

total = 0
for line in x.split('\n'):
    if not line:
        continue

    line = line[5:]
    c_num = int(re.match('\s*(\d+)', line).group(1))
    line = re.sub('^\s*\d+: +', '', line)
    line = re.sub(r' +', ' ', line)
    winning, nums = line.split(' | ')
    winning = [*map(int, winning.strip().split(' '))]
    nums = [*map(int, nums.strip().split(' '))]
    n = 0
    for num in nums:
        if num in winning:
            n += 1
    if n:
        total += 2 ** (n-1)

total = 0
mults = {n: 1 for n in range(1, len([*filter(None, x.split('\n'))]) + 1)}
for line in x.split('\n'):
    if not line:
        continue

    line = line[5:]
    c_num = int(re.match('\s*(\d+)', line).group(1))
    line = re.sub('^\s*\d+: +', '', line)
    line = re.sub(r' +', ' ', line)
    winning, nums = line.split(' | ')
    winning = [*map(int, winning.strip().split(' '))]
    nums = [*map(int, nums.strip().split(' '))]
    n = 0
    for num in nums:
        if num in winning:
            n += 1
    for o in range(n):
        mults[c_num+o+1] += mults[c_num]
print(sum(v for k, v in mults.items()))
