x = open('day9.txt').read().strip()

nums = []
for line in x.split('\n'):
    nums.append([int(v) for v in line.split(' ') if v])

total = totalb = 0
for seq in nums:
    seqs = [seq]
    while any(seqs[-1]):
        newseq = []
        for x in range(len(seqs[-1])-1):
            newseq.append(seqs[-1][x+1] - seqs[-1][x])
        seqs.append(newseq)

    cur = curb = 0
    for seq in seqs[::-1]:
        cur += seq[-1]
        curb = seq[0] - curb
    total += cur
    totalb += curb
print(total)
print(totalb)
