"""
Code to compare performance according to part 2 of Q4
"""

import sys

import matplotlib.pyplot as plt
import numpy as np

from achieve31 import (Simulator, average_rewards, forward_view_td_lambda,
                       k_step_lookahed_sarsa, load_q_function, q_learning)

# def rolling_average(a, n=5):
#     ret = np.cumsum(a, dtype=float)
#     ret[n:] = ret[n:] - ret[:-n]
#     return ret[n - 1:] / n


def rolling_average(a, n):
    return np.convolve(a, np.ones((n,))/n, mode='valid')


if __name__ == "__main__":
    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()
    NUM_EPISODES = int(sys.argv[1])
    PERIOD = int(NUM_EPISODES*0.30)
    NUM_EPISODES = NUM_EPISODES + PERIOD
    NUM_RUNS = int(sys.argv[2])
    # FILENAME = sys.argv[2]

    # q_func = load_q_function(FILENAME, NUM_STATES)

    for k in [1, 10, 100, 1000]:
        ALL_REWARDS = []
        for run in range(NUM_RUNS):
            _, rewards = k_step_lookahed_sarsa(
                SIM, k, 0.1, 0.1, 1, NUM_EPISODES)
            ALL_REWARDS.append(rewards)
        AVG_REWARDS = rolling_average(average_rewards(ALL_REWARDS), PERIOD)
        plt.plot(range(1, 1+len(AVG_REWARDS)), AVG_REWARDS,
                 label=str(k)+' step lookahead SARSA')

    for k in [1, 10, 100, 1000]:
        ALL_REWARDS = []
        for run in range(NUM_RUNS):
            _, rewards = k_step_lookahed_sarsa(
                SIM, k, 0.1, 0.1, 1, NUM_EPISODES, True)
            ALL_REWARDS.append(rewards)
        AVG_REWARDS = rolling_average(average_rewards(ALL_REWARDS), PERIOD)
        plt.plot(range(1, 1+len(AVG_REWARDS)), AVG_REWARDS,
                 label=str(k)+' step lookahead SARSA decayed')

    ALL_REWARDS = []
    for run in range(NUM_RUNS):
        _, rewards = q_learning(SIM, 0.1, 0.1, 1, NUM_EPISODES)
        ALL_REWARDS.append(rewards)
    AVG_REWARDS = rolling_average(average_rewards(ALL_REWARDS), PERIOD)
    plt.plot(range(1, 1+len(AVG_REWARDS)), AVG_REWARDS, label='Q learning')

    ALL_REWARDS = []
    for run in range(NUM_RUNS):
        _, rewards = forward_view_td_lambda(
            SIM, 0.1, 0.5, 0.1, 1, NUM_EPISODES)
        ALL_REWARDS.append(rewards)
    AVG_REWARDS = rolling_average(average_rewards(ALL_REWARDS), PERIOD)
    plt.plot(range(1, 1+len(AVG_REWARDS)), AVG_REWARDS, label='TD(0.5)')

    plt.xlabel('Num Episodes')
    plt.ylabel('Average Rewards')
    plt.legend()
    plt.show()
