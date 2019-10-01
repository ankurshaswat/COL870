"""
COL870 A1 Code
"""

import time
from collections import defaultdict
from random import choice, randint, random

from tqdm import trange


def print_card(player, sign, number):
    """
    Convert draws into proper prints for debugging
    """

    if player:
        if sign == '+':
            print("Player B"+str(number))
        else:
            print("Player R"+str(number))
    else:
        if sign == '+':
            print("Dealer B"+str(number))
        else:
            print("Dealer R"+str(number))


def score_state(state_obj):
    """
    Score state object
    """
    total = state_obj['total']
    trumps = state_obj['trump1'] + state_obj['trump2'] + state_obj['trump3']

    score = 0
    for num_trumps in range(trumps, -1, -1):
        score = total + num_trumps * 10
        if score <= 31:
            break

    return score


def generate_random_b_r():
    """
    Generate Random Card type
    """
    draw = choice(['+', '+', '-'])
    # draw = choices(['+', '-'], weights=[2/3, 1/3])[0]
    # draw = choice(['+', '-'], 1, p=[2/3, 1/3])
    return draw


def generate_random_number():
    """
    Generate Random Next Card Number
    """
    # draw = randint(low=1, high=11)
    draw = randint(1, 10)
    return draw


class Simulator():
    """
    Class to simulate Achieve31 Games
    """

    def __init__(self):
        self.initialize_enc_decoder()
        self.state = {}

    def initialize_enc_decoder(self):
        """
        Initialize Encoder and Decoder for state compression
        """

        state_num = 3
        self.encoder = {}
        # self.decoder = {}
        self.decode_score = {}

        for total in range(-30, 1+31):
            for dealer_card in range(1, 1+10):
                for t1_val in range(0, 2):
                    for t2_val in range(0, 2):
                        for t3_val in range(0, 2):

                            constructed_state = {
                                'total': total,
                                'trump1': t1_val,
                                'trump2': t2_val,
                                'trump3': t3_val,
                                'dealer_card': dealer_card,
                            }

                            player_score_loc = score_state(constructed_state)

                            if not 0 <= player_score_loc <= 31:
                                continue

                            self.encoder[frozenset(
                                constructed_state.items())] = state_num
                            # self.decoder[state_num] = constructed_state
                            self.decode_score[state_num] = player_score_loc

                            state_num += 1

        self.num_states = state_num

        print('total_states = ', state_num)

    def get_num_states(self):
        """
        Get total number of generated states
        """
        return self.num_states

    def encode(self, state, type_state=''):
        """
        Encode input state
        """

        if type_state == 'lose':
            return 0

        if type_state == 'win':
            return 1

        if type_state == 'draw':
            return 2

        return self.encoder[frozenset(state.items())]

    def get_state_score(self, state_num):
        """
        Decode State Score
        """
        if state_num in [0, 1, 2]:
            print("Don't Know what to do")
            return None

        return self.decode_score[state_num]
    # def decode(self, state_num):
    #     """
    #     Decode input state
    #     """

    #     if state_num == 0:
    #         return 'lose'

    #     if state_num == 1:
    #         return 'win'

    #     if state_num == 2:
    #         return 'draw'

    #     return self.decoder[state_num]

    def reset(self):
        """
        Reset State and start new game
        """

        self.state = {
            'total': 0,
            'trump1': 0,
            'trump2': 0,
            'trump3': 0,
            'dealer_card': 0,
        }

        card_num = generate_random_number()

        self.state['total'] = card_num
        if card_num in [1, 2, 3]:
            self.state['trump'+str(card_num)] = 1

        # print_card(True, '+', card_num)

        card_num = generate_random_number()

        self.state['dealer_card'] = card_num

        # print_card(False, '+', card_num)
        return self.encode(self.state)

    def step(self, action_taken):
        """
        Take next step according to action
        """

        if action_taken == 'hit':
            card_sign = generate_random_b_r()
            card_num = generate_random_number()

            if card_sign == '+':
                self.state['total'] += card_num
                if card_num in [1, 2, 3]:
                    self.state['trump'+str(card_num)] = 1
            else:
                self.state['total'] -= card_num

            score = score_state(self.state)

            if not 0 <= score <= 31:
                return self.encode(self.state, 'lose'), -1, True

            if 0 <= score <= 31:
                return self.encode(self.state), 0, False

            # print_card(True, card_sign, card_num)

        # Action = 'Stick'

        dealer_card = self.state['dealer_card']

        dealer_state = {
            'total': dealer_card,
            'trump1': 0,
            'trump2': 0,
            'trump3': 0
        }

        if dealer_card in [1, 2, 3]:
            dealer_state['trump'+str(dealer_card)] = 1

        score = score_state(self.state)
        dealer_score = score_state(dealer_state)

        while 0 <= dealer_score <= 24:
            card_sign = generate_random_b_r()
            card_num = generate_random_number()

            if card_sign == '+':
                dealer_state['total'] += card_num
                if card_num in [1, 2, 3]:
                    dealer_state['trump'+str(card_num)] = 1
            else:
                dealer_state['total'] -= card_num

            # print_card(False, card_sign, card_num)

            dealer_score = score_state(dealer_state)

            # print('Projected Scores', player_score, dealer_score)

        if (not 0 <= dealer_score <= 31) or (dealer_score < score):
            return self.encode(self.state, 'win'), 1, True

        if dealer_score > score:
            return self.encode(self.state, 'lose'), -1, True

        if dealer_score == score:
            return self.encode(self.state, 'draw'), 0, True


