class a:
    def __init__(self):
        self.n = 1

# list = []
# # for i in range(3):
# #     list.append(a())
# b = a()
# c = a()
# d = a()
# list.append(b)
# list.append(c)
# list.append(d)
# print(list)
# list.remove(c)
# print(list)
#import matplotlib.pyplot as plt
# x = [0, 1]
# y = [0, -1]
# plt.plot((0, 0), (1, 0), (1, 1), (0, 1))
# plt.show()

# from matplotlib import pyplot as plt
# from matplotlib.patches import Rectangle
#
# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, fill=None, alpha=1))
# plt.show()

from gekko import gekko
import numpy as np
import matplotlib.pyplot as plt

"""
minimize y
s.t.     y = f(x)

using cubic spline with random sampling of data
"""

# Function to generate data for cspline
def f(x):
    return 3*np.sin(x) - (x-3)

# # Create model
# c = gekko()
#
# # Cubic spline
# x = c.Var(value=15)
# y = c.Var()
# x_data = np.random.rand(50)*10+10
# y_data = f(x_data)
# c.cspline(x,y,x_data,y_data,True)
# c.Obj(y)
#
# # Options
# c.options.IMODE = 3
# c.options.CSV_READ = 0
# c.options.SOLVER = 3
# c.solve()

# Generate continuous trend for plot
z = np.linspace(10,20,100)
plt.plot(z,f(z),'r-',label='original')
# Check if solved successfully
# if c.options.SOLVESTATUS == 1:
#     plt.figure()
#
#     plt.scatter(x_data,y_data,5,'b',label='data')
#     plt.scatter(x.value,y.value,200,'k','x',label='minimum')
#     plt.legend(loc='best')
# else:
#     print ('Failed to converge!')
#     plt.figure()
#     plt.plot(z,f(z),'r-',label='original')
#     plt.scatter(x_data,y_data,5,'b')
#     plt.legend(loc='best')

fig = plt.gcf()
ax = fig.gca()
circle = plt.Circle((1,2 ), 1, fill=None, alpha=1)
ax.add_patch(circle)
plt.show()