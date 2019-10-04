"""
Script to run and save td lambda result
"""

import sys
from collections import defaultdict

from tqdm import trange

from achieve31 import (Simulator, forward_view_td_lambda,
                       run_k_step_td_q_value, save_q_val_function)

if __name__ == "__main__":

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    NUM_RUNS = int(sys.argv[1])

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    OVERALL_Q_FUNC = {'hit': defaultdict(
        lambda: 0), 'stick': defaultdict(lambda: 0)}

    for num_run in trange(NUM_RUNS):
        # print('Run ', num_run)
        q_func, _ = forward_view_td_lambda(SIM, 0.1, 0.5, 0.1, 1, 100000)

        for action in ['hit', 'stick']:
            for state in range(NUM_STATES):
                OVERALL_Q_FUNC[action][state] += q_func[action][state]

    for action in ['hit', 'stick']:
        for state in range(NUM_STATES):
            OVERALL_Q_FUNC[action][state] /= NUM_RUNS

    save_q_val_function('td_lambda_'+str(NUM_RUNS), OVERALL_Q_FUNC, NUM_STATES)
