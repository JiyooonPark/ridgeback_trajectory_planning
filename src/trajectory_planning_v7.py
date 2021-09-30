import numpy as np
import time
from tools import *

class Iidgeback:
    def __init__(self, id, rx, ry, wall, radius=0.622):
        self.id = id
        self.i_center = [rx, ry]
        self.i_radius = 0.8
        self.cover_wall_amount = 0
        self.cover_point = []
        self.calc_cover_points(wall)

    # 벽과 거리를 두기 위한 함수
    def in_limit(self, i, j):
        return ((i - self.i_center[0]) ** 2 + (j - self.i_center[1]) ** 2 - (self.i_radius + 0.3) ** 2) <= 0

    def can_be_generated(self, wall):
        for (i, j) in wall.uncovered + wall.covered:
            if self.in_limit(i, j):
                return False
            else:
                continue
        return True

    # 점이 원 내부에 있는지 확인하는 함수
    def in_iiwa_range(self, i, j):
        return ((i - self.i_center[0]) ** 2 + (j - self.i_center[1]) ** 2 - self.i_radius ** 2) < 0

    # 원을 plot하는 함수
    def print_map(self):
        i_circle = plt.Circle((self.i_center[0], self.i_center[1]), self.i_radius, fill=None, alpha=1, color='orange')
        plt.gca().add_patch(i_circle)

    # 벽을 얼마나 커버하는지 반환하는 함수
    def cover_amount(self, wall):
        count = 0
        for (x, y) in wall.uncovered:
            if self.in_iiwa_range(x, y):
                count += 1
            else:
                continue
        return count

    # 원이 벽의 어떤 점을 커버하는지 계산하여 원의 멤버 변수에 저장
    def calc_cover_points(self, wall):
        for (x, y) in zip(wall.xpoints, wall.ypoints):
            if self.in_iiwa_range(x, y):
                self.cover_point.append((x, y))
            else:
                continue
        # print(f'covers {len(self.cover_point)} points')
        self.cover_wall_amount = len(self.cover_point)
        return self.cover_point

    def check_include_point(self, point):
        if point in self.cover_point:
            return True
        else:
            return False


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

def generate_candidates(point_to_be_included, wall):
    IR = []
    id = 0
    limit = 0.2
    count = 10
    x_interval = generate_interval(wall.xpoints, count)
    y_interval = generate_interval(wall.ypoints, count)

    for i in range(len(x_interval)):
        for j in np.arange(y_interval[int(i)] + limit, y_interval[int(i)] + 1, 1):
            generated_circle = Iidgeback(id, round(x_interval[i], 3), round(j, 3), wall)
            if generated_circle.check_include_point(point_to_be_included):
                IR.append(generated_circle)
                # plt.scatter(generated_circle.i_center[0], generated_circle.i_center[1], s=1)
                # generated_circle.print_map()
            else:
                continue
            id += 1

    # max_count = max(IR, key=attrgetter('cover_wall_amount'))
    # print(max_count.cover_point)
    return IR[-1]

def generate_path(init_circle, wall):
    steps = [init_circle]
    wall.add_covered(init_circle)
    point_to_be_included = init_circle.cover_point[-1]
    prev_max_id = init_circle.id
    while not wall.allcovered():
        max_circle = generate_candidates(point_to_be_included, wall)
        if max_circle == None:
            break
        # plot circle
        if prev_max_id == max_circle.id:
            break
        prev_max_id = max_circle.id
        # print(max_circle.id)

        point_to_be_included = max_circle.cover_point[-1]
        wall.add_covered(max_circle)
        steps.append(max_circle)
    print("path generated with", len(steps), "circles")

    for s in steps:
        plt.scatter(s.i_center[0], s.i_center[1], s=1)
        s.print_map()
    return steps


if __name__ == "__main__":
    file_name = 'smooth_curve'
    input_wall = open_file(file_name, 'txt')
    print(f'Opened file {file_name}')
    x_wall, y_wall = plot_wall(input_wall)
    wall = Wall(x_wall, y_wall)

    # 그리기 관련 부분
    fig = plt.figure(figsize=(8, 3))
    axes = plt.gca()

    # 후보 생성 및 그리디 알고리즘 적용
    init_circle = Iidgeback(-1, x_wall[0], y_wall[0], wall)

    print(init_circle.cover_point)
    steps = generate_path(init_circle, wall)

    # to_gazebo_cmd_format(steps)

    # 그리는 부분
    plt.plot(x_wall, y_wall, color="grey")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
