import numpy

from plot_input import *
import numpy as np

def draw_tangent_line(p1, p2):
    plt.axline( (p1[0], p2[0]), (p1[1], p2[1]))

def draw_multiple_tangent_lines(x, y):
    for i in range(len(x)-1):
        draw_tangent_line(x[i:i+2], y[i:i+2])

def draw_two_tangent_lines(x, y):
    draw_multiple_tangent_lines((x[0], x[len(x) // 2], x[-1]), (y[0], y[len(y) // 2], y[-1]))
    plt.scatter(x[0], y[0], c='red', s=100)
    plt.scatter(x[len(x) // 2], y[len(y) // 2], c='red', s=100)
    plt.scatter(x[-1], y[-1], c='red', s=100)

def between_angle(x, y):
    vector_1 = numpy.array([x[0], y[0]]) - numpy.array([x[len(x) // 2], y[len(y) // 2]])
    vector_2 = numpy.array([x[len(x) // 2],  y[len(y) // 2]]) - np.array([x[-1], y[-1]])

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    print(vector_1, vector_2)
    print(angle)
    print(angle*90)
    plt.text(x[len(x) // 2]-0.2,  y[len(y) // 2]-0.2, f'{round(angle*90, 2)}', fontsize=10)

    return angle*90

if __name__=='__main__':
    filename = "smooth_curve"
    fileext='txt'
    wall = open_file(filename, fileext)
    x, y = plot_wall(wall, 100)

    range_1, range_2 = 30, 60
    # draw_two_tangent_lines(x[::10], y[::10])
    # between_angle(x[::10], y[::10])

    for i in range(len(x)//5):
        if between_angle(x[i:i*5-1], y[i:i*5-1])<=90:
            draw_two_tangent_lines(x[i:i * 5 - 1], y[i:i * 5 - 1])
    plt.show()

