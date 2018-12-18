
grid = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        grid.append(list(line.strip()))



def clone(grid):
    new_grid = [list(row) for row in grid]
    return new_grid

lumber = '#'
ground = '.'
tree = '|'

def num_surrounding(grid, x, y, obj):
    count = 0
    # left column
    if x-1 >= 0:
        if y-1 >= 0:
            count += grid[y-1][x-1] == obj
        count += grid[y][x-1] == obj
        if y+1 < len(grid):
            count += grid[y+1][x-1] == obj
    # rught column
    if x+1 < len(grid):
        if y-1 >= 0:
            count += grid[y-1][x+1] == obj
        count += grid[y][x+1] == obj
        if y+1 < len(grid):
            count += grid[y+1][x+1] == obj
    # middle column
    if y-1 >= 0:
        count += grid[y-1][x] == obj
    if y+1 < len(grid):
        count += grid[y+1][x] == obj

    return count


# run the simulation and return the new grid
def simulate(oldgrid):
    grid = clone(oldgrid)

    for y, row in enumerate(oldgrid):
        for x, col in enumerate(row):
            if col == ground:
                if num_surrounding(oldgrid, x, y, tree) >= 3:
                    grid[y][x] = tree
            elif col == tree:
                if num_surrounding(oldgrid, x, y, lumber) >= 3:
                    grid[y][x] = lumber
            elif col == lumber:
                if num_surrounding(oldgrid, x, y, lumber) >= 1 and num_surrounding(oldgrid, x, y, tree) >= 1:
                    pass
                else:
                    grid[y][x] = ground

    return grid

print(grid)
land = "\n".join(["".join(row) for row in grid])
print(land)

print(num_surrounding(grid, 9, 9, '|'))

def freeze_grid(grid):
    return "\n".join(["".join(row) for row in grid])

grid_map = set([freeze_grid(grid)])
first_griddle = None

# running this:
for i in range(10000):
    grid = simulate(grid)
    frozen = freeze_grid(grid)
    if first_griddle == frozen:
        print("duplicated second time!", i)
    if frozen in grid_map and first_griddle is None:
        print("duplicated once!", i)
        first_griddle = frozen
    grid_map.add(frozen)

# results in
# > duplicated once! 613
# > duplicated second time! 669
# > duplicated second time! 725
# > duplicated second time! 781
# > duplicated second time! 837
# > duplicated second time! 893
# > duplicated second time! 949
# > duplicated second time! 1005
# > duplicated second time! 1061
# > duplicated second time! 1117
# > duplicated second time! 1173
# > duplicated second time! 1229
# > duplicated second time! 1285

# so! first repeat after applyin 613 times -> after 614 it starts a loop, and the period is 669-613 -> 53.
# load up the dumped graph at 613, and run it (1000000000 - 614)%53 -> 50 times.
# count it afterwards.

