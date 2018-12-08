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

    has_children = num_children > 0
    potential_sum = []
    for i in range(num_children):
        potential_sum.append(sum_metadata(tree))

    sum_meta = 0
    if has_children:
        for i in range(amount_metadata):
            e = pop_first(tree)
            if e in range(1, num_children+1):
                sum_meta += potential_sum[e-1]
    else:
        for i in range(amount_metadata):
            sum_meta += pop_first(tree)

    return sum_meta


print(sum_metadata(x))


