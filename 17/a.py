
import time

visualise =  False

coordranges = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():

        parta, partb = line.strip().split(',')
        
        axesa,posa = parta.split('=')
        
        axesb,posb = partb.strip().split('=')
        
        ctup = []
        if axesa == 'x':
            ctup.append(int(posa))
            slicestart = int(posb[:posb.find('.')])
            sliceend = int(posb[posb.find('.')+2:])
            ctup.append((slicestart, sliceend))
        elif axesb == 'x':
            # append the x part
            slicestart = int(posb[:posb.find('.')])
            sliceend = int(posb[posb.find('.')+2:])
            ctup.append((slicestart, sliceend))

            # append the y part)
            ctup.append(int(posa))

        coordranges.append(tuple(ctup))

minx =  min([x[0] if type(x[0]) == int else x[0][0] for x in coordranges])
maxx =  max([x[0] if type(x[0]) == int else x[0][1]+1 for x in coordranges])
miny =  min([x[1] if type(x[1]) == int else x[1][0] for x in coordranges])
maxy =  max([x[1] if type(x[1]) == int else x[1][1]+1 for x in coordranges])

grid = [['.' for a in range(5000)] for _ in range(5000)]

# fill with clay
for coord in coordranges:
    # x-slice, woohoo
    if type(coord[0]) == int:
        for i in range(coord[1][0], coord[1][1]+1):
            grid[i][coord[0]] = '#'
    else:
        for i in range(coord[0][0], coord[0][1]+1):
            grid[coord[1]][i] = '#'

def print_around_grid(grid, cx, cy):
    linelen = 40
    cystart = cy-25 if cy > 25 else 0
    print('\n'.join(["".join(row[cx-linelen:cx+linelen]) for row in grid[cystart:cy+25]]))

water_source = (500, 0)

# get the number of water covered tiles
def num_covered(grid):
    # only count if between miny,maxy inclusive, and one of ~|
    return 0

def empty(grid, x, y):
    return grid[y][x] == '.'

def exists_trough(grid, fromx, fromy):
    rowstr = "".join(grid[fromy])

    rightledgeindex = rowstr[fromx:].find('#')
    if rightledgeindex == -1:
        return False
    leftledgeindex = rowstr[:fromx].rfind('#')
    if leftledgeindex == -1:
        return False

    nextrow = "".join(grid[fromy+1][leftledgeindex:fromx+rightledgeindex])
    return all(x in '~|#' for x in nextrow)

# assumes is a ledgey/puddling thingy!
def fill_trough(grid, fromx, fromy):
    rowstr = "".join(grid[fromy])

    rightledgeindex = rowstr[fromx:].find('#')
    leftledgeindex = rowstr[:fromx].rfind('#')
    assert rightledgeindex != -1 and leftledgeindex != -1

    grid[fromy][fromx] = '~'
    grid[fromy][leftledgeindex+1:fromx+rightledgeindex] = '~'*(fromx+rightledgeindex-(leftledgeindex+1))

# fill with | and return the positions of the left and rightmost ones if they're freestanding (only a . underneath)
def fill_void(grid, fromx, fromy):
    assert not exists_trough(grid, fromx, fromy)
    assert grid[fromy+1][fromx] != '.'

    right_spot = None 
    # fill right
    for i in range(10000):
        if grid[fromy][fromx+i] == '#':
            right_spot = None
            break

        grid[fromy][fromx+i] = '|'
        right_spot = fromx + i

        # we looney toons
        if grid[fromy+1][fromx + i] in '|.':
            break

    left_spot = None
    for i in range(10000):
        if grid[fromy][fromx-i] == '#':
            left_spot = None
            break

        grid[fromy][fromx-i] = '|'
        left_spot= fromx - i

        # we looney toons
        if grid[fromy+1][fromx - i] in '|.':
            break

    return left_spot, right_spot

# this is a recursive function that gets called on the first | off a cliff, i.e. a drop that will fall vertically
# this function forks when it bifurcates
def run(grid, startx, starty):
    if grid[starty+1][startx] == '|':
        # print('fuck')
        return
        
    cx, cy = startx, starty
    
    # ray cast down as far as we can
    while True:
        if visualise:
            time.sleep(0.03)
            print_around_grid(grid, cx, cy)
        if grid[cy+1][cx] in "#~":
            grid[cy][cx] = '|'
            # if this is a trough, fill it, and go up
            while exists_trough(grid, cx, cy):
                #print("trough")
                fill_trough(grid, cx, cy)
                cy -= 1
                if visualise:
                    time.sleep(0.03)
                    print_around_grid(grid, cx, cy)
            
            # now, we're at a non-trough - check overflow
            left_flow, right_flow = fill_void(grid, cx, cy)
            if visualise:
                time.sleep(0.03)
                print_around_grid(grid, cx, cy)
                
            # potentially bifurcate and call this fn again at new location
            if left_flow:
                run(grid, left_flow, cy)
            if right_flow:
                run(grid, right_flow, cy)

            # potentially shouldn't have this?
            return


        # add a |?
        grid[cy][cx] = '|'
        cy += 1

        # no bother continuing if water already spurted down here
        if grid[cy][cx] == '|':
            return

        # check if out of bounds, and return otherwise?
        if cy >= maxy:
            return

# start one below the water source
run(grid, water_source[0], water_source[1]+1)

print(sum([1 for x in "".join(["".join(row) for row in grid[miny:maxy]]) if x in '~|']))
