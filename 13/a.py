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
def find_cart(xpos, ypos, cart_states):
    for index, (x, y, _, _) in enumerate(cart_states):
        if x == xpos and y == ypos:
            return index

def run_iter():
    for index, (xpos, ypos, cartdir, nextturn) in enumerate(cart_states):
        if cartdir == '>':
            nextel = transformed[ypos][xpos+1]
            nextchar = '>'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos+1, ypos)
                #TODO: remove the other cart
                exit()
            if nextel == "\\":
                nextchar = 'v' 
            elif nextel == '/':
                nextchar = '^'
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn
    
            transformed[ypos][xpos+1] = nextchar
            # TODO: change this cart's position
            # TODO: change the old cart's position to the old character
            cart_states[index] = [xpos+1, ypos, nextchar, afterturn]
        elif cartdir == 'v':
            nextel = transformed[ypos+1][xpos]
            nextchar = 'v'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos, ypos+1)

                exit()
            if nextel == "/":
                nextchar = '<' 
            if nextel == "\\":
                nextchar = '>' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            transformed[ypos+1][xpos] = nextchar
            #TODO change this cart's position
            # TODO: change the old cart's position to the old character
            cart_states[index] = [xpos, ypos+1, nextchar, afterturn]
        elif cartdir == '<':
            nextel = transformed[ypos][xpos-1]
            nextchar = '<'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos-1, ypos)
                exit()
            if nextel == "\\":
                nextchar = '^' 
            if nextel == "/":
                nextchar = 'v' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            transformed[ypos][xpos-1] = nextchar
            #TODO change this cart's position
            # TODO: change the old cart's position to the old character
            cart_states[index] = [xpos-1, ypos, nextchar, afterturn]
        elif cartdir == '^':
            nextel = transformed[ypos-1][xpos]
            nextchar = '^'
            afterturn = nextturn
            if nextel in cart_shapes:
                print("collision!", xpos, ypos-1)
                exit()
            if nextel == "/":
                nextchar = '>' 
            if nextel == "\\":
                nextchar = '<' 
            elif nextel == '+':
                nextchar = get_char_type(cartdir, nextturn)
                afterturn = shuffle_dir(nextturn)
                # TODO: change this cart's next turn to afterturn
    
            transformed[ypos-1][xpos] = nextchar
            #TODO change this cart's position
            cart_states[index] = [xpos, ypos-1, nextchar, afterturn]
    
        # change the old cart's position to the old character
        transformed[ypos][xpos] = grid[ypos][xpos]
    cart_states.sort(key=lambda x: (x[1],x[0]))
    #print(cart_states)

while True:
    print("\n".join(["".join(a) for a in transformed]))
    run_iter()
    input()

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
