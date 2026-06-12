import numpy as np

from ..spatial.so import SO3, so3
from ..spatial.se import SE3, se3, crm, crf


class ABAlgorithm:
    def __init__(self):
        pass

    def forward_dynamics(self, obj, q, qd, tau, f_ext=None):
        model = obj.model

        a_grav = self.get_gravity(model)
        NB = model["NB"]

        Xup = {}
        S = {}
        v = {}
        c = {}
        IA = {}
        pA = {}

        for i in range(NB):
            XJ, S[i] = self.jcalc(model["jtype"][i], q[i])
            vJ = S[i] * qd[i]
            Xup[i] = XJ @ model["Xtree"][i]

            if model["parent"][i] == -1:
                v[i] = vJ
                c[i] = np.zeros_like(a_grav)
            else:
                v[i] = Xup[i] @ v[model["parent"][i]] + vJ
                c[i] = crm(v[i]) @ vJ

            IA[i] = model["I"][i]
            pA[i] = crf(v[i]) @ model["I"][i] @ v[i]

        if f_ext is not None:
            pA = self.apply_external_forces(model["parent"], Xup, pA, f_ext)

        U = {}
        d = {}
        u = {}

        for i in reversed(range(NB)):
            U[i] = IA[i] @ S[i]
            d[i] = (S[i].T @ U[i])[0, 0]  # Extract scalar from 1x1 matrix
            u[i] = tau[i] - (S[i].T @ pA[i])[0, 0]

            parent = model["parent"][i]
            if parent != -1:
                Ia = IA[i] - np.outer(U[i], U[i]) / d[i]
                pa = pA[i] + Ia @ c[i] + (U[i] * u[i] / d[i])

                IA[parent] = IA[parent] + Xup[i].T @ Ia @ Xup[i]
                pA[parent] = pA[parent] + Xup[i].T @ pa

        a = {}
        qdd = np.zeros(NB)

        for i in range(NB):
            parent = model["parent"][i]
            if parent == -1:
                a[i] = Xup[i] @ (-a_grav) + c[i]
            else:
                a[i] = Xup[i] @ a[parent] + c[i]
            qdd[i] = (u[i] - (U[i].T @ a[i])[0, 0]) / d[i]  # Extract scalar from 1x1 matrix
            a[i] = a[i] + S[i].dot(qdd[i])

        return qdd

    def get_gravity(self, model):
        g = np.array(model["gravity"])
        a_grav = np.array([0, 0, 0, g[0], g[1], g[2]]).reshape(6, 1)
        return a_grav

    def apply_external_forces(self, parent, Xup, pA, f_ext):
        pass

    def jcalc(self, jtyp, q):
        joint_map = {
            "Rx": (lambda q: SE3(SO3.rx(q).T).adjoint(), np.array([[1], [0], [0], [0], [0], [0]])),
            "Ry": (lambda q: SE3(SO3.ry(q).T).adjoint(), np.array([[0], [1], [0], [0], [0], [0]])),
            "Rz": (lambda q: SE3(SO3.rz(q).T).adjoint(), np.array([[0], [0], [1], [0], [0], [0]])),
            "Px": (
                lambda q: SE3(SO3().matrix, [q, 0, 0]).adjoint(),
                np.array([[0], [0], [0], [1], [0], [0]]),
            ),
            "Py": (
                lambda q: SE3(SO3().matrix, [0, q, 0]).adjoint(),
                np.array([[0], [0], [0], [0], [1], [0]]),
            ),
            "Pz": (
                lambda q: SE3(SO3().matrix, [0, 0, q]).adjoint(),
                np.array([[0], [0], [0], [0], [0], [1]]),
            ),
        }

        code = jtyp if isinstance(jtyp, str) else jtyp.get("code")

        transform_fn, S = joint_map[code]

        Xj = transform_fn(q)

        return Xj, S
