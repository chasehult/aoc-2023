import re

x = open('day1.txt').read()

t = 0
for line in x.split('\n'):
    if not line:
        continue
    first = re.search(r'\d', line).group(0)
    last = re.search(r'\d', line[::-1]).group(0)
    t += int(first + last)
print(t)


nums = 'zero one two three four five six seven eight nine 0 1 2 3 4 5 6 7 8 9'.split()

t = 0
for line in x.split('\n'):
    if not line:
        continue
    first = re.search('|'.join(nums), line).group(0)
    last = re.search(r'.*(' + '|'.join(nums) + ')',  line).group(1)
    t += int(str(nums.index(first) % 10) + str(nums.index(last) % 10))
print(t)
