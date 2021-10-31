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

    x_points = [-0.553, 0.246, 1.624, 2.834, 2.79, 4.322, 5.604, 6.776, 6.878, 8.433, 9.974]
    y_points = [4.469, 4.287, 4.31, 4.487, 4.492, 3.671, 3.703, 4.792, 4.778, 4.215, 4.954]
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
    plt.plot(wall_x, wall_y_abs)
    plt.show()
    plt.plot(x_step, y_step)
