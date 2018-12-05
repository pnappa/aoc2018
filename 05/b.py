
x = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        x = list(line.strip())

def ispolar(a,b):
    if a is None or b is None:
        return False
    if a == b:
        return False
    if a.isupper() == b.isupper():
        return False
    return abs(ord(b)-ord(a)) == 32

master_x = list(x)

import string
lower = string.ascii_lowercase
upper = string.ascii_uppercase

for tup in zip(lower, upper):
    x = [a for a in master_x if a not in tup]
    while True:
        x = [a for a in x if a is not None]
        for index in range(len(x)-1):
            if ispolar(x[index], x[index+1]):
                x[index] = None
                x[index+1] = None
        if x.count(None) == 0:
            break
    print("for removing:", tup, "length is:", len(x))

print(len(x))
