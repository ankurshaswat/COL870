"""
Draw 3d graph of q value function from graph
"""
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

from achieve31 import Simulator, load_q_function


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


def get_new_plt(title):
    """
    Define and return new plot for new figure
    """
    fig = plt.figure(num=title)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    axx = fig.add_subplot(111, projection='3d')
    axx.set_xlabel('Player Raw Score')
    axx.set_ylabel('Dealer Card')
    axx.set_zlabel('Q Value')
    return axx


if __name__ == "__main__":
    FILENAME = sys.argv[1]

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    Q = load_q_function(FILENAME, NUM_STATES)

    FUNC = generate_func(Q, 'hit', 1, 1, 1)
    X, Y, Z = generate_x_y_z(-30, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(421, projection='3d')
    AX = get_new_plt('hit 3 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 3 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 1, 1)
    X, Y, Z = generate_x_y_z(-30, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(422, projection='3d')
    AX = get_new_plt('stick 3 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 3 Trumps')

    FUNC = generate_func(Q, 'hit', 1, 1, 0)
    X, Y, Z = generate_x_y_z(-20, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(423, projection='3d')
    AX = get_new_plt('hit 2 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 2 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 1, 0)
    X, Y, Z = generate_x_y_z(-20, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(424, projection='3d')
    AX = get_new_plt('stick 2 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 2 Trumps')

    FUNC = generate_func(Q, 'hit', 1, 0, 0)
    X, Y, Z = generate_x_y_z(-10, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(425, projection='3d')
    AX = get_new_plt('hit 1 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 1 Trumps')

    FUNC = generate_func(Q, 'stick', 1, 0, 0)
    X, Y, Z = generate_x_y_z(-10, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(426, projection='3d')
    AX = get_new_plt('stick 1 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 1 Trumps')

    FUNC = generate_func(Q, 'hit', 0, 0, 0)
    X, Y, Z = generate_x_y_z(0, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(427, projection='3d')
    AX = get_new_plt('hit 0 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Hit - 0 Trumps')

    FUNC = generate_func(Q, 'stick', 0, 0, 0)
    X, Y, Z = generate_x_y_z(0, 31, 1, 10, FUNC)
    # AX = FIG.add_subplot(428, projection='3d')
    AX = get_new_plt('stick 0 trump')
    AX.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    AX.set_title('Stick - 0 Trumps')

    plt.show()
