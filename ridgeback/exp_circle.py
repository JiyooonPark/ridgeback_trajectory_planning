import numpy as np
from matplotlib import pyplot as plt
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
        self.cover_point = []
    def in_circle(self, i, j):
        return ((i-self.center[0])**2+(j-self.center[1])**2 - self.radius**2) <= 0
    def generate_points(self):
        cover = []
        for i in np.arange(self.center[0]-self.radius, self.center[0]+self.radius, 0.05):
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

    # 원을 plot하는 함수
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
    # 원이 벽의 어떤 점을 커버하는지 계산하여 원의 멤버 변수에 저장
    def calc_cover_points(self, wall):
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.in_circle(x, y):
                self.cover_point.append((x, y))
            else:
                continue
        return self.cover_point

class Wall:
    def __init__(self, x, y):
        self.covered = []
        self.uncovered = list(zip(x, y))
        self.xpoints = x
        self.ypoints = y
        self.squares = self.generate_squares()

    def add_covered(self, square):
        cx = []
        cy = []
        for (x, y) in square.calc_cover_points(self):
            if (x, y) in self.uncovered:
                print('('+str(x)+','+str(y)+')', end=' ')
                self.covered.append((x, y))
                self.uncovered.remove((x, y))
                cx.append(x)
                cy.append(y)
            else:
                continue
        plt.scatter(cx,cy, marker="|")
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
    def __init__(self, plate, wall):
        self.candidate = self.generate_c(plate)
        self.wall = wall

    def generate_c(self, plate):
        start = time.time()
        C = []
        id = 0
        limit = 0.5

        for i in np.arange(plate[0], plate[1], 0.05):
            for j in np.arange(Y().f1(i) - 2, Y().f1(i) -limit, 0.1):
                # if away_form_wall(i,j, limit):
                C.append(Circle(id, round(i, 2), round(j, 2)))
                id += 1
        print('points generated. Time:', time.time() - start)
        return C

    def away_from_limit(self, x, y, limit):
        pass
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
        max_circle = max_coverage(wall, C.candidate)
        if max_circle == None:
            break

        # plot circle
        plt.scatter(max_circle.center[0], max_circle.center[1])
        circle = plt.Circle((max_circle.center[0], max_circle.center[1]), max_circle.radius, fill=None, alpha=1)
        plt.gca().add_patch(circle)


        wall.add_covered(max_circle)
        C.delete_c(max_circle)
        steps.append(max_circle)

    for s in steps:
        print(s.center, end="")
    print("path generated with", len(steps), "circles")

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
    def generate_x(self, x_down, x_up, space = 0.05):
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
C = Candidate([x_down, x_up, -10, 10], wall)
greedy_cover(wall, C)

plt.plot(x.x, y.y ,color="grey")
plt.show()


