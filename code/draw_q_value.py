"""
Draw 3d graph of q value function from graph
"""
import sys

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

from achieve31 import Simulator


if __name__ == "__main__":
    FILENAME = sys.argv[1]

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    Q = {}

    with open(FILENAME) as file:
        for _ in range(2):
            action = file.readline().strip()
            Q[action] = {}
            for i in range(NUM_STATES):
                score = float(file.readline().strip().split()[1])
                Q[action][i] = score

    xdata = []
    ydata = []
    zdata = []

    def generate_func(Q, action, t1, t2, t3):
        def f(x, y):
            state = {
                'total': x,
                'trump1': t1,
                'trump2': t2,
                'trump3': t3,
                'dealer_card': y,
            }
            # print(state)
            state_enc = SIM.encode(state)
            return Q[action][state_enc]
        return f

    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    # Action hit
    # Player Raw Score -30 to 30
    # Dealer from 1 to 10
    # Trump 1,1,1
    # func = generate_func(Q, 'hit', 1, 1, 1)

    # x = np.arange(-30, 32)
    # y = np.arange(1, 11)
    # X, Y = np.meshgrid(x, y)
    # Z = np.zeros(X.shape)
    # for i in range(X.shape[0]):
    #     for j in range(X.shape[1]):
    #         Z[i, j] = func(X[i, j], Y[i, j])

    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
    #                 cmap='viridis', edgecolor='none')
    # ax.set_title('q value of hit with 3 trumps')
    # plt.show()

    # func = generate_func(Q, 'stick', 1, 1, 1)

    # x = np.arange(-30, 31)
    # y = np.arange(1, 11)
    # X, Y = np.meshgrid(x, y)
    # Z = np.zeros(X.shape)
    # for x in range(-30, 1+30):
    #     for y in range(1, 1+10):

    #         # xdata.append(x)
    #         # ydata.append(y)
    #         # zdata.append(func(x,y))
    #         z = func(x, y)
    #         Z[y-1, x] = z

    # ax.plot_wireframe(X, Y, Z)
    # plt.show()

    func = generate_func(Q, 'hit', 1, 0, 0)

    x = np.arange(-10, 32)
    y = np.arange(1, 11)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = func(X[i, j], Y[i, j])

    ax1.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    # plt.show()

    func = generate_func(Q, 'hit', 0, 1, 0)

    x = np.arange(-10, 32)
    y = np.arange(1, 11)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = func(X[i, j], Y[i, j])

    ax2.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    plt.show()
