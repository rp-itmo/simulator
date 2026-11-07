import numpy as np
import mujoco

from config import MODEL


m = mujoco.MjModel.from_xml_path(MODEL)
print(m.opt.gravity)
print(mujoco.mj_getTotalmass(m))


def controller(q, dq, t, knee_sit, thigh_jump, kp_jump):
    q_home = np.array([0, 0.9, -1.8] * 4)
    q_sit  = np.array([0, -knee_sit / 2, knee_sit] * 4)
    q_jump = np.array([0, thigh_jump, -0.9] * 4)

    if t <= 2.0:  # стойка
        q_dest = q_home
        Kp = 100
    elif t <= 4.0:  # присед
        q_dest = q_sit
        Kp = 100
    elif t < 4.5:  # толчок: своя сила
        q_dest = q_jump
        Kp = kp_jump
    else:  # полёт и приземление
        q_dest = q_home
        Kp = 100

    torques = Kp * (q_dest - q) - 1 * dq  # Kp вместо 100
    return torques


def run_jump(knee_sit, thigh_jump, kp_jump):  # новый аргумент kp_jump
    d = mujoco.MjData(m)
    mujoco.mj_resetDataKeyframe(m, d, m.key("home").id)
    mujoco.mj_forward(m, d)  # посчитать центр масс до первого шага, иначе там нули

    base = m.body("base").id
    x0 = d.subtree_com[base][0]  # x центра масс всего оробота на старте

    while d.time < 7.0:
        d.ctrl[:] = controller(d.qpos[3:], d.qvel[3:], d.time, 
                               knee_sit, thigh_jump, kp_jump)
        mujoco.mj_step(m, d)

    length = d.subtree_com[base][0] - x0
    if abs(d.qpos[2]) > 0.3:  # корпус сильно наклонён: упала
        length = 0.0

    return length


def test():
    best_length = 0.0
    best_params = None

    with open("jump_results.txt", "w", encoding="utf-8") as f:
        for knee_sit in np.linspace(-2.7, -1.8, 7):  # только реальные приседы
            for thigh_jump in np.linspace(1.2, 2.0, 9):  # сетка сдвинута вправо
                for kp_jump in [50, 100, 200, 300]:  # новый цикл по силе толчка
                    length = run_jump(knee_sit, thigh_jump, kp_jump)
                    line = (f"колено приседа {knee_sit:.2f}, бедро толчка {thigh_jump:.2f}, "
                            f"Kp толчка {kp_jump} -> {length:.3f} м")
                    print(line)
                    f.write(line + "\n")
                    if length > best_length:
                        best_length = length
                        best_params = (knee_sit, thigh_jump, kp_jump)

        result = (f"Лучший прыжок: {best_length:.3f} м при колене приседа {best_params[0]:.2f}, "
                  f"бедре толчка {best_params[1]:.2f}, Kp толчка {best_params[2]}")
        print(result)
        f.write(result + "\n")

    return best_params


if __name__ == "__main__":
    test()
