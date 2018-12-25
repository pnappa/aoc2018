

# i cleaned up input so that it's CSV: x,y,z,r
nanobots = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        nanobots.append(tuple(map(int, line.strip().split(","))))

biggest_bot = max(nanobots, key=lambda x: x[3])
print('largest nanobot', biggest_bot)

def dist(ax, ay, az, bx, by, bz):
    return abs(ax-bx) + abs(ay-by) + abs(az-bz)

# O(n) to find how many nanobots within range
num_within = 0
for (nx, ny, nz, _) in nanobots:
    if dist(nx,ny,nz, *biggest_bot[:3]) <= biggest_bot[3]:
        num_within += 1

print(num_within)
