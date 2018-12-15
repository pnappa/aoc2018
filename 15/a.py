import string

grid = []
with open('input3', 'r') as ifile:
    for line in ifile.readlines():
        grid.append(list(line.strip()))

attack_power = 3

units = []

# scan through and find and assign each hp
for yindex, row in enumerate(grid):
    for xindex, col in enumerate(row):
        if col == 'E' or col == 'G':
            units.append([xindex, yindex, col, 200])

def opposite_type(el):
    return 'E' if el == 'G' else 'G'

#return true if cardinally adjacent
def posadj(posax, posay, posbx, posby):
    if posax == posbx:
        if posay == posby + 1 or posay + 1 == posby:
            return True
    elif posay == posby:
        if posax == posbx + 1 or posax + 1 == posbx:
            return True
    return False

# returns the enemy that's adjacent that has the lowest hp, ties are resolved with coords
def enemy_adjacent(units, xindex, yindex, col):
    oppo = opposite_type(col)
    options = []
    for unit in units:
        if unit is None:
            continue
        otherx, othery, othertype, hp = unit
        # ignore same species
        if othertype != oppo:
            continue

        if posadj(xindex, yindex, otherx, othery):
            options.append((hp, othery, otherx))

    assert len(options) <= 4

    if len(options) == 0:
        return None

    # sort by hp, y, then x
    options.sort(key=lambda x: (x[0], x[1], x[2]))
    # return xy
    return (options[0][1],options[0][2])

def find_agent_index(yindex, xindex, units):
    for ind, (xprime, yprime, _, _) in enumerate(units):
        if xprime == xindex and yindex == yprime:
            return ind

# manhattan dist
def dist(ax, ay, bx, by):
    return abs(ax-bx) + abs(ay-by)

def occupied(grid, x, y):
    el = grid[y][x]
    return el == 'G' or el == 'E' or el == '#' or type(el) == int

def get_offset(x, y, direction):
    if direction == '1up':
        return (x, y-1)
    if direction == '2left':
        return (x-1, y)
    if direction == '3right':
        return (x+1, y)
    if direction == '4down':
        return (x, y+1)
    raise Exception('fuck fuck')

def flood_fill(grid, startx, starty):
    # XXX: WIP
    # simulate a flood fill and fill all non-occupied posotions with step counts
    # duplicate the grid and start floodfilling
    dupgrid = [list(row) for row in grid]
    dupgrid[starty][startx] = 0

    # telescoping_distances[0].append((startx, starty, None))

    cdist = 1
    telescoping_distances = dict.fromkeys(range(1000), [])
    # add the initial cardinal directions
    if not occupied(dupgrid, startx, starty-1):
        #print("up not occued")
        telescoping_distances[cdist].append((starty-1, startx, '1up'))
    if not occupied(dupgrid, startx-1, starty):
        #print("left not occued")
        telescoping_distances[cdist].append((starty, startx-1, '2left'))
    if not occupied(dupgrid, startx+1, starty):
        # print("right not occued")
        telescoping_distances[cdist].append((starty, startx+1, '3right'))
    if not occupied(dupgrid, startx, starty+1):
        # print("down not occued")
        telescoping_distances[cdist].append((starty+1, startx, '4down'))

    # continue floodfilling until we have no more left
    while len(telescoping_distances[cdist]) != 0:
        # next iterations queued elements
        next_queued = []
        for (qposy, qposx, fromdir) in telescoping_distances[cdist]:
            if occupied(dupgrid, qposx, qposy):
                continue
            dupgrid[qposy][qposx] = cdist
            for xoff, yoff in zip( [0, -1, 1, 0], [-1, 0, 0, 1]):
                next_queued.append((qposy+yoff, qposx+xoff, fromdir))
        next_queued.sort()

        cdist += 1
        telescoping_distances[cdist] = next_queued

    # input()
    return dupgrid, telescoping_distances

def path_dist(startx, starty, endx, endy, grid):
    if starty == endy and startx == endx:
        return 0, (startx, starty)
    # print("path finding to", endx, endy, "from", startx, starty)
    # TODO: path finding..?
    # duplicate the grid and start floodfilling
    dupgrid = [list(row) for row in grid]
    dupgrid[starty][startx] = 0
    
    # positions next to floodfill adjacents
    queued_positions = [(1, startx-1,starty, 'left'), (1, startx+1, starty, 'right'), (1, startx, starty-1, 'up'), (1, startx, starty+1, 'down')]
    queued_positions.sort()

    # check the queued positions first
    for (dis, initposx, initposy, _) in queued_positions:
        if initposx == endx and initposy == endy:
            return dis, (initposx, initposy)

    while True:
        # sort by y,x
        queued_positions.sort()
        if len(queued_positions) == 0:
            return None, None
        next_queued = []
        for queued_pos in queued_positions:
            # don't bother looking at unreachable positions anyway
            if occupied(dupgrid, queued_pos[1], queued_pos[2]):
                continue
            # fill this element
            dupgrid[queued_pos[2]][queued_pos[1]] = queued_pos[0]
            # print(queued_pos)
            # for each of the cardinal directions if it isn't a number or occupied, give it a number
            xoffsets, yoffsets = [0, 0, 1, -1], [1, -1, 0, 0]
            for xoff,yoff in zip(xoffsets, yoffsets):
                newx, newy = queued_pos[1]+xoff, queued_pos[2]+yoff
                #print("lookin at", newx, newy)
                #print('element at pos', dupgrid[newy][newx])
                calcdist = queued_pos[0] + 1
                if newx == endx and newy == endy:
                    # DONE!
                    firststepdir = queued_pos[-1] 
                    nextstep = None
                    if firststepdir == 'left':
                        nextstep = startx -1, starty
                    elif firststepdir == 'right':
                        nextstep = startx+1, starty
                    elif firststepdir == 'up':
                        nextstep = startx, starty-1
                    elif firststepdir == 'down':
                        nextstep = startx, starty + 1
                    # print("result", calcdist, nextstep)
                    return calcdist, nextstep

                if not occupied(dupgrid, newx, newy):
                    #print('added')
                    # dupgrid[newy][newx] = calcdist
                    # append which step we took to find this one too
                    next_queued.append((calcdist, newx, newy, queued_pos[-1]))

        queued_positions = next_queued

