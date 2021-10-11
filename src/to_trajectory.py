from tools import *
import random
def find_closest(start, end, wall_x, wall_y):
    color = "#" + ''.join([random.choice('0123455436789ABCDEF') for j in range(6)])
    trajectory_x = []
    trajectory_y = []
    wall_start = wall_x.index(min(wall_x, key=lambda x: abs(x - start[0])))
    wall_end = wall_x.index(min(wall_x, key=lambda x: abs(x - end[0])))
    # y_diff = round( (end[1] - wall_y[wall_end] + start[1] - wall_y[wall_start])/2 , 3)
    y_diff = start[1] - wall_y[wall_start]
    for i in range(wall_start, wall_end):
        trajectory_x.append(round(wall_x[i],3))
        trajectory_y.append(round(wall_y[i] + y_diff, 3))
    plt.scatter(trajectory_x, trajectory_y, c=color, s=2)
    return zip(trajectory_x, trajectory_y)

if __name__=='__main__':
    fig = plt.figure(figsize=(8, 3))
    axes = plt.gca()
    trajectory = []

    x_points = [-0.864, 0.246, 1.624, 2.834, 3.329, 4.322, 5.604, 6.465, 7.417, 8.433, 9.663]
    y_points = [5.008, 4.909, 4.932, 5.109, 4.803, 4.293, 4.325, 5.331, 5.089, 4.837, 5.493]
    # y_points_abs = [abs(x)+0.8 for x in y_points]
    # x_positive = [x+0.4 for x in x_points]
    # y_positive = [abs(y) - 0.8 for y in y_points]
    file_name = 'smooth_curve'
    input_wall = open_file(file_name, 'txt')

    wall_x, wall_y = plot_wall(input_wall)
    wall_y_abs = [abs(x) for x in wall_y]
    wall = list(zip(wall_x, wall_y_abs))
    path = list(zip(x_points, y_points))
    for i in range(0, len(path)):
        trajectory.append([-100,-100+0.2])
        # trajectory.extend(find_closest(path[i], path[i+1], wall_x, wall_y_abs))
        trajectory.append([x_points[i], y_points[i]])
        trajectory.append([100, 100+0.2])
    x_step, y_step = to_gazebo_cmd_format_list(trajectory)
    # plt.scatter(x_points, y_points_abs, c='pink')
    print()
    # print(y_positive)
    # plt.scatter(x_step, y_step)
    plt.plot(wall_x, wall_y_abs)
    plt.show()
    plt.plot(x_step, y_step)

    # print(trajectory)