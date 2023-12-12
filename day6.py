import re

x = open('day6.txt').read()

time, distance, *_ = x.split('\n')
time = [*map(int, re.sub(r' +', ' ', time[10:]).strip().split(' '))]
distance = [*map(int, re.sub(r' +', ' ', distance[10:]).strip().split(' '))]

prod = 1
for t, d in zip(time, distance):
    num_more = 0
    for c_time in range(t):
        made_dist = c_time * (t - c_time)
        if made_dist > d:
            num_more += 1
    prod *= num_more
print(prod)

time, distance, *_ = x.split('\n')
time = int(time[10:].replace(' ', ''))
distance = int(distance[10:].replace(' ', ''))

# Find lower bound
lower, upper = 0, time
while True:
    mid = (lower + upper) // 2
    midp1 = mid + 1
    mid_makes = mid * (time - mid) > distance
    midp1_makes = midp1 * (time - midp1) > distance
    if mid_makes and midp1_makes:
        upper = mid
    elif not mid_makes and not midp1_makes:
        lower = mid
    else:
        lower_bound = mid
        break

lower, upper = 0, time
while True:
    mid = (lower + upper) // 2
    midp1 = mid + 1
    mid_makes = mid * (time - mid) > distance
    midp1_makes = midp1 * (time - midp1) > distance
    if mid_makes and midp1_makes:
        lower = mid
    elif not mid_makes and not midp1_makes:
        upper = mid
    else:
        upper_bound = mid
        break

print(upper_bound - lower_bound)
