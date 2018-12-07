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
# our pool is all vertices without incoming nodes
pool = sorted([v for v in rev_adjacency if len(rev_adjacency[v]) == 0])
pool.sort(reverse=True)
for p in pool:
    del rev_adjacency[p]
num_avail_workers = 5

# current time left for each task
time_cost_vertices = {k: 60 + ord(k)-64 for k in verts}

visited = set()

c_jobs = []
visitd = set()
for second in range(0, 5000000):
    if len(c_jobs) == 0 and len(pool) == 0:
        break
    # assign any free workers to jobs
    while num_avail_workers > 0 and len(pool) > 0:
        j = pool.pop()
        c_jobs.append([j, time_cost_vertices[j]])
        visited.add(j)
        num_avail_workers -= 1

    # save the jobs we need to remove
    rem_pool = []
    # subtract 1 second from our current jobs
    for index, _ in enumerate(c_jobs):
        c_jobs[index][1] -= 1
        # if this job is finished, return the worker ot the pool
        if c_jobs[index][1] <= 0:
            num_avail_workers += 1
            rem_pool.append(c_jobs[index])

    # remove these finished jobs
    for r in rem_pool:
        c_jobs.remove(r)
        # remove this (r[0]) as a predecessor for all vertices in the rev_adj list
        for v in rev_adjacency:
            if r[0] in rev_adjacency[v]:
                rev_adjacency[v].remove(r[0])

    # now add to the pool any available vertices
    pool = [v for v in rev_adjacency if len(rev_adjacency[v]) == 0]
    pool.sort(reverse=True)
    for p in pool:
        if p in rev_adjacency and p in visited:
            del rev_adjacency[p]

print(second-1)
