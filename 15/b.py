import string

import sys
grid = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        grid.append(list(line.strip()))

goblin_attack_power = 3
elf_attack_power = 3


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
    for ind, e in enumerate(units):
        if e is None:
            continue
        xprime, yprime, _, _ = e
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
    telescoping_distances = dict.fromkeys(range(32*32), [])
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

def is_num(i):
    try:
        int(i)
        return True
    except:
        return False

def del_none(units):
    cdeleted = 0
    for i in range(len(units)):
        if units[i-cdeleted] == None:
            del units[i-cdeleted]
            cdeleted += 1

def attack_if_possible(grid, units, cx, cy, col):
    enemy = enemy_adjacent(units, cx, cy, col)
    if enemy is None:
        return False
    
    ind = find_agent_index(*enemy, units)

    xindexprime, yindexprime, oppotype, new_hp = units[ind]
    if col == 'E':
        new_hp -= elf_attack_power
    elif col == 'G':
        new_hp -= goblin_attack_power
    # print("attack occuring by", col, "to", xindexprime, yindexprime, "hp is now", new_hp)
    # killed
    if new_hp < 0:
        units[ind] = None
        grid[enemy[0]][enemy[1]] = '.'

        # fuck, an elf died
        if oppotype == 'E':
            print("elf died", elf_attack_power)
            exit(-1)
    else:
        units[ind] = [xindexprime, yindexprime, oppotype, new_hp]

    return True

haswon = False
wasfullround = False
def iteration(grid, units):
    global haswon, wasfullround
    last_attacking_index = None
    for index, unit in enumerate(units):
        # print(unit)
        if unit is None:
            continue
        xindex, yindex, col, hp = unit

        # if we can't attack now, we move
        if not attack_if_possible(grid, units, xindex, yindex, col):
            # move

            # get a floodfill
            flood_grid, tdists = flood_fill(grid, xindex, yindex)

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

            # sort by y,x
            potential_locations.sort(key=lambda x: (x[1], x[0]))
            # this can't even move, what a fuckin loser lol
            if len(potential_locations) == 0:
                continue

            # otherwise it can, so let's find what the pos should move
            tofindx, tofindy = potential_locations[0]
            #print(tofindx, tofindy)
            founddir = None
            for (fucky, fuckx, directo) in tdists[cmin]:
                if fuckx == tofindx and tofindy == fucky:
                    founddir = directo
                    break

            chosen_step = get_offset(xindex, yindex, founddir)

            assert chosen_step != None
            # and move it that dir
            units[index] = [chosen_step[0], chosen_step[1], col, hp]
            grid[yindex][xindex] = '.'
            grid[chosen_step[1]][chosen_step[0]] = col

            if attack_if_possible(grid, units, chosen_step[0], chosen_step[1], col):
                last_attacking_index = index
                # print("moved and attacked!")
        else:
            last_attacking_index = index
            
    # print("was full round?", last_attacking_index == len(units)-1)
    wasfullround = (last_attacking_index == len(units)-1)
    # XXX: this wont work
    # units = [a for a in units if a is not None]
    del_none(units)

    # sort by y, then x
    units.sort(key=lambda x: (x[1], x[0]))
    if all([True if x[2] == 'E' else False for x in units]):
        haswon = True
        print("elf side wins!!")

    if all([True if x[2] == 'G' else False for x in units]):
        haswon = True
        print("goblin side wins!!")

while True:
    elf_attack_power = int(sys.argv[1])

    for i in range(1000):
        #print("\n".join(["".join(row) for row in grid]))
        # print(units)
        iteration(grid, units)
        if haswon:
            sumhp = 0
            for x,y, col, hp in units:
                sumhp += hp
            if wasfullround:
                i+=1
            print(i, sumhp, elf_attack_power)
            exit()
