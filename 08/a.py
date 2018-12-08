import string

x = []
with open('input', 'r') as ifile:
    x = list(map(int, ifile.readline().strip().split(' ')))


def pop_first(l):
    r = l[0]
    l.remove(r)
    return r

def sum_metadata(tree):
    num_children = pop_first(tree)
    amount_metadata = pop_first(tree)

    sum_meta = 0
    for i in range(num_children):
        sum_meta += sum_metadata(tree)

    for i in range(amount_metadata):
        sum_meta += pop_first(tree)

    return sum_meta


print(sum_metadata(x))


