import numpy as np
from matplotlib import pyplot as plt

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
            # print(self.id, "and ", circle.id, "overlaps")
            return True
        else:
            # print(self.id, "and ", circle.id, "does not overlap")
            return False
    def print_map(self):
        for x, y in self.points:
            plt.scatter(x, y)
    def cover_amount(self, wall):
        count = 0
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.limits[0]<x<self.limits[1] and self.limits[0]<y<self.limits[1]:
                count+=1
            else:
                continue
        self.cover = count
        return self.cover
    def cover_points(self, wall):
        c = []
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.limits[0]<x<self.limits[1] and self.limits[0]<y<self.limits[1] :
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
    def add_covered(self, square):
        for (x, y) in square.cover_points(self):
            if (x, y) in self.uncovered:
                print(i, end=' ')
                self.covered.append((x, y))
                self.uncovered.remove((x, y))
        print()
        print('length uncovered:', len(self.uncovered), '/', len(self.uncovered)+len(self.covered))
        print('length covered:', len(self.covered), '/', len(self.uncovered)+len(self.covered))
    def allcovered(self):
        if len(self.uncovered) == 0:
            return True
        else:
            return False
    def print_map(self):
        plt.plot(self.xpoints, self.ypoints)



class Candidate:
    def __init__(self, plate):
        self.candidate = self.generate_c(plate)

    def generate_c(self, plate):
        S = []
        id = 0
        for i in np.arange(plate[0], plate[1], 0.1):
            for j in np.arange(plate[2], plate[3], 0.1):
                S.append(Square(id, round(i, 2), round(j, 2)))
                id += 1
        return S
    def delete_c(self, c):
        c.update_overlap(self.candidate)
        for c in c.overlapped:
            print('removing...', c.id)
            self.candidate.remove(c)
        print('after deleted C:', len(self.candidate))

def max_coverage(wall, S):
    selected = None
    m = 0
    print('len of S is : ', len(S))
    for s in S:
        if s.cover_amount(wall) > m:
            selected = s
        else:
            continue
    print("max_coverage is", selected.id)
    return selected

def greedy_cover(wall, C):
    steps = []
    while not wall.allcovered():
        print('len', len(wall.uncovered))
        square = max_coverage(wall, C.candidate)
        C.delete_c(square)
        wall.add_covered(square)
        # wall.covered.append(square)
        # wall.uncovered.remove(square)
        square.print_map()
        steps.append(square)
        plt.show()
    for s in square:
        print(s.id)
    return square



x = np.arange(1, 5, 0.1)
X = []
for i in x:
    X.append(round(i, 2))
y = np.sin(x * 0.5)
Y = []
for i in y:
    Y.append(round(i, 2))
axes = plt.gca()
axes.set_xlim([0, 6])
axes.set_ylim([-2, 2])
plt.plot(X, Y)

wall = Wall(X, Y)
C = Candidate([0, 6, -2, 2])
greedy_cover(wall, C)

# print(s.cover)



plt.show()