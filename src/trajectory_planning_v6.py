import numpy as np
import time
from tools import *


class Iidgeback:
    def __init__(self, id, rx, ry, radius=0.622):
        self.id = id
        self.r_center = [rx, ry]
        self.i_center = [rx, ry]
        self.r_radius = radius
        self.i_radius = 0.8
        self.cover_wall_amount = 0
        self.cover_point = []

    # 벽과 거리를 두기 위한 함수
    def in_limit(self, i, j):
        return ((i - self.r_center[0]) ** 2 + (j - self.r_center[1]) ** 2 - (self.r_radius + 0.3) ** 2) <= 0

    def can_be_generated(self, wall):
        for (i, j) in wall.uncovered + wall.covered:
            if self.in_limit(i, j):
                return False
            else:
                continue
        return True

    # 점이 원 내부에 있는지 확인하는 함수
    def in_iiwa_range(self, i, j):
        return ((i - self.i_center[0]) ** 2 + (j - self.i_center[1]) ** 2 - self.i_radius ** 2) < 0 and (
                (i - self.r_center[0]) ** 2 + (j - self.r_center[1]) ** 2 - self.r_radius ** 2) > 0

    # 원을 plot하는 함수
    def print_map(self):
        i_circle = plt.Circle((self.i_center[0], self.i_center[1]), self.i_radius, fill=None, alpha=1, color='orange')
        r_circle = plt.Circle((self.r_center[0], self.r_center[1]), self.r_radius, fill=None, alpha=1)
        plt.gca().add_patch(i_circle)
        plt.gca().add_patch(r_circle)

    # 벽을 얼마나 커버하는지 반환하는 함수
    def cover_amount(self, wall):
        count = 0
        for (x, y) in wall.uncovered:
            if self.in_iiwa_range(x, y):
                count += 1
            else:
                continue
        self.cover_wall_amount = count
        return count

    def cover_amount_angle(self, wall):
        max_cover = [self.r_center[0], self.r_center[1]]
        max_count = 0
        angle_list = []
        for angle, circle in enumerate(point_in_circumference(self.r_radius - 0.2)):
            self.i_center = [circle[0] + self.r_center[0], circle[1] + self.r_center[1]]
            m = self.cover_amount(wall)
            if m > max_count:
                max_cover = [circle[0] + self.r_center[0], circle[1] + self.r_center[1]]
                max_count = m
                angle_list.append(angle)
        self.i_center = max_cover
        return self.cover_amount(wall)

    # 원이 벽의 어떤 점을 커버하는지 계산하여 원의 멤버 변수에 저장
    def calc_cover_points(self, wall):
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.in_iiwa_range(x, y):
                self.cover_point.append((x, y))
            else:
                continue
        return self.cover_point

    def plot_direction(self):
        plt.plot([self.r_center[0], self.i_center[0]], [self.r_center[1], self.i_center[1]], 'm-')


# 벽 class
class Wall:
    def __init__(self, x, y):
        self.covered = []
        self.uncovered = list(zip(x, y))
        self.xpoints = x
        self.ypoints = y

    # 벽에서 커버된 점을 추가함
    def add_covered(self, candidate):
        cx = []
        cy = []
        for (x, y) in candidate.calc_cover_points(self):
            if (x, y) in self.uncovered:
                print('(' + str(x) + ',' + str(y) + ')', end=' ')
                self.covered.append((x, y))
                self.uncovered.remove((x, y))
                cx.append(x)
                cy.append(y)
            else:
                continue
        plt.scatter(cx, cy, marker="|")
        print()
        print('length covered:', len(self.covered), '/', len(self.uncovered) + len(self.covered))

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
    def __init__(self, plate, wall, input_wall):
        self.wall = wall
        self.candidate = self.generate_c(plate)
        self.input_wall = input_wall

    def generate_c(self, plate):
        IR = []
        id = 0
        limit = 0.2
        count = 10
        x_interval = generate_interval(self.wall.xpoints, count)
        y_interval = generate_interval(self.wall.ypoints, count)
        for i in range(len(x_interval)):
            for j in np.arange(y_interval[int(i)] + limit, y_interval[int(i)] + 1, 0.05):
                generated_circle = Iidgeback(id, round(x_interval[i], 2), round(j, 2))
                if generated_circle.can_be_generated(wall):
                    IR.append(generated_circle)
                else:
                    continue
                id += 1
        return IR

    def delete_c(self, c):
        self.candidate.remove(c)


# 가장 많은 점을 커버하는
def max_coverage(wall, C):
    selected = C[0]
    for c in C:
        m = selected.cover_amount_angle(wall)
        if c.cover_amount_angle(wall) > m:
            selected = c
        else:
            continue
    selected.plot_direction()
    if m == 0:
        return None
    return selected


# 실제로 다음 원을 선택하는 그리디 알고리즘
def greedy_cover(wall, C):
    print('in greedy')
    steps = []
    while not wall.allcovered():
        max_circle = max_coverage(wall, C.candidate)
        if max_circle == None:
            break
        # plot circle
        plt.scatter(max_circle.r_center[0], max_circle.r_center[1], s=1)
        max_circle.print_map()

        wall.add_covered(max_circle)
        C.delete_c(max_circle)
        steps.append(max_circle)
    print('wall all covered')
    for s in steps:
        print(s.r_center, end="")
    print("path generated with", len(steps), "circles")

    return steps


if __name__ == "__main__":
    file_name = 'smooth_curve'
    input_wall = open_file(file_name, 'txt')
    print(f'Opened file {file_name}')
    x_wall, y_wall = plot_wall(input_wall)
    x = generate_interval(x_wall, 3)
    y = generate_interval(y_wall, 3)
    wall = Wall(x, y)

    # 그리기 관련 부분
    fig = plt.figure(figsize=(8, 3))
    axes = plt.gca()

    # 후보 생성 및 그리디 알고리즘 적용
    C = Candidate([min(x), max(x), min(y), max(y)], wall, input_wall)
    print('Candidates generated')
    steps = greedy_cover(wall, C)

    to_gazebo_cmd_format(steps)

    # 그리는 부분
    plt.plot(x, y, color="grey")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
