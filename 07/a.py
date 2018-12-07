import string

x = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        fromV = line[5:6]
        toV = line[36:37]
        x.append((fromV, toV))

verts = string.ascii_uppercase

# build an adjacency list
ordering = {v:set() for v in verts}
# reverse adjacency list
rev_adjacency = {v:set() for v in verts}
for edge in x:
    ordering[edge[0]].add(edge[1])
    rev_adjacency[edge[1]].add(edge[0])

    
topo = []
# our queue is all vertices without incoming nodes
queue = [v for v in rev_adjacency if len(rev_adjacency[v]) == 0]
# alphabetical
queue.sort()
visited = set()
c_index = 0
while len(visited) < 26:
    c_node = verts[c_index]

    if c_node in visited:
        c_index += 1
        c_index %= len(verts)
        continue

    # if any precedessors haven't been visited, we ignore this vertex
    if any([False if pred in visited else True for pred in rev_adjacency[c_node]]):
        c_index += 1
        c_index %= len(verts)
        continue

    topo.append(c_node)
    visited.add(c_node)
    c_index = 0

print("".join(topo))
