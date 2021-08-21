import numpy as np
from matplotlib import pyplot as plt
import time
import math

class Circle():
    def __init__(self, id, x, y, radius = 0.7):
        self.id = id
        self.center = [x, y]
        self.radius = radius
        self.limits = [x-radius, x+radius, y+radius, y-radius]
        self.cover = 0
        self.cover_point = []

    # 벽과 거리를 두기 위한 함수
    def in_limit(self, i, j):
        return ((i - self.center[0]) ** 2 + (j - self.center[1]) ** 2 - (self.radius / 2) ** 2) <= 0

    def can_be_generated(self, wall):
        for (i, j) in wall.uncovered+wall.covered:
            if self.in_limit(i, j):
                return False
            else:
                continue
        return True

    # 점이 원 내부에 있는지 확인하는 함수
    def in_circle(self, i, j):
        return ((i-self.center[0])**2+(j-self.center[1])**2 - self.radius**2) <= 0

    # 원을 plot하는 함수
    def print_map(self):
        circle = plt.Circle((self.center[0], self.center[1]), self.radius, fill=None, alpha=1)
        plt.gca().add_patch(circle)

    # 벽을 얼마나 커버하는지 반환하는 함수
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

# 벽 class
class Wall:
    def __init__(self, x, y):
        self.covered = []
        self.uncovered = list(zip(x, y))
        self.xpoints = x
        self.ypoints = y

    # 벽에서 커버된 점을 추가함
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
        print('length covered:', len(self.covered), '/', len(self.uncovered)+len(self.covered))

    # 모든 점이 커버되었는지 확인
    def allcovered(self):
        if len(self.uncovered) == 0:
            return True
        else:
            return False

    # plot하는 함수
    def print_map(self):
        plt.plot(self.xpoints, self.ypoints)

# 초기에 원 후보를 생성
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
            for j in np.arange(Y().f1(i) - 2, Y().f1(i)-limit, 0.1):
                # if away_form_wall(i,j, limit):
                generated_circle = Circle(id, round(i, 2), round(j, 2))
                if generated_circle.can_be_generated(wall):
                    C.append(generated_circle)
                else:
                    continue
                id += 1
        print('points generated. Time:', time.time() - start)
        return C

    def delete_c(self, c):
        self.candidate.remove(c)

# 가장 많은 점을 커버하는
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

# 실제로 다음 원을 선택하는 그리디 알고리즘
def greedy_cover(wall, C):

    steps = []
    while not wall.allcovered():
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

# 벽에 관련된 함수 (실제로는 필요없지만, 벽이 없어서 생성하기위해 필요)
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


def setting(circle):
    print('c:', circle.center)
    return circle.center[0]

if __name__=="__main__":

    # 실제로는 필요가 없지만, plot으로 보기 위해 설정하는 x의 범위
    x_up= 10
    x_down = 0

    # 실제로는 필요없는 벽 데이터값 생성 부분
    x = X(x_down, x_up)
    y = Y(x.x)
    wall = Wall(x.x, y.y)

    # 그리기 관련 부분
    fig = plt.figure(figsize=(6, 6))
    axes = plt.gca()

    # 후보 생성 및 그리디 알고리즘 적용
    C = Candidate([x_down, x_up, -10, 10], wall)
    steps = greedy_cover(wall, C)

    sorted = sorted(steps, key=setting)
    print('X:')
    for s in sorted:
        print(s.center[0], end=', ')
    print('\nY:')
    for s in sorted:
        print(s.center[1], end=', ')



    # 그리는 부분
    plt.plot(x.x, y.y ,color="grey")
    plt.show()


'''
flow: 
1. Create wall data 
2. Create Candidates
3. Use greedy algorithm to select possible positions

Problem:
- algorithm without generating candidates?
- faster method?
- Is this the best route?
- areas in circle that are unreachable

Solved:
- candidates generated too close to wall 
- uses too much memory for storing points 


'''