import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 40, 0.1)
y = np.sin(x * 0.5)
axes = plt.gca()
axes.set_xlim([0, 40])
axes.set_ylim([-2, 2])
plt.plot(x, y)
plt.show()
print(x)
print(y)

radius = 2
theta = np.linspace(0, 2 * np.pi, 100)
x = radius * np.cos(theta)
y = radius * np.sin(theta)
X = np.linspace(-2, 2, 100)
plt.plot(X, y)
plt.axis('equal')
plt.title('Circle')
plt.show()