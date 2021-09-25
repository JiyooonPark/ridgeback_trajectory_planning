import matplotlib.pyplot as plt

def open_file(filename, fileext):
    point = []
    wall = []
    with open('../input/'+filename+'.'+fileext) as f:
        for line in f:
            if line[0]!='v':
                continue
            for word in line.split():
                if word =='v':
                    point = []
                    continue
                else:
                    point.append(float(word))
            wall.append(point)
    return wall

def plot_wall(wall, size=0.4):
    x_wall = []
    y_wall = []
    z_wall = []

    marker_shape="o"

    for [x, y, z] in wall:
        x_wall.append(x)
        y_wall.append(y)
        z_wall.append(z)
    plt.figure(figsize=(20, 3))
    if x_wall[0] == 0:
        plt.scatter(y_wall, z_wall, c='indigo', s=size, marker=marker_shape)
        print('zero: x')
        return y_wall, z_wall
    elif y_wall[0] == 0:
        plt.scatter(x_wall, z_wall, c='indigo', s=size, marker=marker_shape)
        print('zero: y')
        return x_wall, z_wall
    elif z_wall[0] == 0:
        plt.scatter(x_wall, y_wall, c='indigo', s=size, marker=marker_shape)
        print('zero: z')
        return x_wall, y_wall

if __name__=='__main__':
    filename = "smooth_curve"
    fileext='txt'
    wall = open_file(filename, fileext)
    plot_wall(wall)
