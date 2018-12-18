
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

for i in range(10):
    input()
    grid = simulate(grid)
    land = "\n".join(["".join(row) for row in grid])
    print(land)


land = "\n".join(["".join(row) for row in grid])
print(sum([1 for x in land if x == tree]))
print(sum([1 for x in land if x == lumber]))