def is_num(i):
    try:
        int(i)
        return True
    except:
        return False

haswon = False
def iteration(grid, units):
    global haswon
    for index, unit in enumerate(units):
        # print(unit)
        if unit is None:
            continue
        xindex, yindex, col, hp = unit
        enemy =  enemy_adjacent(units, xindex, yindex, col)
        if enemy is not None:
            # attack
            ind = find_agent_index(*enemy, units)
            xindexprime, yindexprime, oppotype, new_hp = units[ind]
            new_hp -= attack_power
            print("attack occuring by", col, "to", xindexprime, yindexprime, "hp is now", new_hp)
            # killed
            if new_hp < 0:
                print("enemy of", col, "KIA")
                # del units[ind]
                units[ind] = None
                grid[enemy[0]][enemy[1]] = '.'
            else:
                units[ind] = [xindexprime, yindexprime, oppotype, new_hp]
        else:
            # move

            # get a floodfill
            flood_grid, tdists = flood_fill(grid, xindex, yindex)

            # print("\n".join(["".join(map(str, row)) for row in flood_grid]))

            potential_locations = []
            cmin = 99999999
            for unit2 in units:
                if unit2 is None:
                    continue
                otherx, othery, othercol, _ = unit2
                # ignore same-units
                if othercol == col:
                    continue
                for (offx, offy) in zip([0, -1, 1, 0], [-1, 0, 0, 1]):
                    primex, primey = otherx + offx, othery + offy
                    dist_to_point = flood_grid[primey][primex]
                    if not is_num(dist_to_point):
                        continue
                    if dist_to_point == cmin:
                        potential_locations.append((primex, primey))
                    elif dist_to_point < cmin:
                        cmin = dist_to_point
                        potential_locations = [(primex, primey)]
            #print(potential_locations)
            # sort by y,x
            potential_locations.sort(key=lambda x: (x[1], x[0]))
            # this can't even move, what a fuckin loser lol
            if len(potential_locations) == 0:
                continue

            #print(tdists[cmin])

            # otherwise it can, so let's find what the pos should move
            tofindx, tofindy = potential_locations[0]
            #print(tofindx, tofindy)
            founddir = None
            for (fucky, fuckx, directo) in tdists[cmin]:
                if fuckx == tofindx and tofindy == fucky:
                    founddir = directo
                    break

            chosen_step = get_offset(xindex, yindex, founddir)

            # debugging this fucking elf
            # if col == 'E':
            #     print('grid pre-elf')
            #     print(units)
            #     print("\n".join(["".join(row) for row in grid]))
            #     input()

            # for otherunit in units:
            #     otherx, othery, othercol, _ = otherunit
            #     # no need to path find to a friendly
            #     if othercol == col:
            #         continue

            #     xoffsets, yoffsets = [0, 0, 1, -1], [1, -1, 0, 0]
            #     for opos in zip(xoffsets, yoffsets):
            #         primex = otherx + opos[0]
            #         primey = othery + opos[1]
            #         cdist, nextstep = path_dist(xindex, yindex, primex, primey, grid)
            #         if cdist is not None and othercol != col and cdist < min_dist:
            #             min_dist = cdist
            #             closest_chosen = (primex, primey)
            #             chosen_step = nextstep

            # print("chosen step", chosen_step)
                        
            assert chosen_step != None
            # and move it that dir
            units[index] = [chosen_step[0], chosen_step[1], col, hp]
            grid[yindex][xindex] = '.'
            grid[chosen_step[1]][chosen_step[0]] = col
            #print("\n".join(["".join(row) for row in grid]))

            # if col == 'E':
            #     print('grid post-elf')
            #     print("\n".join(["".join(row) for row in grid]))
            #     input()
            
    # XXX: this wont work
    units = [a for a in units if a is not None]

    # sort by y, then x
    units.sort(key=lambda x: (x[1], x[0]))
    if all([True if x[2] == 'E' else False for x in units]) or all([True if x[2] == 'G' else False for x in units]):
        haswon = True
        print("one side wins!!")
        return

for i in range(1000):
    print("\n".join(["".join(row) for row in grid]))
    if haswon:
        print(i-1)
        exit()
    iteration(grid, units)
