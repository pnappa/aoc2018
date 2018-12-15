import string

grid = []
transformed = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        grid.append([a for a in line if a != '\n'])
        transformed.append([a for a in line if a != '\n'])

cart_shapes = "><^v"

# fix grid to only contain grid characters (no carts)
for index, line in enumerate(grid):
    for index2, col in enumerate(line):
        if col in cart_shapes:
            if col == '>' or col == '<':
                grid[index][index2] = '-'
            if col == 'v' or col == '^':
                grid[index][index2] = '|'
            ## oh god, let's hope this is the case
            #if index2 == 0 or index2 == len(line)-1:
            #    grid[index][index2] == '|'
            #elif index == 0 or index == len(grid)-1:
            #    grid[index][index2] == '-'
            #elif 

            

# grid = r"""/->-\        
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/   """.split('\n')
# transformed = [list(x) for x in grid]


cart_states = []
# populate the carts
for yindex, row in enumerate(transformed):
    for xindex, col in enumerate(row):
        if col in cart_shapes:
            # left means next intersection they'll turn left
            cart_states.append([xindex, yindex, col, 'LEFT'])

cart_states.sort(key=lambda x: (x[1],x[0]))

def shuffle_dir(cdir):
    if cdir == 'LEFT':
        return 'STRAIGHT'
    if cdir == 'STRAIGHT':
        return 'RIGHT'
    if cdir == 'RIGHT':
        return 'LEFT'
    # shouldn't reach here
    assert False

# get the shape this cart should take given it turns the direction given by nextdir
def get_char_type(c, nextdir):
    if c == '>':
        if nextdir == 'LEFT':
            return '^'
        if nextdir == 'STRAIGHT':
            return '>'
        if nextdir == 'RIGHT':
            return 'v'
    if c == 'v':
        if nextdir == 'LEFT':
            return '>'
        if nextdir == 'STRAIGHT':
            return 'v'
        if nextdir == 'RIGHT':
            return '<'
    if c == '<':
        if nextdir == 'LEFT':
            return 'v'
        if nextdir == 'STRAIGHT':
            return '<'
        if nextdir == 'RIGHT':
            return '^'
    if c == '^':
        if nextdir == 'LEFT':
            return '<'
        if nextdir == 'STRAIGHT':
            return '^'
        if nextdir == 'RIGHT':
            return '>'
    
# return the index of the cart at this pos
def find_cart(xpos, ypos):
    for index, el in enumerate(cart_states):
        if el is None:
            continue
        (x, y, _, _) = el
        if x == xpos and y == ypos:
            return index

def num_left(cart_states):
    count = 0
    for e in cart_states:
        if e is not None:
            count += 1

    return count

def run_iter():
    global cart_states
    for index, el in enumerate(cart_states):
        if el == None:
            continue
        xpos, ypos, cartdir, nextturn = el
        if cartdir == '>':
            nextel = transformed[ypos][xpos+1]
            nextchar = '>'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos+1, ypos)
                # remove the other cart and this one
                cart_states[index] = None
                cart_states[find_cart(xpos+1, ypos)] = None
                transformed[ypos][xpos+1] = grid[ypos][xpos+1]
                if num_left(cart_states) == 1:
                    print("last remaining cart", cart_states)
                    exit()
            if nextel == "\\":
                nextchar = 'v' 
            elif nextel == '/':
                nextchar = '^'
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn
    
            # TODO: change this cart's position
            # TODO: change the old cart's position to the old character
            if cart_states[index] is not None:
                transformed[ypos][xpos+1] = nextchar
                cart_states[index] = [xpos+1, ypos, nextchar, afterturn]
        elif cartdir == 'v':
            nextel = transformed[ypos+1][xpos]
            nextchar = 'v'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos, ypos+1)
                cart_states[index] = None
                cart_states[find_cart(xpos, ypos+1)] = None
                transformed[ypos+1][xpos] = grid[ypos+1][xpos]
                if num_left(cart_states) == 1:
                    print("last remaining cart", cart_states)
                    exit()
            if nextel == "/":
                nextchar = '<' 
            if nextel == "\\":
                nextchar = '>' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            #TODO change this cart's position
            # TODO: change the old cart's position to the old character
            if cart_states[index] is not None:
                transformed[ypos+1][xpos] = nextchar
                cart_states[index] = [xpos, ypos+1, nextchar, afterturn]
        elif cartdir == '<':
            nextel = transformed[ypos][xpos-1]
            nextchar = '<'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos-1, ypos)
                cart_states[index] = None
                cart_states[find_cart(xpos-1, ypos)] = None
                transformed[ypos][xpos-1] = grid[ypos][xpos-1]
                if num_left(cart_states) == 1:
                    print("last remaining cart", cart_states)
                    exit()
            if nextel == "\\":
                nextchar = '^' 
            if nextel == "/":
                nextchar = 'v' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            #TODO change this cart's position
            # TODO: change the old cart's position to the old character
            if cart_states[index] is not None:
                transformed[ypos][xpos-1] = nextchar
                cart_states[index] = [xpos-1, ypos, nextchar, afterturn]
        elif cartdir == '^':
            nextel = transformed[ypos-1][xpos]
            nextchar = '^'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos, ypos-1)
                cart_states[index] = None
                cart_states[find_cart(xpos, ypos-1)] = None
                transformed[ypos-1][xpos] = grid[ypos-1][xpos]
                if num_left(cart_states) == 1:
                    print("last remaining cart", cart_states)
                    exit()
            if nextel == "/":
                nextchar = '>' 
            if nextel == "\\":
                nextchar = '<' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            #TODO change this cart's position
            if cart_states[index] is not None:
                transformed[ypos-1][xpos] = nextchar
                cart_states[index] = [xpos, ypos-1, nextchar, afterturn]
    
        # change the old cart's position to the old character
        transformed[ypos][xpos] = grid[ypos][xpos]
    cart_states = [a for a in cart_states if a is not None]
    cart_states.sort(key=lambda x: (x[1],x[0]))
    print(cart_states)

while True:
    # print("\n".join(["".join(a) for a in transformed]))
    run_iter()
    # print("\n".join(["".join(a) for a in transformed]))
    #input()

#
#
#run_iter()
#print("\n".join(["".join(a) for a in grid]))
#print("\n".join(["".join(a) for a in transformed]))
#run_iter()
#print("\n".join(["".join(a) for a in grid]))
#print("\n".join(["".join(a) for a in transformed]))
#run_iter()
#print("\n".join(["".join(a) for a in grid]))
#print("\n".join(["".join(a) for a in transformed]))
