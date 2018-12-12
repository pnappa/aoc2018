
class Tape():
    def __init__(self, inputstr, startind=0):
        self.storage = {}
        for index, el in enumerate(inputstr):
            self.storage[index+startind] = el

    def __getitem__(self, index):
        if index in self.storage:
            return self.storage[index]
        return '.'
    def __setitem__(self, pos, char):
        self.storage[pos] = char

    def min_index(self):
        return min(self.storage.keys())

    def max_index(self):
        return max(self.storage.keys())

    def __str__(self):
        istr = ""
        for i in range(self.min_index(), self.max_index()+1):
            istr += self[i]
        return istr

    def dict_only_checkers(self):
        ret = []
        for k,v in self.storage.items():
            if v == '#':
                ret.append((k,v))
        ret.sort()
        return tuple(ret)

    def print_positions(self):
        pos = []
        for k,v in self.storage.items():
            if v == '#':
                pos.append(k)

        print(pos)


class Machine():
    def __init__(self, tape, transitions):
        self.tape = tape

        self.transitions = {k.split(',')[0]:k.split(',')[1] for k in transitions}

    def step(self):
        # iterate over and apply rules that match
        
        old_tape = Tape(str(self.tape), self.tape.min_index())
        for index in range(old_tape.min_index()-2, old_tape.max_index()+3):
            # get the str for surrounding this pot
            stargs = old_tape[index-2]
            stargs += old_tape[index-1]
            stargs += old_tape[index]
            stargs += old_tape[index+1]
            stargs += old_tape[index+2]

            testing = True
            if stargs in self.transitions:
                self.tape[index] = self.transitions[stargs]
                # input()
            elif testing:
                self.tape[index] = '.'

    def get_value(self):
        res = 0
        for pos,el in self.tape.storage.items():
            if el == '#':
                res += pos

        return res


rules = """..###,.
.##.#,#
#..#.,.
#.#.#,#
###..,#
.#..#,.
##..#,#
.###.,#
..#..,.
.....,.
#####,.
.#...,#
...#.,#
#...#,#
####.,.
.####,.
##.##,#
...##,.
..##.,.
#.##.,.
#....,.
.#.#.,.
..#.#,#
#.#..,#
##...,#
##.#.,.
#..##,.
.##..,.
#.###,.
....#,.
.#.##,#
###.#,#""".split('\n')

tape = Tape("..#..###...#####.#.#...####.#..####..###.##.#.#.##.#....#....#.####...#....###.###..##.#....#######")

#test input
# tape = Tape("#..#.#..##......###...###")
# rules = """...##,#
# ..#..,#
# .#...,#
# .#.#.,#
# .#.##,#
# .##..,#
# .####,#
# #.#.#,#
# #.###,#
# ##.#.,#
# ##.##,#
# ###..,#
# ###.#,#
# ####.,#""".split('\n')

mach = Machine(tape, rules)

print("initial tape:", mach.tape)

e = {}
for i in range(50000000000):
    if i % 1000 == 0:
        print("thousand its", i)
    # damn, my guess didn't pay out
    if mach.tape.dict_only_checkers() in e:
        print("found loop at iteration", i)
        exit()
    e[mach.tape.dict_only_checkers()] = i
    mach.step()

    # i noticed this pattern in the output
    if len(mach.tape.dict_only_checkers()) == 53:
        print(i)
        mach.tape.print_positions()
        # ctrl-c after a while
        # then in counter.py i did some maths on it