def generate_episode_q_value(simulator):
    """
    Generate episodes according to simple policy in state action tuples
    """
    state = simulator.reset()
    done = False
    state_action_pairs = []
    rewards = []

    while not done:
        # decoded_state = simulator.decode(state)
        player_score = simulator.get_state_score(state)

        if player_score < 25:
            action = 'hit'
        else:
            action = 'stick'

        state_action_pairs.append((state, action))

        state, reward, done = simulator.step(action)

        rewards.append(reward)

    return state_action_pairs, rewards


def average(lst):
    """
    Find average of elements of list
    """
    return sum(lst) / len(lst)


def run_mc_q_value(simulator, gamma, visit_type, num_episodes):
    """
    Run Monte Carlo method for finding Q values
    """
    q_val = {'hit': defaultdict(lambda: 0), 'stick': defaultdict(lambda: 0)}
    returns = {'hit': defaultdict(
        lambda: []), 'stick': defaultdict(lambda: [])}

    for _ in trange(num_episodes):
        state_action_pairs, reward = generate_episode_q_value(simulator)
        g_val = 0
        for ind, state_action in reversed(list(enumerate(state_action_pairs))):
            g_val = reward[ind] + gamma * g_val
            if visit_type == 'every' or (state_action not in state_action_pairs[:ind-1]):

                returns[state_action[1]][state_action[0]].append(g_val)
                q_val[state_action[1]][state_action[0]] = average(
                    returns[state_action[1]][state_action[0]])

    return q_val


def run_k_step_td_q_value(simulator, k, alpha, gamma):
    """
    Run k step TD method for finding Q values
    """
    q_val = {'hit': defaultdict(lambda: 0), 'stick': defaultdict(lambda: 0)}

    for _ in range(10000):

        state = simulator.reset()

        t_terminal = 1000000000
        t_apparent = -1
        t_actual = 0
        done = False

        # decoded_state = simulator.decode(state)
        player_score = simulator.get_state_score(state)

        if player_score < 25:
            action = 'hit'
        else:
            action = 'stick'

        states = [state]
        actions = [action]
        rewards = []

        while not done or t_apparent < t_terminal - 1:
            if t_actual < t_terminal:

                state, reward, done = simulator.step(action)
                states.append(state)
                rewards.append(reward)
                if done:
                    t_terminal = t_actual + 1
                else:
                    t_terminal += 1
                    # decoded_state = simulator.decode(state)
                    player_score = simulator.get_state_score(state)

                    if player_score < 25:
                        action = 'hit'
                    else:
                        action = 'stick'

                    actions.append(action)

            t_apparent = t_actual - k + 1

            if t_apparent >= 0:

                g_value = 0
                for i in range(t_apparent+1, 1+min(t_apparent+k, t_terminal)):
                    g_value += (gamma ** (i-t_apparent-1)) * rewards[i-1]

                if t_apparent + k < t_terminal:
                    temp_state = states[t_apparent+k]
                    temp_action = actions[t_apparent+k]
                    g_value += (gamma ** k) * \
                        q_val[temp_action][temp_state]

                temp_state = states[t_apparent]
                temp_action = actions[t_apparent]
                old_q = q_val[temp_action][temp_state]
                q_val[temp_action][temp_state] = old_q + \
                    alpha * (g_value - old_q)

            t_actual += 1
    return q_val


