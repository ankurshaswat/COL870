"""
Code to compare performance according to part 3 of Q4
"""
import matplotlib.pyplot as plt

from achieve31 import (Simulator, k_step_lookahed_sarsa, q_learning,
                       test_policy, test_q_func)

if __name__ == "__main__":
    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for k in [1, 10, 100, 1000]:
        x = []
        y = []
        for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
            greedy_pi, _ = k_step_lookahed_sarsa(
                SIM, k, alpha, 0.1, 1, 100000)
            rew = test_policy(SIM, greedy_pi, 10)
            print('K step lookahead SARSA: k={} alpha={} Reward={}'.format(
                k, alpha, rew))
            y.append(rew)
            x.append(alpha)
        # ax.scatter(x, y, label="k step lookahead SARSA "+str(k))
        ax.plot(x, y, marker='o', label="k step lookahead SARSA "+str(k))
    plt.legend()

    plt.show()
    for k in [1, 10, 100, 1000]:
        for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
            greedy_pi, _ = k_step_lookahed_sarsa(
                SIM, k, alpha, 0.1, 1, 100000, True)
            rew = test_policy(SIM, greedy_pi, 10)
            print('K step lookahead SARSA with Decay: k={} alpha={} Reward={}'.format(
                k, alpha, rew))

    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
        q_func, _ = q_learning(SIM, alpha, 0.1, 1, 100000)
        rew = test_q_func(SIM, q_func, 10)
        print('Q Learning: alpha={} Reward={}'.format(alpha, rew))
