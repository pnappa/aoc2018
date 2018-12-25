

# i cleaned up input so that it's CSV: x,y,z,r
nanobots = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        nanobots.append(tuple(map(int, line.strip().split(","))))

biggest_bot = max(nanobots, key=lambda x: x[3])
print('largest nanobot', biggest_bot)

def dist(ax, ay, az, bx, by, bz):
    return abs(ax-bx) + abs(ay-by) + abs(az-bz)

def count_within(x,y,z, nanobots):
    count = 0
    for (nx, ny, nz, r) in nanobots:
        count += int(dist(nx, ny, nz, x,y,z) <= r)
    return count

def get_within(x,y,z, nanobots):
    ret = []
    for (nx, ny, nz, r) in nanobots:
        if dist(nx,ny,nz, x,y,z) <= r:
            ret.append((nx, ny, nz, r))
    return ret

# get a list of all extreme points (minx, and miny, minz) for each nanobot
def get_extremums(nanobots):
    retlist = []
    for (nx, ny, nz, r) in nanobots:
        # ..what if the radii go beyond 0,0,0?
        xclamp = max([nx-r, 0])
        yclamp = max([ny-r, 0])
        zclamp = max([nz-r, 0])

        retlist.append((xclamp, ny, nz))
        retlist.append((nx, yclamp, nz))
        retlist.append((nx, ny, zclamp))

        # shouldn't be required...
        retlist.append((nx+r, ny, nz))
        retlist.append((nx, ny+r, nz))
        retlist.append((nx, ny, nz+r))

    return retlist

extremums = get_extremums(nanobots)

cmax = []
cmax_in = 0
for extremum in extremums:
    within = count_within(*extremum, nanobots)
    if within > cmax_in:
        cmax = [extremum]
        cmax_in = within
    elif within == cmax_in:
        cmax.append(extremum)
    else:
        continue

print(cmax, cmax_in)

def adjacent_points(x,y,z):
    ret = []

    ret.append((x-1, y, z))
    ret.append((x+1, y, z))
    ret.append((x, y-1, z))
    ret.append((x, y+1, z))
    ret.append((x, y, z-1))
    ret.append((x, y, z+1))

    return ret


# just an assumption for later code, this may not actually be the case
assert len(cmax) == 1
cmax = cmax[0]
intersecting = get_within(*cmax, nanobots)

# now, "flood-fill" to find all coordinates that are in the 3d secant
stack = []
expected = cmax_in
stack.append(cmax)
positions = set()
while len(stack):
    pos = stack.pop()
    print(pos)

    # don't visit this as it's not our maxima
    if count_within(*pos, intersecting) < expected or pos in positions:
        continue

    positions.add(pos)
    
    # now add all the positions adjacent (manhattan)
    for ap in adjacent_points(*pos):
        stack.append(ap)

print(positions)














