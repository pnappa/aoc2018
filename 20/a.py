import queue

class Graph():
    def __init__(self, istr):
        # TODO parse the istr
        visited = {(0,0): 0}

        self.queue = queue.PriorityQueue()

# load the input "regex" into a list
parsed_path = []

regexo = []
with open('input4', 'r') as ifile:
    regexo = ifile.readline().strip()

class Node():
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

    def print(self, layer=0):
        print("-"*layer + ">", self.label)
        for e in self.next:
            e.print(layer+1)
    
# return a chain of Nodes
def iter_path(it):
    retlist = [Node()]
    try:
        cstr = ""
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

                retlist.append(nek)
                cnode = retlist[-1]
            elif el == ')':
                return retlist
            elif el == '|':
                retlist.append(Node())
                cnode = retlist[-1]
    except StopIteration:
        return retlist

# the first node is the start of the path graph
path = iter_path(iter(regexo[1:-1]))[0]

print(regexo)
path.print()

# a graphy object that stores known positions
class Grid():
    def __init__(self, startpos):
        self.costs = {startpos: 0}

    def get_cost(self, x, y):
        if (x,y) in self.costs:
            return self.costs[(x,y)]
        else:
            return 9999999999999

