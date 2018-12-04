
rect = [[0]*1000 for _ in range(1000)]

cloths = []

with open('input', 'r') as ifile:
    for line in ifile.readlines():
        idnum, _, offset, size = line.strip().split(' ')
        x,y = tuple(map(lambda r: int(r), offset[:-1].split(',')))
        w,h = tuple(map(lambda r: int(r), size.split('x')))

        cloths.append((idnum, x,y,w,h))

        # colour in the rectangle
        for ih in range(h):
            for iw in range(w):
                if rect[y+ih][x+iw] == 0:
                    rect[y+ih][x+iw] = 1
                else:
                    rect[y+ih][x+iw] = -1

print(rect)

# iterate over the cloths to see if all of their squares are 1
for idnum, x,y,w,h in cloths:
    allset = True
    for ih in range(h):
        for iw in range(w):
            if rect[y+ih][x+iw] != 1:
                allset = False
                break
        if not allset:
            break
    if not allset:
        continu:
    else:
        print("found free:", idnum)
            
