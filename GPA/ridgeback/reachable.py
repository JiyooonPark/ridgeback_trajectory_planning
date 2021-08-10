import numpy as np
from matplotlib import pyplot as plt

class reachable():
    def __init__(self, id, x, y, radius = 1):
        self.id = id
        self.center = [x, y]
        self.radius = radius
        self.covers = self.generate_cover()
        self.overlapped = []
    def generate_cover(self):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.radius * np.cos(theta)
        y = self.radius * np.sin(theta)
        # for X in range(int(x)):
    def update_overlap(self, steps):
        for circle in steps:
            if self.check_overlap(circle):
                self.overlapped.append(circle.id)
            else:
                continue
    def check_overlap(self, circle):
        pass
