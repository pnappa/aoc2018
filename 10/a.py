import string

grid = []
points = []
with open('input', 'r') as ifile:
    for line in ifile.readlines():
        points.append([int(x.strip()) for x in  line.strip().split(',')])

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# heurisitics told me to look here
for i in range(10104):
    # apply the velocities to each point
    for index, point in enumerate(points):
        points[index] = [point[0] + point[2], point[1] + point[3], point[2], point[3]]

#if iteration % 1 == 0:
#    point_distances = 0
#    for point in points:
#        point_distances += sum([dist(point, x) for x in points])
#    print(point_distances)
#    print(iteration, "iterations")
#input()
# apply the velocities to each point
for index, point in enumerate(points):
    points[index] = [point[0] + point[2], point[1] + point[3], point[2], point[3]]
# print the grid
min_x = min([x[0] for x in points])
min_y = min([x[1] for x in points])
max_x = max([x[0] for x in points])
max_y = max([x[1] for x in points])

print(min_x, min_y)
print(max_x, max_y)

# shift all the points -= min_x, min_y
for index, point in enumerate(points):
    points[index] = [point[0] - min_x, point[1] - min_y, 0, 0]

grid = [['.' for _ in range(max_x - min_x + 1)] for __ in range(max_y - min_y + 1)]
for p in points:
    grid[p[1]][p[0]] = "#"

print("\n".join(["".join(a) for a in grid]))

# print_grid(grid)
# let us pause per iteration
# a better heuristic will be if there's a lot of straight lines
# check if there's any long vertical lines
# sortedpoints = 
# num_contiguous = len(set([a[0] for a in points]).union(set([a[1] for a in points])))
# print(num_contiguous)
#sortedpoints = sorted([[a[0],a[1]] for a in points])
#verticals = []
#is_continuous = False
#for index, s in enumerate(sortedpoints):
#    # skip the last point
#    if index == len(sortedpoints) - 1:
#        break
#    # is this vertically contiguous with the next?
#    if abs(s[0] - sortedpoints[index+1][0]) <= 1 and abs(s[1] - sortedpoints[index+1][1]) <= 1:

#    if s[0] == sortedpoints[index+1][0] and abs(s[1] - sortedpoints[index+1][1]) == 1:
#        if is_continuous:
#            verticals[-1] += 1
#        else:
#            verticals.append(1)
#            is_continuous = True
#    else:
#        is_continuous = False
#if max(verticals) > 5:
#    print("found candidate")
#    input()


    

    
