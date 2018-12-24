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

# ignore the ^$
#parse_list = list(regexo[1:-1])

# return the list: will be of format ['NWES', ['S', ['SNE', None]], 'EEW']
def parse_list(paths):
    # https://stackoverflow.com/a/17141899/1129185
    def nestify(xs):
        stack = [[]]
        for x in xs:
            if x == '(':
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif x == ')':
                stack.pop()
                if not stack:
                    return 'error: opening bracket is missing'
                    #raise ValueError('error: opening bracket is missing')
            else:
                stack[-1].append(x)
        if len(stack) > 1:
            return 'error: closing bracket is missing'
            #raise ValueError('error: closing bracket is missing')
        return stack.pop()

    # go through and join strings, and replace '|'
    def join_smoosh(xs):
        res = []
        for index, x in enumerate(xs):
            if index == 0:
                res.append(x)
            else:
                if type(res[-1]) == str and type(x) == str:
                    res[-1] += x
                else:
                    pass


    # the go through that isn't joined or supporting branches
    # i.e.
    # ['E', 'N', 'W', 'W', 'W', ['N', 'E', 'E', 'E', '|', 'S', 'S', 'E', ['E', 'E', '|', 'N']]]
    pass_a =  nestify(paths)

    # then we go and join strings


# ignore the ^$
parsed_path = parse_list(list(regexo[1:-1]))
print(parsed_path)
        

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

#    def set_label(l):
#        self.label = l

    
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
                # recurse on this bracket (remember, the ) has been swallowed)
                for e in iter_path(it):
                    cnode.add_next(e)
                retlist.append(Node())
                cnode = retlist[-1]
            elif el == ')':
                return retlist
            elif el == '|':
                retlist.append(Node())
                cnode = retlist[-1]
    except StopIteration:
        return retlist

path = iter_path(iter(regexo[1:-1]))

print(regexo)
print(path)
for e in path:
    e.print()
