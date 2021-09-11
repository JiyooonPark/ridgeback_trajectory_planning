import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class Square():
    def __init__(self, id, x, y, radius = 1):
        self.id = id
        self.center = [x, y]
        self.radius = radius
        self.points = self.generate_points()
        self.overlapped = []
        self.limits = [x-radius, x+radius, y+ radius, y-radius]
        self.cover = 0
    def generate_points(self):
        cover = []
        for i in np.arange(self.center[0]-self.radius, self.center[0]+self.radius, 0.1):
           for j in np.arange(self.center[1]-self.radius, self.center[1]+self.radius, 0.1):
               cover.append((round(i, 2), round(j,2)))
        return cover
    def update_overlap(self, steps):
        for s in steps:
            if self.check_overlap(s):
                self.overlapped.append(s)
    def check_overlap(self, circle):
        if len(set(self.points))+len(set(circle.points)) > len(set(self.points+circle.points)):
            return True
        else:
            return False
    def print_map(self):
        currentAxis = plt.gca()
        currentAxis.add_patch(Rectangle((self.limits[0], self.limits[3] ), self.radius*2, self.radius*2, fill=None, alpha=1))

    def cover_amount(self, wall):
        count = 0
        for (x, y) in wall.uncovered:
            if self.limits[0]<x<self.limits[1] and self.limits[3]<y<self.limits[2]:
                count+=1
            else:
                continue
        self.cover = count
        return self.cover
    def cover_points(self, wall):
        c = []
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.limits[0]<x<self.limits[1] and self.limits[3]<y<self.limits[2]:
                c.append((x, y))
            else:
                continue
        return c

class Wall:
    def __init__(self, x, y):
        self.covered = []
        self.uncovered = list(zip(x, y))
        self.xpoints = x
        self.ypoints = y
        self.squares = self.generate_squares()
    def add_covered(self, square):
        for (x, y) in square.calc_cover_points(self):
            if (x, y) in self.uncovered:
                print('('+str(x)+','+str(y)+')', end=' ')
                self.covered.append((x, y))
                self.uncovered.remove((x, y))
            else:
                continue
        print()
        # print('length uncovered:', len(self.uncovered), '/', len(self.uncovered)+len(self.covered))
        print('length covered:', len(self.covered), '/', len(self.uncovered)+len(self.covered))
    def allcovered(self):
        if len(self.uncovered) == 0:
            return True
        else:
            return False
    def print_map(self):
        plt.plot(self.xpoints, self.ypoints)
    def generate_squares(self):
        s = []
        id = -1
        for (x, y) in self.uncovered:
            s.append(Square(id, x, y))
            id -= 1
        return s

class Candidate:
    def __init__(self, plate):
        self.candidate = self.generate_c(plate)
    def generate_c(self, plate):
        C = []
        id = 0
        for i in np.arange(plate[0], plate[1], 0.1):
            for j in np.arange(plate[2], plate[3], 0.1):
                if j< f(i):
                    C.append(Square(id, round(i, 2), round(j, 2)))
                    id += 1
        return C
    def delete_c(self, c):
        self.candidate.remove(c)

def max_coverage(wall, C):
    selected = C[0]
    for c in C:
        m = selected.cover_amount(wall)
        if c.cover_amount(wall) > m:
            selected = c
        else:
            continue
    print("max_coverage id:", selected.id, 'covers:', m)
    if m == 0:
        return None
    return selected

def greedy_cover(wall, C):
    steps = []
    while not wall.allcovered():
        # print('len(wall.uncovered)', len(wall.uncovered))
        # print('Candidates #', len(C.candidate))
        square = max_coverage(wall, C.candidate)
        if square == None:
            break
        square.print_map()
        wall.add_covered(square)
        C.delete_c(square)
        steps.append(square)
    plt.show()
    for s in steps:
        print(s.center, end="")
    return steps
def F(x):
    list = []
    for X in x:
        list.append( 3*np.sin(X) - (X-3))
    return list
import math
def f(x):
    return 3*math.sin(x) - (x-3)
x_up= 20
x_down = 0

x = np.arange(x_down, x_up, 0.1)
X = []
for i in x:
    X.append(round(i, 2))


# y = np.sin(x * 0.5)
y = F(X)
Y = []
for i in y:
    Y.append(round(i, 2))

axes = plt.gca()
axes.set_xlim([x_down, x_up])
# axes.set_ylim([-10, 10])
plt.plot(X, Y)

wall = Wall(X, Y)
C = Candidate([x_down, x_up, -20, 5])
greedy_cover(wall, C)

plt.show()


