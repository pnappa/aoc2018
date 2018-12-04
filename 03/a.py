
rect = [[0]*1000 for _ in range(1000)]

with open('input', 'r') as ifile:
    for line in ifile.readlines():
        _, _, offset, size = line.strip().split(' ')
        x,y = tuple(map(lambda r: int(r), offset[:-1].split(',')))
        w,h = tuple(map(lambda r: int(r), size.split('x')))

        # colour in the rectangle
        for ih in range(h):
            for iw in range(w):
                if rect[y+ih][x+iw] == 0:
                    rect[y+ih][x+iw] = 1
                else:
                    rect[y+ih][x+iw] = -1

print(rect)

csum = 0
for row in rect:
    csum += sum(map(lambda x: 1 if x >= 2 else 0, row))

print(csum)
    
        
