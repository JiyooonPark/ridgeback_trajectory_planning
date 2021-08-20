x_wall = []
with open('wall.txt') as f:
    for line in f:
        for word in line.split():
            x_wall.append(float(word))
print(x_wall)
y_wall = []
with open('y_wall.txt') as f:
    for line in f:
        for word in line.split():
            y_wall.append(float(word))
print(y_wall)

import numpy as np
import matplotlib.pyplot as plt

x = x_wall
y = y_wall
axes = plt.gca()
plt.scatter(x, y)
plt.show()

plt.show()