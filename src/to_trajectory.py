from tools import *
import random
def find_closest(start, end, wall_x, wall_y):
    color = "#" + ''.join([random.choice('0123455436789ABCDEF') for j in range(6)])
    trajectory_x = []
    trajectory_y = []
    wall_start = wall_x.index(min(wall_x, key=lambda x: abs(x - start[0])))
    wall_end = wall_x.index(min(wall_x, key=lambda x: abs(x - end[0])))
    y_diff = round( (end[1] - wall_y[wall_end] + start[1] - wall_y[wall_start])/2 , 3)

    for i in range(wall_start, wall_end):
        trajectory_x.append(round(wall_x[i],3))
        trajectory_y.append(round(wall_y[i] - y_diff, 3))
    plt.scatter(trajectory_x, trajectory_y, c=color, s=2)
    return zip(trajectory_x, trajectory_y)

if __name__=='__main__':
    trajectory = []

    x_points = [-0.04099999999999998, 0.68, 1.231]
    y_points = [-1.505, -1.5619999999999998, -1.505]
    y_points_abs = [abs(x)+0.8 for x in y_points]
    x_positive = [x for x in x_points]
    y_positive = [abs(y) - 0.8 for y in y_points]
    file_name = 'wood_bee_hive_line'
    input_wall = open_file(file_name, 'obj')

    wall_x, wall_y = plot_wall(input_wall)
    # wall_x = [-1.649, -1.532, -1.449, -1.395, -1.361, -1.341, -1.328, -1.316, -1.296, -1.262, -1.207, -1.125, -1.008, -0.862, -0.696, -0.513, -0.313, -0.1, 0.127, 0.364, 0.612, 0.868, 1.13, 1.398, 1.669, 1.923, 2.142, 2.333, 2.501, 2.652, 2.79, 2.923, 3.054, 3.19, 3.337, 3.499, 3.683, 3.857, 3.991, 4.096, 4.18, 4.253, 4.322, 4.398, 4.489, 4.605, 4.754, 4.946, 5.189, 5.423, 5.591, 5.706, 5.781, 5.829, 5.864, 5.9, 5.949, 6.024, 6.14, 6.308, 6.544, 6.79, 6.987, 7.146, 7.276, 7.387, 7.489, 7.59, 7.701, 7.831, 7.99, 8.187, 8.433, 8.676, 8.864, 9.009, 9.121, 9.211, 9.291, 9.371, 9.461, 9.574, 9.718, 9.907, 10.149]
    # wall_y = [-4.953, -5.023, -5.072, -5.105, -5.124, -5.136, -5.143, -5.15, -5.161, -5.181, -5.213, -5.263, -5.333, -5.394, -5.421, -5.418, -5.395, -5.356, -5.31, -5.264, -5.224, -5.198, -5.192, -5.213, -5.269, -5.339, -5.396, -5.441, -5.473, -5.49, -5.492, -5.478, -5.448, -5.401, -5.335, -5.251, -5.147, -5.039, -4.942, -4.857, -4.784, -4.722, -4.671, -4.63, -4.6, -4.581, -4.572, -4.573, -4.584, -4.62, -4.692, -4.792, -4.914, -5.049, -5.191, -5.331, -5.462, -5.578, -5.669, -5.729, -5.751, -5.741, -5.711, -5.667, -5.612, -5.55, -5.483, -5.417, -5.354, -5.299, -5.255, -5.226, -5.215, -5.23, -5.271, -5.332, -5.41, -5.497, -5.59, -5.683, -5.771, -5.848, -5.91, -5.95, -5.965]
    wall_y_abs = [abs(x) for x in wall_y]
    wall = list(zip(wall_x, wall_y_abs))
    path = list(zip(x_positive, y_positive))
    for i in range(0, len(path)-1):
        trajectory.extend(find_closest(path[i], path[i+1], wall_x, wall_y_abs))
    x_step, y_step = to_gazebo_cmd_format_list(trajectory)
    plt.scatter(x_points, y_points_abs, c='pink')

    # plt.scatter(x_step, y_step)
    plt.plot(wall_x, wall_y_abs)
    plt.show()

    # print(trajectory)