def k_step_lookahed_sarsa(simulator, k, alpha, epsilon, gamma, num_epis):
    """
    Simulate k step lookahead SARSA
    """
    q_val = {'hit': defaultdict(lambda: 0), 'stick': defaultdict(lambda: 0)}
    greedy_pi = defaultdict(lambda: 'hit')

    all_final_rewards = []

    for _ in trange(num_epis):
        state = simulator.reset()

        greedy_action = greedy_pi[state]

        action = greedy_action
        if random() < epsilon:
            action = choice(['hit', 'stick'])

        t_terminal = 1000000000
        t_apparent = -1
        t_actual = 0
        done = False

        states = [state]
        actions = [action]
        rewards = []

        while not done or t_apparent < t_terminal - 1:
            if t_actual < t_terminal:

                state, reward, done = simulator.step(action)
                states.append(state)
                rewards.append(reward)
                if done:
                    all_final_rewards.append(reward)
                    t_terminal = t_actual + 1
                else:
                    t_terminal += 1
                    # decoded_state = simulator.decode(state)
                    greedy_action = greedy_pi[state]

                    action = greedy_action
                    if random() < epsilon:
                        action = choice(['hit', 'stick'])

                    actions.append(action)

            t_apparent = t_actual - k + 1

            if t_apparent >= 0:

                g_value = 0
                for i in range(t_apparent+1, 1+min(t_apparent+k, t_terminal)):
                    g_value += (gamma ** (i-t_apparent-1)) * rewards[i-1]

                if t_apparent + k < t_terminal:
                    temp_state = states[t_apparent+k]
                    temp_action = actions[t_apparent+k]
                    g_value += (gamma ** k) * \
                        q_val[temp_action][temp_state]

                temp_state = states[t_apparent]
                temp_action = actions[t_apparent]
                old_q = q_val[temp_action][temp_state]
                q_val[temp_action][temp_state] = old_q + \
                    alpha * (g_value - old_q)

                state_score = simulator.get_state_score(temp_state)

                hit_val = q_val['hit'][temp_state]
                stick_val = q_val['stick'][temp_state]

                if stick_val > hit_val or state_score == 31:
                    greedy_pi[temp_state] = 'stick'
                else:
                    greedy_pi[temp_state] = 'hit'

            t_actual += 1

    return greedy_pi, all_final_rewards


def save_q_val_function(name, q_func, num_states):
    """
    Function to save q value function obtained after much calculation
    """
    with open('saves/'+name+'_'+str(int(time.time())), 'w') as file:
        for action in ['hit', 'stick']:
            file.write(action+'\n')
            for state_num in trange(num_states):
                file.write(str(state_num)+' ' +
                           str(q_func[action][state_num])+'\n')


def average_rewards(arr_rewards):
    """
    Average list of rewards
    """
    avg_rewards = []
    for i in range(len(arr_rewards[0])):
        avg_rewards.append(0)
        for _, rewards in enumerate(arr_rewards):
            avg_rewards[i] += rewards[i]
        avg_rewards[i] /= len(arr_rewards)

    return avg_rewards