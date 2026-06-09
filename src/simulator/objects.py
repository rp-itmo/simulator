import numpy as np
import math
from simulator.spatial.se import SE3, se3, skew
from simulator.spatial.so import SO3, so3


def mcI(mass, com, Icm):
    I = np.zeros((6, 6))
    C = skew(com)
    I[0:3, 0:3] = Icm + mass * C @ C.T
    I[0:3, 3:6] = mass * C
    I[3:6, 0:3] = mass * C.T
    I[3:6, 3:6] = mass * np.eye(3)
    return I


class RobotTree:
    def __init__(self):
        self.xfd = np.zeros(6)
        self.q = np.zeros(1)
        self.qd = np.zeros(1)
        self.model = {}
        self.positions = []

    def some_tree(self, nb, bf=1, skew=0, taper=1):
        model = {}
        model["gravity"] = np.array([0.0, -9.81, 0.0])  # WARN: hardcoded for now
        model["NB"] = nb

        self.q = np.zeros(nb)
        self.qd = np.zeros(nb)

        model["jtype"] = []
        model["parent"] = np.zeros(nb, dtype=int)
        model["Xtree"] = []
        model["I"] = []

        for i in range(nb):
            model["jtype"].append("Rz")
            model["parent"][i] = int(np.floor(i - 2 + np.ceil(bf)) / bf)
            model["parent"][0] = -1

            if model["parent"][i] == -1:
                model["Xtree"].append(SE3(SO3().matrix, [0, 0, 0]).adjoint())
            else:
                model["Xtree"].append(
                    SE3(SO3.rx(skew).T).adjoint()
                    @ SE3(SO3().matrix, [model["parent"][i].size, 0, 0]).adjoint()
                )

            len_i = taper ** (i)
            mass = taper ** (3 * (i))
            CoM = len_i * np.array([0.5, 0, 0])
            Icm = mass * len_i**2 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])

            model["I"].append(mcI(mass, CoM, Icm))

        self.model = model


class TwoLink:
    def __init__(self):
        self.model = {
            "NB": 2,
            "jtype": ["Rz", "Rz"],
            "parent": [-1, 0],
            "Xtree": [
                SE3(SO3().matrix, [0, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
            ],
            "I": [
                mcI(1.0, np.array([0.5, 0, 0]), np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.0, np.array([0.5, 0, 0]), np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
            ],
            "gravity": np.array([0.0, -9.81, 0.0]),
        }
        self.q = np.zeros(self.model["NB"])
        self.qd = np.zeros(self.model["NB"])


class Tree7:
    def __init__(self):
        self.model = {
            "NB": 8,
            "jtype": ["Rz", "Rz", "Rz", "Rz", "Rz", "Rz", "Rz", "Rz"],
            "parent": [-1, 0, 1, 1, 2, 2, 3, 3],
            "Xtree": [
                SE3(SO3().matrix, [0, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
            ],
            "I": [
                mcI(1.5, np.array([0.5, 0, 0]), 1.5 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.4, np.array([0.5, 0, 0]), 1.4 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.3, np.array([0.5, 0, 0]), 1.3 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.2, np.array([0.5, 0, 0]), 1.2 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.1, np.array([0.5, 0, 0]), 1.1 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.01, np.array([0.5, 0, 0]), 1.01 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.02, np.array([0.5, 0, 0]), 1.02 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.03, np.array([0.5, 0, 0]), 1.03 * np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
            ],
            "gravity": np.array([0.0, -9.81, 0.0]),
        }
        self.q = np.zeros(self.model["NB"])
        self.qd = np.zeros(self.model["NB"])


class CartPole:
    def __init__(self):
        self.model = {
            "NB": 2,
            "jtype": ["Px", "Rz"],
            "parent": [-1, 0],
            "Xtree": [
                SE3(SO3().matrix, [0, 0, 0]).adjoint(),
                SE3(SO3().matrix, [1, 0, 0]).adjoint(),
            ],
            "I": [
                mcI(1.0, np.array([0.5, 0, 0]), np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
                mcI(1.0, np.array([0.5, 0, 0]), np.diag([0.0025, 1.015 / 12, 1.015 / 12])),
            ],
            "gravity": np.array([0.0, -9.81, 0.0]),
        }
        self.q = np.zeros(self.model["NB"])
        self.qd = np.zeros(self.model["NB"])


if __name__ == "__main__":
    robot = RobotTree()
    robot.some_tree(8, 2)

    np.set_printoptions(precision=4)
    # for m in robot.model:
    #     print(f"{m}")
    #     if type(robot.model[m]) is list:
    #         for it in robot.model[m]:
    #             print(f"{it}")
    #     else:
    #         print(f"{robot.model[m]}")

    r = Tree7()

    for key in robot.model:
        print(robot.model[key], r.model[key])
    # print(robot.model)

    # print(r.model)
    # robot = TwoLink()
    # print(robot)
