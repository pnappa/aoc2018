import string
import functools

xsize = 300
ysize = 300

def power_lev(xcoord, ycoord):
    rackID = xcoord + 10
    plev = rackID * ycoord
    # actually fuck this line, i didn't solve it for an hour because i had a typo in this line
    plev += 6303
    plev *= rackID 
    radix = ("000" + str(plev))[-3]
    return int(radix) - 5

grid = [[power_lev(x, y) for x in range(1, xsize+1)] for y in range(1, ysize+1)]

# pos & width -> sum
# (x,y,w) -> 999
cache = {}
def sum_grid(startx, starty, size):
    if (startx, starty, size) in cache:
        pass
    elif size == 1:
        cache[(startx,starty,size)] = grid[starty][startx]
    elif size == 2:
        a = cache[(startx, starty, 1)] 
        b= cache[(startx+1, starty, 1)]
        c= cache[(startx, starty+1, 1)] 
        d= cache[(startx+1, starty+1, 1)]
        cache[(startx, starty, size)] = a+b+c+d
    elif size % 2 == 0:
        subsquare = size//2
        a =  cache[(startx, starty, subsquare)]
        b =  cache[(startx+subsquare, starty, subsquare)]
        c =  cache[(startx, starty+subsquare, subsquare)]
        d =  cache[(startx+subsquare, starty+subsquare, subsquare)]
        cache[(startx, starty, size)] = a+b+c+d
    else:
        subsquare = size-1
        bigblock = cache[(startx+1, starty+1, subsquare)]
        remainder = 0
        for i in range(size):
            remainder += grid[starty][startx+i]
            remainder += grid[starty+i][startx]
        cache[(startx,starty,size)] = bigblock + remainder
    return cache[(startx, starty, size)]


max_sum = 0
square_size = 0
lxy_coord = (0,0)
# iterate over and find max 3x3 (ignore first and last rows)
for i in range(1, 50):
    print(i)
    for y in range(0, ysize-i):
        for x in range(0, xsize-i):
            c_sum = sum_grid(x,y,i)
            #for ypos in range(0, i):
            #    for xpos in range(0, i):
            #        c_sum += grid[y+ypos][x+xpos]
            #        #c_sum += sum_grid(y+ypos,x+xpos, i)
            if c_sum > max_sum:
                max_sum = c_sum
                lxy_coord = (x+1,y+1)
                square_size = i
                
print(max_sum, lxy_coord, square_size)
