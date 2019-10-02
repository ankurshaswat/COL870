"""
Code to compare performance according to part 2 of Q4
"""

import matplotlib.pyplot as plt

from achieve31 import (Simulator, average_rewards, k_step_lookahed_sarsa,
                       q_learning)

if __name__ == "__main__":
    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    for k in [1, 10, 100, 1000]:
        all_rewards = []
        for run in range(10):
            _, rewards = k_step_lookahed_sarsa(SIM, k, 0.1, 0.1, 1, 100)
            all_rewards.append(rewards)
        fin_rewards = average_rewards(all_rewards)

    for k in [1, 10, 100, 1000]:
        all_rewards = []
        for run in range(10):
            _, rewards = k_step_lookahed_sarsa(SIM, k, 0.1, 0.1, 1, 100, True)
            all_rewards.append(rewards)
        fin_rewards = average_rewards(all_rewards)

    all_rewards = []
    for run in range(10):
        _, rewards = q_learning(SIM, 0.1, 0.1, 1, 100)
        all_rewards.append(rewards)
    fin_rewards = average_rewards(all_rewards)

    plt.plot(fin_rewards)
    plt.show()
