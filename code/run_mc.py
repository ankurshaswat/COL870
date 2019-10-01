"""
Script to run and save mc result
"""
import sys

from achieve31 import Simulator, run_mc_q_value, save_q_val_function

if __name__ == "__main__":

    TYPE = sys.argv[1]
    NUM_EPISODES = int(sys.argv[2])

    SIM = Simulator()
    NUM_STATES = SIM.get_num_states()

    Q_FUNCTION = run_mc_q_value(SIM, 1, TYPE, NUM_EPISODES)

    save_q_val_function('mc_'+TYPE+'_'+str(NUM_EPISODES),
                        Q_FUNCTION, NUM_STATES)
