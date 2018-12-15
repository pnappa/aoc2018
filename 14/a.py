

initial = [3,7]
num_recipes = 919901

elf1pos = 0
elf2pos = 1


def move():
    global initial,elf1pos, elf2pos
    #initial += str(int(initial[elf1pos]) + int(initial[elf2pos]))
    res = initial[elf1pos] + initial[elf2pos]
    if res // 10 == 0:
        initial.append(res)
    else:
        initial.append(res//10)
        initial.append(res%10)
    

    #print(initial)

    # move elf1 pos along N+1 spots
    elf1pos += (int(initial[elf1pos])+1)
    elf1pos %= len(initial)
    elf2pos += (int(initial[elf2pos])+1)
    elf2pos %= len(initial)
    
    #print(elf1pos, elf2pos)

for i in range(10000000):
    move()

num = 51589
print("".join(map(str, initial)))


print(str(num) in "".join(map(str, initial)))
