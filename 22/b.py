import queue

depth = 10914
target = (9,739)

#depth = 510
#target = (10,10)

grid = [[None for  _ in range(target[0]+1)] for _ in range(target[1]+1)]

ROCKY = 0
WET = 1
NARROW = 2

erosion_cache = {}

# return 
def get_erosion(grid, posx, posy, depth):
    global erosion_cache

    if (posx, posy) in erosion_cache:
        return erosion_cache[(posx, posy)]

    if posx == 0 and posy == 0:
        gi = 0
    elif posx == target[0] and posy == target[1]:
        gi = 0
    elif posy == 0:
        gi = posx * 16807
    elif posx == 0:
        gi = posy * 48271
    else:
        gi = get_erosion(grid, posx-1, posy, depth) * get_erosion(grid, posx, posy-1, depth)

    erosion_cache[(posx, posy)] = ((gi + depth) % 20183)

    return erosion_cache[(posx, posy)]

def print_cache():
    def get_char(num):
        num = num % 3
        if num == ROCKY:
            return '.'
        if num == WET:
            return '='
        if num == NARROW:
            return '|'
        print(num)
        raise Exception('fuck')

    global erosion_cache
    
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            print(get_char(erosion_cache[(x,y)]), end='')

        print()

TORCH = 0
CLIMBGEAR = 1
NEITHER = 2

def is_valid_tool(terrain, tool):
    if terrain == ROCKY:
        return tool == CLIMBGEAR or tool == TORCH
    if terrain == WET:
        return tool == CLIMBGEAR or tool == NEITHER
    if terrain == NARROW:
        return tool == TORCH or tool == NEITHER

def get_avail_tools(terrain):
    if terrain == ROCKY:
        return CLIMBGEAR, TORCH
    if terrain == WET:
        return CLIMBGEAR, NEITHER
    if terrain == NARROW:
        return TORCH, NEITHER
    print("error terrain:", terrain)

def get_pos_choices(x, y):
    ret = []

    if x != 0:
        ret.append((x-1, y))
    if y != 0:
        ret.append((x, y-1))
    ret.append((x+1, y))
    ret.append((x, y+1))

    return ret

def get_terrain(x, y):
    #return erosion_cache[(x,y)] % 3
    return get_erosion(grid, x, y, depth) % 3

# get the edges from this node
def get_edges(grid, x, y, ctool):
    pos_tools = get_avail_tools(get_terrain(x,y))
    assert ctool in pos_tools

    edges = {}
    # if we move, this is where we can move
    positions = get_pos_choices(x, y)
    for pos in positions:
        pos_t = get_terrain(*pos)
        if is_valid_tool(pos_t, ctool):
            edges[(pos, ctool)] = 1

    # we can also move to ourself, and change tool
    other_tool = pos_tools[(pos_tools.index(ctool)+1)%len(pos_tools)]
    edges[((x,y), other_tool)] = 7

    return edges

# path find until we reach the goal
def solve(grid, goalx, goaly):
    # start at 0,0 with a torch (and 0 cumcost)
    start_pos = (0, (0,0), TORCH)

    # ((posx, posy), tool) -> cum cost
    costs = {}
    q = queue.PriorityQueue()
    q.put(start_pos)

    # djikstra over the lazy-graph
    while not q.empty():
        cost, c_pos, tool = q.get()

        print("position:", c_pos, "cost:", cost)

        x,y = c_pos
        # too wide! very unlikely to go any wider (remember, goal is like x=9)
        if x > 50:
            continue

        # hmm.. this shouldn't be possible, right?
        # wait, no, it's possible.
        if (c_pos, tool) in costs:
            continue
        costs[(c_pos, tool)] = cost

        if c_pos == (goalx, goaly) and tool == TORCH:
            print('goal reached!')
            break


        for identifier, edge_cost in get_edges(grid, *c_pos, tool).items():
            if identifier in costs:
                # should this be possible too..? we don't have neg edges
                if edge_cost+cost < costs[identifier]:
                    print("WARNING: revisited node with lower cost")
                continue

            other_pos, other_tool = identifier
            # let em queue
            q.put((edge_cost+cost, other_pos, other_tool))
    return costs
            

g = solve(grid, *target)
print("cost to reach", g[(target, TORCH)])
