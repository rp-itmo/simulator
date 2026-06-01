import numpy as np


class Robot:
    def init(self):
        self.model = {
            "parent": [-1, 0, 1, 2]
        }

        self.q = np.array([
            0.0,
            0.5,
            -0.4,
            0.3
        ])

        self.position = [
            0.0,
            0.0,
            0.0
        ]

    def get_position(self):
        return self.position

    def update(self):
        self.q[0] += 0.02
        self.q[1] += 0.015
        self.q[2] -= 0.01
        self.q[3] += 0.008

        self.position[0] += 0.15