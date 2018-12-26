import string
import sys

goperations = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

# run the instruction, and return the resulting registers
def run(registers, inst, arga, argb, argc):
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
        resregister[argc] = int(arga > resregister[argb])
    if inst == 'gtri':
        resregister[argc] = int(resregister[arga] > argb)
    if inst == 'gtrr':
        resregister[argc] = int(resregister[arga] > resregister[argb])
    if inst == 'eqir':
        resregister[argc] = int(arga == resregister[argb])
    if inst == 'eqri':
        resregister[argc] = int(resregister[arga] == argb)
    if inst == 'eqrr':
        resregister[argc] = int(resregister[arga] == resregister[argb])
    return resregister


program = []

registers = [0,0,0,0,0,0]
rip = 4

with open('input', 'r') as ifile:
    for line in ifile:
        instr, a, b, c = line.strip().split(' ')
        program.append((instr, int(a), int(b), int(c)))

ctr = 0
hasclicked = False
# now evaluate it
while registers[rip] < len(program) and ctr < 1e5:
    ctr += 1
    print("executing", program[registers[rip]], "NUM", ctr)
    if program[registers[rip]] == ('eqrr', 3, 0, 5):
        print('yippee, last instr', registers)
        print('set r0 to', registers[3])
        sys.exit()
    registers = run(registers, *program[registers[rip]])
    registers[rip] += 1
    print(registers)

print(registers)
print(ctr)
