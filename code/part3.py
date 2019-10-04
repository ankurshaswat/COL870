"""
Code to compare performance according to part 3 of Q4
"""
import random
import sys

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from achieve31 import (Simulator, forward_view_td_lambda,
                       k_step_lookahed_sarsa, q_learning,
                       test_policy_on_starts, test_q_func_on_starts, test_policy, test_q_func)

if __name__ == "__main__":
    random.seed(12345)

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    NUM_EPISODES = int(sys.argv[1])
    NUM_TEST_EPISODES = int(sys.argv[2])

    # TEST_STARTS = []
    # for test_num in range(NUM_TEST_EPISODES):
    #     TEST_STARTS.append(SIM.reset())

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for k in [1, 10, 100, 1000]:
        x = []
        y = []
        for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
            greedy_pi, _ = k_step_lookahed_sarsa(
                SIM, k, alpha, 0.1, 1, NUM_EPISODES)
            rew = test_policy(SIM, greedy_pi, NUM_TEST_EPISODES)
            # rew = test_policy_on_starts(SIM, greedy_pi, TEST_STARTS)
            print('{} step lookahead SARSA: alpha={} Reward={}'.format(
                k, alpha, rew))
            y.append(rew)
            x.append(alpha)
        ax.plot(x, y, marker='o', label=str(k)+" step lookahead SARSA")

    for k in [1, 10, 100, 1000]:
        x = []
        y = []
        for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
            greedy_pi, _ = k_step_lookahed_sarsa(
                SIM, k, alpha, 0.1, 1, NUM_EPISODES, True)
            rew = test_policy(SIM, greedy_pi, NUM_TEST_EPISODES)
            # rew = test_policy_on_starts(SIM, greedy_pi, TEST_STARTS)
            y.append(rew)
            x.append(alpha)
            print('{} step lookahead SARSA with Decay: alpha={} Reward={}'.format(
                k, alpha, rew))
        ax.plot(x, y, marker='o', label=str(k)+" step lookahead SARSA decayed")

    x = []
    y = []
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
        q_func, _ = q_learning(SIM, alpha, 0.1, 1, NUM_EPISODES)
        # rew = test_q_func_on_starts(SIM, q_func, TEST_STARTS)
        rew = test_q_func(SIM, q_func, NUM_TEST_EPISODES)
        y.append(rew)
        x.append(alpha)
        print('Q Learning: alpha={} Reward={}'.format(alpha, rew))
    ax.plot(x, y, marker='o', label="Q Learning")

    x = []
    y = []
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
        q_func, _ = forward_view_td_lambda(
            SIM, alpha, 0.5, 0.1, 1, NUM_EPISODES)
        rew = test_q_func(SIM, q_func, NUM_TEST_EPISODES)
        # rew = test_q_func_on_starts(SIM, q_func, TEST_STARTS)
        y.append(rew)
        x.append(alpha)
        print('TD(0.5) Decayed: alpha={} Reward={}'.format(alpha, rew))
    ax.plot(x, y, marker='o', label="TD(0.5) Decayed")

    plt.xlabel('Alpha')
    plt.ylabel('Average Rewards')
    plt.legend()
    plt.show()
