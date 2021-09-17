def open_file(filename, fileext):
    point = []
    wall = []
    with open('../input/' + filename + '.' + fileext) as f:
        for line in f:
            if line[0] != 'v':
                continue
            for word in line.split():
                if word == 'v':
                    point = []
                    continue
                else:
                    point.append(float(word))
            wall.append(point)
    # print(wall)
    return wall


def plot_wall(wall):
    x_wall = []
    y_wall = []
    z_wall = []

    for [x, y, z] in wall:
        x_wall.append(x)
        y_wall.append(y)
        z_wall.append(z)

    if x_wall[0] == 0:
        return y_wall, z_wall
    elif y_wall[0] == 0:
        return x_wall, z_wall
    elif z_wall[0] == 0:
        return x_wall, y_wall
    else:
        print('no axis with zero value')
    # plt.show()
    print(x_wall)
    return x_wall, y_wall


def setting(circle):
    print('c:', circle.r_center)
    return circle.r_center[0]

# when the final trajectory is given as output,
# outputs the gazebo executable list or ridgeback positions
def to_gazebo_cmd_format(steps):
    sorted_path = sorted(steps, key=setting)
    print('X:')
    for s in sorted_path:
        print(s.r_center[0], end=', ')
    print('\nY:')
    for s in sorted_path:
        print(s.r_center[1], end=', ')

# when generating candidates, generates intervals btw dots
import numpy
def generate_interval(wall, count):
    interval_wall = []
    for i in range(len(wall) - 1):
        interval_wall.extend(numpy.linspace(wall[i], wall[i + 1], count))
    print(interval_wall)
    return interval_wall

def generate_denser_wall(wall, count):
    dense_wall = []
    for i in range(len(wall)):
        dense_wall.extend(numpy.linspace(wall[i], wall[i + 1], count))


import math
import matplotlib.pyplot as plt
def point_in_circumference(r,n=6):
    pi = math.pi
    return [(round(math.cos(pi/n*x)*r, 2),round(-math.sin(pi/n*x)*r, 2)) for x in range(0,n+1)]

if __name__=='__main__':

    res = point_in_circumference(10)
    print(res)
    x_list, y_list = [], []
    for x, y in res:
        x_list.append(x)
        y_list.append(y)
    plt.scatter(x_list, y_list)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()