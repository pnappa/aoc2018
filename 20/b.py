import queue

# load the input "regex" into a list
parsed_path = []

regexo = []
with open('input', 'r') as ifile:
    regexo = ifile.readline().strip()

class Node:
    def __init__(self):
        self.next = []
        self.label = None
        pass

    def add_next(self,e):
        self.next.append(e)

    def update_label(self,letter):
        if self.label is None:
            self.label = ''
        self.label += letter

    # print ALL paths from this node onwards (yes, careful of exponentiality)
    def print(self, layer=0):
        print("-"*layer + ">", self.label)
        for e in self.next:
            e.print(layer+1)
    
# return a chain of Nodes
def iter_path(it):
    retlist = [Node()]
    try:
        cnode = retlist[0]
        while True:
            el = next(it)
            if el in "NEWS":
                cnode.update_label(el)
            elif el == '(':
                nek = Node()
                # recurse on this bracket (remember, the ) has been swallowed)
                for e in iter_path(it):
                    cnode.add_next(e)
                    e.add_next(nek)

                #retlist.append(nek)
                cnode = nek
            elif el == ')':
                return retlist
            elif el == '|':
                retlist.append(Node())
                cnode = retlist[-1]
    except StopIteration:
        return retlist

# the first node is the start of the path graph
path = iter_path(iter(regexo[1:-1]))[0]

# collapse the paths (i.e. remove all Nones)
# NE -> [None, SW] -> REST
# turns into
# NE -> [SW, REST] (with SW still pointing to REST)
def collapse_path(pa):
    has_changed = True
    to_visit = [pa]
    visited = set()
    
    # the first shouldn't be an empty boi
    assert pa.label != None

    while len(to_visit):
        cnode = to_visit.pop()
        if cnode in visited:
            continue
        visited.add(cnode)

        to_add = []
        for index, nek in enumerate(cnode.next):
            if nek.label == None:
                to_add.append(nek.next)

        cnode.next = [x for x in cnode.next if x.label is not None]

        for addy in to_add:
            cnode.next += addy
        cnode.next = list(set(cnode.next))

        to_visit += list(cnode.next)

print(regexo)
# just do it a fair few times (tbh i should have this built-in into the function, but cbf)
for i in range(1000):
    collapse_path(path)

# a graphy object that stores known positions
class Grid:
    def __init__(self, startpos):
        # adj matrix
        self.edges = {}
        # (pos, Node)
        self.visit_node_pos = set()

    # visit the positions as dictated  (returning the resultant position too)
    def travel_str(self, startpos, tstr):
        assert type(tstr) == str

        cpos = startpos
        for letter in tstr:
            oldcpos = cpos
            cpos = Grid.transmute(cpos, letter)

            if oldcpos not in self.edges:
                self.edges[oldcpos] = []
            self.edges[oldcpos].append(cpos)
            # duh, it's undirected
            if cpos not in self.edges:
                self.edges[cpos] = []
            self.edges[cpos].append(oldcpos)

        return cpos

    def print(self):
        minx = min(self.edges, key=lambda x: x[0])[0]
        miny = min(self.edges, key=lambda x: x[1])[1]
        maxx = max(self.edges, key=lambda x: x[0])[0]
        maxy = max(self.edges, key=lambda x: x[1])[1]

        def coord_to_indices(x,y):
            return 2*(x-minx)+1, 2*(y-miny)+1

        num_xcells = maxx-minx+1
        num_ycells = maxy-miny+1
        grid = [['#' for _ in range(2*num_xcells + 1)] for _ in range(num_ycells*2 + 1)]

        for fromN, toNodes in self.edges.items():
            for toX,toY in toNodes:
                fromx, fromy = fromN

                # add the dots
                ax,ay = coord_to_indices(*fromN)
                grid[ay][ax] = '.'
                bx,by = coord_to_indices(toX, toY)
                grid[by][bx] = '.'

                # add the doors in
                # verty boi
                if toX == fromx:            
                    grid[(by+ay)//2][bx] = '-'
                elif toY == fromy:
                    grid[by][(bx+ax)//2] = '|'

        # starting pos
        sx, sy = coord_to_indices(0,0)
        grid[sy][sx] = 'X'
        print("\n".join(map(''.join, grid)))

    def transmute(pos, letter):
        N = (0, -1)
        E = (1, 0)
        W = (-1, 0)
        S = (0, 1)

        if letter == 'N':
            offset = N
        elif letter == 'E':
            offset = E
        elif letter == 'W':
            offset = W
        elif letter == 'S':
            offset = S

        return (pos[0]+offset[0], pos[1]+offset[1])

    def step_through(self, c_pos, node):
        # don't need to revisit paths that we already started here from
        if (c_pos, node) in self.visit_node_pos:
            return

        self.visit_node_pos.add((c_pos, node))

        if node.label is not None:
            c_pos = self.travel_str(c_pos, node.label)

        for n in node.next:
            self.step_through(c_pos, n)

    # go through and find the shortest path to all walkable positions
    def bfs(self, startpos):
        search_visited = set()
        # node -> cumulative cost
        reached_weight = {}

        q = queue.Queue()
        q.put((0,startpos))

        while not q.empty():
            cost, el = q.get()

            if el in search_visited:
                continue
                # raise Exception('somehow revisiting a node..?')

            search_visited.add(el)
            
            for edge in self.edges[el]:
                # don't revisit already visited nodes
                if edge in search_visited or edge in reached_weight:
                    continue
                q.put((cost+1, edge))
                #assert edge not in reached_weight or reached_weight[edge] <= cost + 1
                if edge not in reached_weight:
                    reached_weight[edge] = cost+1

        return reached_weight

grid = Grid((0,0))
# path find, using djikstras (but instead we have to travel the entire path tho)
grid.step_through((0,0), path)

weighties = grid.bfs((0,0))
# part b
print("num with >= 1000", sum([1 for x in weighties.values() if x >= 1000]))
