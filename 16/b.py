import string

goperations = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

# run the instruction, and return the resulting registers
def run(inst, registers, arga, argb, argc):
    resregister = list(registers)
    if inst == 'addr':
        resregister[argc] = resregister[arga] + resregister[argb] 
    if inst == 'addi':
        resregister[argc] = resregister[arga] + argb
    if inst == 'mulr':
        resregister[argc] = resregister[arga] * resregister[argb]
    if inst == 'muli':
        resregister[argc] = resregister[arga] * argb
    if inst == 'banr':
        resregister[argc] = resregister[arga] & resregister[argb]
    if inst == 'bani':
        resregister[argc] = resregister[arga] & argb
    if inst == 'borr':
        resregister[argc] = resregister[arga] | resregister[argb]
    if inst == 'bori':
        resregister[argc] = resregister[arga] | argb
    if inst == 'setr':
        resregister[argc] = resregister[arga]
    if inst == 'seti':
        resregister[argc] = arga
    if inst == 'gtir':
        resregister[argc] = arga > resregister[argb]
    if inst == 'gtri':
        resregister[argc] = resregister[arga] > argb
    if inst == 'gtrr':
        resregister[argc] = resregister[arga] > resregister[argb]
    if inst == 'eqir':
        resregister[argc] = arga == resregister[argb]
    if inst == 'eqri':
        resregister[argc] = resregister[arga] == argb
    if inst == 'eqrr':
        resregister[argc] = resregister[arga] == resregister[argb]
    return resregister

# fuck, this doesn't copy the list...
#successful_assignments = dict.fromkeys(range(15), goperations)
successful_assignments = {k:list(goperations) for k in range(16)}

# instrusamples is of the form:
# [REG,REG,REG,REG, ..]:num num num num:[REG, REG, ...]
with open('instrsamples', 'r') as examples:
    for row in examples.readlines():
        begreg,instructions,endreg = row.strip().split(':')
        # intify them all
        begreg = eval(begreg)
        endreg = eval(endreg)
        opnum, a,b,c = map(int, instructions.split(' '))

        # try them all, and remove the goperation str from the opcode number if it fails
        for optype in goperations:
            # this operation for this assignment is already wrong
            if optype not in successful_assignments[opnum]:
                continue
            # if using optype as opnum fails, remove it from the possibilities
            if run(optype, begreg, a, b, c) != endreg:
                del successful_assignments[opnum][successful_assignments[opnum].index(optype)]

print(successful_assignments)

# unfortunately, successful assignmments aren't one only
# from this, go through and find the ones with only one and assign them now.
correct_operators = {}

while True:
    removed = []
    for k,v in successful_assignments.items():
        if len(v) == 1:
            correct_operators[k] = v[0]
            removed.append(v[0])
    for opnum, listo in successful_assignments.items():
        for oper in removed:
            if oper in listo:
                successful_assignments[opnum].remove(oper)
    if len(removed) == 0:
        break

print(correct_operators)

creg = [0,0,0,0]
# prog is simply the program opcodes
with open('prog', 'r') as progfile:
    for row in progfile.readlines():
        opnum, a, b, c = map(int, row.strip().split(' '))
        creg = run(correct_operators[opnum], creg, a, b, c)

print(creg)

