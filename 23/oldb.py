# XXX: this doesn't work! my assumption of extremums do not work under 3d manhattan space

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
cmax = list(set(cmax))

def adjacent_points(x,y,z):
    ret = []

    offsets = [(-1,-1,-1), (-1,-1,0), (-1, -1, 1), (-1, 0, -1), (1,1,1)]
    for xoff in range(-1, 2):
        for yoff in range(-1, 2):
            for zoff in range(-1, 2):
                ret.append((x+xoff, y+yoff, z+zoff))

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
min_dist = 1e9
looked_at = 0
while len(stack):
    pos = stack.pop()
    num_in = count_within(*pos, intersecting)
    # don't visit this as it's not our maxima
    if num_in < expected or pos in positions or sum(pos) > min_dist:
        continue

    min_dist = sum(pos)

    if looked_at % 1000 == 0:
        print(looked_at, pos)
    assert num_in == expected

    looked_at += 1

    positions.add(pos)
    
    # now add all the positions adjacent (manhattan)
    for ap in adjacent_points(*pos):
        stack.append(ap)

print(positions)


