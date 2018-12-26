

# crack out the ILP solvers for this one
# basing myself off this one http://benalexkeen.com/linear-programming-with-python-and-pulp-part-2/

import pulp

nanobots = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        nanobots.append(tuple(map(int, line.strip().split(","))))

# minx
minx = min(nanobots, key=lambda x: x[0]-x[3])
maxx = max(nanobots, key=lambda x: x[0]+x[3])

miny = min(nanobots, key=lambda x: x[1]-x[3])
maxy = max(nanobots, key=lambda x: x[1]+x[3])

minz = min(nanobots, key=lambda x: x[2]-x[3])
maxz = max(nanobots, key=lambda x: x[2]+x[3])

def in_range(x,y,z, nanobot):
    absx = x.value() - nanobot[0] if x.value() > nanobot[0] else nanobot[0] - x.value()
    absy = y.value() - nanobot[1] if y.value() > nanobot[1] else nanobot[1] - y.value()
    absz = z.value() - nanobot[2] if z.value() > nanobot[2] else nanobot[2] - z.value()

    return ( absx + absy + absz ) < nanobot[3]

my_lp_problem = pulp.LpProblem("minimum distance for maximally intersecting area", pulp.LpMaximize)

# maximise f(x,y,z) : sum for n in nanobots: x in n's range && y in n's range && z in n's range
x = pulp.LpVariable('x', lowBound = minx, upBound = maxx, cat = 'Integer')
y = pulp.LpVariable('y', lowBound = miny, upBound = maxy, cat = 'Integer')
z = pulp.LpVariable('z', lowBound = minz, upBound = maxz, cat = 'Integer')

# objective function
my_lp_problem += pulp.lpSum([in_range(x,y,z,n) for n in nanobots]), 'f(x,y,z)'

print(my_lp_problem)
