"""
COL870 A1 Code
"""

from collections import defaultdict

from numpy.random import choice, randint


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
    draw = choice(['+', '-'], 1, p=[2/3, 1/3])
    return draw


def generate_random_number():
    """
    Generate Random Next Card Number
    """
    draw = randint(low=1, high=11)
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
        self.decoder = {}

        for total in range(-30, 32):
            for dealer_card in range(1, 11):
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
                            self.decoder[state_num] = constructed_state
                            state_num += 1

        print('total_states = ', state_num)

    def encode(self, type_state=''):
        """
        Encode input state
        """

        if type_state == 'lose':
            return 0

        if type_state == 'win':
            return 1

        if type_state == 'draw':
            return 2

        return self.encoder[frozenset(self.state.items())]

    def decode(self, state_num):
        """
        Decode input state
        """

        if state_num == 0:
            return 'lose'

        if state_num == 1:
            return 'win'

        if state_num == 2:
            return 'draw'

        return self.decoder[state_num]

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
                return self.encode('lose'), -1, True

            return self.encode(), 0, False

            # print_card(True, card_sign, card_num)

        ## Action = 'Stick'

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

        while 0 <= dealer_score < 24:
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
            return self.encode('win'), 1, True

        if dealer_score > score:
            return self.encode('lose'), -1, True

        if dealer_score == score:
            return self.encode('draw'), 0, True


def generate_episode_q_value(simulator):
    """
    Generate episodes according to simple policy in state action tuples
    """
    state = simulator.reset()
    done = False
    state_action_pairs = []
    rewards = []

    while not done:
        decoded_state = simulator.decode(state)
        player_score = score_state(decoded_state)

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


def run_mc_q_value(simulator, gamma, visit_type):
    """
    Run Monte Carlo method for finding Q values
    """
    q_val = {'hit': defaultdict(lambda: 0), 'stick': defaultdict(lambda: 0)}
    returns = {'hit': defaultdict(
        lambda: []), 'stick': defaultdict(lambda: [])}

    for _ in range(10000):
        state_action_pairs, reward = generate_episode_q_value(simulator)
        g_val = 0
        for ind, state_action in enumerate(state_action_pairs):
            g_val = reward[ind] + gamma * g_val

            if visit_type == 'every' or (state_action not in state_action_pairs[:ind-1]):
                returns[state_action[1]][state_action[0]].append(g_val)
                q_val[state_action[1]][state_action[0]] = average(
                    returns[state_action[1]][state_action[0]])

    return q_val


if __name__ == "__main__":
    SIM = Simulator()
    Q_FUNCTION = run_mc_q_value(SIM, 0, 'first')
    print(Q_FUNCTION)
