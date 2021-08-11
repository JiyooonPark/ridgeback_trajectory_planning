import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import time
import math

class Circle():
    def __init__(self, id, x, y, radius = 1):
        self.id = id
        self.center = [x, y]
        self.radius = radius
        self.points = self.generate_points()
        self.overlapped = []
        self.limits = [x-radius, x+radius, y+ radius, y-radius]
        self.cover = 0
    def in_circle(self, i, j):
        return ((i-self.center[0])**2+(j-self.center[1])**2 - self.radius**2) <= 1
    def generate_points(self):
        cover = []
        for i in np.arange(self.center[0]-self.radius, self.center[0]+self.radius, 0.1):
           for j in np.arange(self.center[1]-self.radius, self.center[1]+self.radius, 0.1):
               if self.in_circle(i, j):
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
        circle = plt.Circle((self.center[0], self.center[1]), self.radius, fill=None, alpha=1)
        plt.gca().add_patch(circle)
    def cover_amount(self, wall):
        count = 0
        for (x, y) in wall.uncovered:
            if self.in_circle(x, y):
                count+=1
            else:
                continue
        self.cover = count
        return self.cover
    def cover_points(self, wall):
        c = []
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.in_circle(x, y):
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
        for (x, y) in square.cover_points(self):
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
            s.append(Circle(id, x, y))
            id -= 1
        return s
class Candidate:
    def __init__(self, plate):
        self.candidate = self.generate_c(plate)
    def generate_c(self, plate):
        start = time.time()
        C = []
        id = 0
        for i in np.arange(plate[0], plate[1], 0.1):
            for j in np.arange(Y().f1(i) - 4, Y().f1(i) + 4, 0.1):
                if j< Y().f1(i):
                    C.append(Circle(id, round(i, 2), round(j, 2)))
                    id += 1
        print('points generated. Time:', time.time() - start)
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
        # square.print_map()
        circle = plt.Circle((square.center[0], square.center[1]), square.radius, fill=None, alpha=1)
        plt.gca().add_patch(circle)

        wall.add_covered(square)
        C.delete_c(square)
        steps.append(square)
    for s in steps:
        print(s.center, end="")
    return steps
class Y:
    def __init__(self, x=[]):
        self.x = x
        self.y = self.round_y()

    def f1(self, x):
        return 3 * math.sin(x) - (x - 3)

    def f1_list(self, X):
        list = []
        for x in X:
            list.append(self.f1(x))
        return list
    def round_y(self):
        y = self.f1_list(self.x)
        Y = []
        for i in y:
            Y.append(round(i, 2))
        self.y = Y
        return Y
class X:
    def __init__(self, x_down, x_up):
        self.x_down = x_down
        self.x_up = x_up
        self.x = self.round_x_()
    def generate_x(self, x_down, x_up, space = 0.1):
        return np.arange(x_down, x_up, space)
    def round_x_(self):
        x = self.generate_x(self.x_down, self.x_up)
        X = []
        for i in x:
            X.append(round(i, 2))
        return X

x_up= 10
x_down = 0

x = X(x_down, x_up)
y = Y(x.x)

axes = plt.gca()
# axes.set_xlim([x_down, x_up])
# axes.set_ylim([-10, 10])

wall = Wall(x.x, y.y)
C = Candidate([x_down, x_up, -10, 10])
greedy_cover(wall, C)

plt.plot(x.x, y.y)
plt.show()


