
from collections import Counter

def get_counts(counter):
    num_two = 0
    num_three = 0
    for v in counter.values():
        if v == 2:
            num_two += 1
        if v == 3:
            num_three += 1

    return num_two, num_three


num_three_count = 0
num_two_count = 0
with open('input', 'r') as ifile:
    for line in ifile:
        line = line.strip()
        l = Counter(line)
        res = get_counts(l)
        num_two_count += 1 if res[0] > 0 else 0
        num_three_count += 1 if res[1] > 0 else 0

print(num_two_count*num_three_count)

