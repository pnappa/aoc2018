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

num_threeplus = 0
# instrusamples is of the form:
# [REG,REG,REG,REG, ..]:num num num num:[REG, REG, ...]
# create the file by running the following bash commands (after getting rid of the program at the end of file)
# $ grep "Before" input | grep -o "\[.*\]" > befores
# $ grep "After" input | grep -o "\[.*\]" > afters
# $ grep -E "^[0-9]+ [0-9]+ [0-9]+ [0-9]+$" input > ops
# $ paste -d":" befores ops afters > instrsamples
with open('instrsamples', 'r') as examples:
    for row in examples.readlines():
        begreg,instructions,endreg = row.strip().split(':')
        # intify them all
        begreg = eval(begreg)
        endreg = eval(endreg)
        #ignore opnum, we try them all anyway
        _, a,b,c = map(int, instructions.split(' '))

        num_equiv = 0
        for optype in goperations:
            num_equiv += run(optype, begreg, a, b, c) == endreg

        if num_equiv >= 3:
            num_threeplus += 1

print(num_threeplus)
