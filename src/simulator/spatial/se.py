import numpy as np
#from spatial.so import SO3, so3
from .so import SO3, so3

def skew(v):
    v = v.flatten()
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def unskew(A):
    return 0.5 * np.array([A[2, 1] - A[1, 2], A[0, 2] - A[2, 0], A[1, 0] - A[0, 1]])


def crm(v):
    return np.block([[skew(v[:3]), np.zeros((3, 3))], [skew(v[3:]), skew(v[:3])]])


def crf(v):
    return -crm(v).T


class se3:
    def __init__(self, w, v):
        self.w = np.array(w, dtype=float).reshape(3, 1)
        self.v = np.array(v, dtype=float).reshape(3, 1)

    @property
    def twist(self):
        return np.stack([w, v])

    def hat(self):
        w_hat = so3.hat(self.w)
        return np.vstack([np.hstack([w_hat, self.v]), np.zeros((1, 4))])

    @staticmethod
    def vee(twist_hat):
        w_hat = twist_hat[:3, :3]
        v = twist_hat[:3, 3].reshape(3, 1)
        w_vee = so3.vee(w_hat)  # Возвращает array(3)
        return se3(w_vee, v)

    def exp(self):
        """Exponential map: se(3) -> SE(3)"""
        theta = np.linalg.norm(self.w)
        if theta < 1e-9:
            R = np.eye(3)
            t = self.v
        else:
            so3_obj = so3(self.w)
            R = so3_obj.exp().matrix
            k = self.w / theta
            K = so3.hat(k)
            B = (1 - np.cos(theta)) / (theta**2)
            D = (theta - np.sin(theta)) / (theta**3)
            V = np.eye(3) + B * K + D * K @ K
            t = V @ self.v
        return SE3(R, t)


class SE3:
    def __init__(self, R, t=None):
        self.R = np.array(R, dtype=float)
        self.t = np.zeros(3) if t is None else np.array(t, dtype=float).reshape(3, 1)

    @property
    def matrix(self):
        return np.vstack([np.hstack([self.R, self.t]), np.array([[0, 0, 0, 1]])])

    def compose(self, other):
        R_new = self.R @ other.R
        t_new = self.R @ other.t + self.t
        return SE3(R_new, t_new)

    def inverse(self):
        R_inv = self.R.T
        t_inv = -R_inv @ self.t
        return SE3(R_inv, t_inv)

    def adjoint(self):
        R = self.R
        t_hat = so3.hat(self.t.flatten())
        top = np.hstack([R, np.zeros((3, 3))])
        bottom = np.hstack([-R @ t_hat, R])
        return np.vstack([top, bottom])

    def act(self, point):
        p = np.array(point, dtype=float).reshape(3, 1)
        return self.R @ p + self.t

    def log(self):
        """SE(3) -> se(3)"""
        so3_obj = SO3(self.R)
        so3_log = so3_obj.log()
        w = so3_log.w
        theta = np.linalg.norm(w)
        if theta < 1e-9:
            return se3(w, self.t)
        K = so3.hat(w / theta)
        half_theta = theta / 2
        sin_half = np.sin(half_theta)
        if sin_half == 0:
            cot_half = 1.0
        else:
            cos_half = np.cos(half_theta)
            cot_half = cos_half / sin_half
        a = (1 / theta**2) * (1 - half_theta * cot_half)
        V_inv = np.eye(3) - 0.5 * K + a * (K @ K)
        v = V_inv @ self.t
        return se3(w, v)

    @staticmethod
    def from_matrix(T):
        return SE3(T[:3, :3], T[:3, 3])

    @staticmethod
    def from_axis_angle(axis, angle, t=None):
        if t is None:
            t = np.zeros((3, 1))
        else:
            t = np.array(t, dtype=float).reshape(3, 1)
        so3_obj = SO3.from_axis_angle(axis, angle)
        R = so3_obj.matrix
        return SE3(R, t)

    @staticmethod
    def from_quaternion(q, t=None):
        """q = [x, y, z, w] как в SO3"""
        if t is None:
            t = np.zeros((3, 1))
        else:
            t = np.array(t, dtype=float).reshape(3, 1)
        so3_obj = SO3.from_quaternion(q)
        R = so3_obj.matrix
        return SE3(R, t)

    @staticmethod
    def from_rotation_translation(R, t):
        return SE3(R, t)

    @staticmethod
    def from_adjoint(X):
        R = X[:3, :3]
        t = -unskew(R.T @ X[3:, :3])
        return SE3(R, t)
