import string

points = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        points.append([int(x.strip()) for x in  line.strip().split(',')])

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


xsize = 300
ysize = 300

def power_lev(xcoord, ycoord):
    rackID = xcoord + 10
    plev = rackID * ycoord
    plev += 6303
    plev *= rackID 
    radix = ("000" + str(plev))[-3]
    return int(radix) - 5

grid = [[power_lev(x, y) for x in range(1, xsize+1)] for y in range(1, ysize+1)]

print(grid)
print(len(grid))

max_sum = 0
lxy_coord = (0,0)
# iterate over and find max 3x3 (ignore first and last rows)
for i in range(1, 3):
    offset = i//2 if i % 2 == 0 else (i-1)//2
    print("square size:", i, "offset:", offset)
    for y in range(offset, ysize-offset):
        for x in range(offset, xsize-offset):
            c_sum = 0
            for ypos in range(-offset, offset+1):
                for xpos in range(-offset, offset+1):
                    c_sum += grid[y-ypos][x-xpos]
                # c_sum += grid[y-1][x-1] + grid[y-1][x] + grid[y-1][x+1]
                # c_sum += grid[y][x-1] + grid[y][x] + grid[y][x+1]
                # c_sum += grid[y+1][x-1] + grid[y+1][x] + grid[y+1][x+1]
    
            if c_sum > max_sum:
                max_sum = c_sum
                lxy_coord = (x, y)
            

print(max_sum, lxy_coord)
        

