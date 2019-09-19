"""
COL870 A1 Code
"""

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


def score_state(state_to_score):
    """
    Score states for player and dealer
    """
    player_total = state_to_score['player_total']
    player_trumps = state_to_score['player_trump1'] + \
        state_to_score['player_trump2'] + state_to_score['player_trump3']

    player_score = 0
    for i in range(player_trumps, -1, -1):
        player_score = player_total + i * 10
        if player_score <= 31:
            break

    dealer_total = state_to_score['dealer_total']
    dealer_trumps = state_to_score['dealer_trump1'] + \
        state_to_score['dealer_trump2'] + state_to_score['dealer_trump3']

    dealer_score = 0
    for i in range(dealer_trumps, -1, -1):
        dealer_score = dealer_total + i * 10
        if dealer_score <= 31:
            break

    return player_score, dealer_score


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

        for player_total in range(-30, 32):
            for dealer_total in range(-30, 32):
                for p_t1 in range(0, 2):
                    for p_t2 in range(0, 2):
                        for p_t3 in range(0, 2):
                            for d_t1 in range(0, 2):
                                for d_t2 in range(0, 2):
                                    for d_t3 in range(0, 2):
                                        constructed_state = {
                                            'player_total': player_total,
                                            'player_trump1': p_t1,
                                            'player_trump2': p_t2,
                                            'player_trump3': p_t3,
                                            'dealer_total': dealer_total,
                                            'dealer_trump1': d_t1,
                                            'dealer_trump2': d_t2,
                                            'dealer_trump3': d_t3,
                                        }
                                        player_score, dealer_score = score_state(
                                            constructed_state)

                                        if not (0 <= player_score <= 31 and 0 <= dealer_score <= 31):
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

    def check_and_return_next_state(self, state, end_game=False):
        """
        Check the scores and continue game if possible
        """
        player_score, dealer_score = score_state(state)

        done = False

        if (player_score < 0 or player_score > 31) and (dealer_score < 0 or dealer_score > 31):
            next_state, reward, done = self.encode('draw'), 0, True

        if player_score < 0 or player_score > 31:
            next_state, reward, done = self.encode('lose'), -1, True

        if dealer_score < 0 or dealer_score > 31:
            next_state, reward, done = self.encode('win'), 1, True

        if end_game and not done:
            if player_score > dealer_score:
                next_state, reward, done = self.encode('win'), 1, True

            if player_score == dealer_score:
                next_state, reward, done = self.encode('draw'), 0, True

            if player_score < dealer_score:
                next_state, reward, done = self.encode('lose'), -1, True

        if not done:
            next_state, reward, done = self.encode(), 0, False

        return next_state, reward, done

    def reset(self):
        """
        Reset State and start new game
        """
        self.state = {
            'player_total': 0,
            'player_trump1': 0,
            'player_trump2': 0,
            'player_trump3': 0,
            'dealer_total': 0,
            'dealer_trump1': 0,
            'dealer_trump2': 0,
            'dealer_trump3': 0,
        }

        card_num = generate_random_number()

        self.state['player_total'] = card_num
        if card_num == 1:
            self.state['player_trump1'] = 1
        elif card_num == 2:
            self.state['player_trump2'] = 1
        elif card_num == 3:
            self.state['player_trump3'] = 1

        # print_card(True, '+', card_num)

        card_num = generate_random_number()

        self.state['dealer_total'] = card_num
        if card_num == 1:
            self.state['dealer_trump1'] = 1
        elif card_num == 2:
            self.state['dealer_trump2'] = 1
        elif card_num == 3:
            self.state['dealer_trump3'] = 1

        # print_card(False, '+', card_num)

        init_state_loc, _, _ = self.check_and_return_next_state(self.state)
        return init_state_loc

    def step(self, action):
        """
        Take next step according to action
        """
        if action == 'hit':
            card_sign = generate_random_b_r()
            card_num = generate_random_number()

            if card_sign == '+':
                self.state['player_total'] += card_num
                if card_num == 1:
                    self.state['player_trump1'] = 1
                elif card_num == 2:
                    self.state['player_trump2'] = 1
                elif card_num == 3:
                    self.state['player_trump3'] = 1
            else:
                self.state['player_total'] -= card_num

            # print_card(True, card_sign, card_num)

        else:
            while True:
                card_sign = generate_random_b_r()
                card_num = generate_random_number()

                if card_sign == '+':
                    self.state['dealer_total'] += card_num
                    if card_num == 1:
                        self.state['dealer_trump1'] = 1
                    elif card_num == 2:
                        self.state['dealer_trump2'] = 1
                    elif card_num == 3:
                        self.state['dealer_trump3'] = 1
                else:
                    self.state['dealer_total'] -= card_num

                # print_card(False, card_sign, card_num)

                player_score, dealer_score = score_state(self.state)

                # print('Projected Scores', player_score, dealer_score)

                if(dealer_score < 0 or dealer_score > 31) or dealer_score >= 25:
                    break

        next_state, reward, done = self.check_and_return_next_state(
            self.state, action != 'hit')

        return next_state, reward, done


episodes = []
SIM = Simulator()

for i in range(10):
    episode = []

    INIT_STATE = SIM.reset()
    episode.append(INIT_STATE)
    DECODED_STATE = SIM.decode(INIT_STATE)
    # print(DECODED_STATE)
    # print('Projected Scores', score_state(DECODED_STATE))
    DONE = False
    ACTION = 'none'
    while not DONE:
        PLAYER_SCORE, _ = score_state(DECODED_STATE)

        if PLAYER_SCORE < 25:
            ACTION = 'hit'
            NEXT_STATE, REWARD, DONE = SIM.step('hit')
        else:
            ACTION = 'stick'
            NEXT_STATE, REWARD, DONE = SIM.step('stick')
        DECODED_STATE = SIM.decode(NEXT_STATE)
        episode.append(ACTION)
        episode.append(REWARD)
        episode.append(NEXT_STATE)
        # print(DECODED_STATE, REWARD, DONE)
        # if not DONE:
        # print('Projected Scores', score_state(DECODED_STATE))
    print((len(episode)-1) / 3)
    episodes.append(episode)

print(episodes)
