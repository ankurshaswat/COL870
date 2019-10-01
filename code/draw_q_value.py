"""
Draw 3d graph of q value function from graph
"""
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

from achieve31 import Simulator


def generate_func(q_loc, action_loc, t1_val, t2_val, t3_val):
    """
    Generate a function which encodes states using provided Q and action.
    """
    def func(x_loc, y_loc):
        """
        Function to output z based on x and Y_RANGE.
        """
        state = {
            'total': x_loc,
            'trump1': t1_val,
            'trump2': t2_val,
            'trump3': t3_val,
            'dealer_card': y_loc,
        }
        # print(state)
        state_enc = SIM.encode(state)
        return q_loc[action_loc][state_enc]
    return func


def generate_x_y_z(x_start, x_end, y_start, y_end, func):
    """
    generate x y z in shape to create wireframe
    """
    x_range = np.arange(x_start, 1+x_end)
    y_range = np.arange(y_start, 1+y_end)
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    z_mesh = np.zeros(x_mesh.shape)
    for i in range(x_mesh.shape[0]):
        for j in range(x_mesh.shape[1]):
            z_mesh[i, j] = func(x_mesh[i, j], y_mesh[i, j])

    return x_mesh, y_mesh, z_mesh


def load_q_function(filename, num_states):
    """
    Load q function from file
    """
    q_func = {}

    with open(filename) as file:
        for _ in range(2):
            action = file.readline().strip()
            q_func[action] = {}
            for i in range(num_states):
                score = float(file.readline().strip().split()[1])
                q_func[action][i] = score
    return q_func


if __name__ == "__main__":
    FILENAME = sys.argv[1]

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    Q = load_q_function(FILENAME, NUM_STATES)

    FIG = plt.figure()

    FUNC = generate_func(Q, 'hit', 1, 1, 1)
    X, Y, Z = generate_x_y_z(-30, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(421, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 3 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 1, 1)
    X, Y, Z = generate_x_y_z(-6, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(422, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 3 Trumps')

    FUNC = generate_func(Q, 'hit', 1, 1, 0)
    X, Y, Z = generate_x_y_z(-20, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(423, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 2 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 1, 0)
    X, Y, Z = generate_x_y_z(4, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(424, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 2 Trumps')

    FUNC = generate_func(Q, 'hit', 1, 0, 0)
    X, Y, Z = generate_x_y_z(-10, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(425, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 1 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 0, 0)
    X, Y, Z = generate_x_y_z(14, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(426, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 1 Trumps')

    FUNC = generate_func(Q, 'hit', 0, 0, 0)
    X, Y, Z = generate_x_y_z(0, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(427, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 0 Trumps')

    FUNC = generate_func(Q, 'stick', 0, 0, 0)
    X, Y, Z = generate_x_y_z(24, 31, 1, 10, FUNC)
    AX = FIG.add_subplot(428, projection='3d')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 0 Trumps')

    plt.show()
