from numpy.random import choice, randint


class Simulator():
    def __init__(self):
        self.initialize_enc_decoder()
        self.reset()

    def initialize_enc_decoder(self):
        state_num = 3
        self.encoder = {}
        self.decoder = {}

        for s1 in range(-30, 32):
            for s2 in range(-30, 32):
                for p_t1 in range(0, 2):
                    for p_t2 in range(0, 2):
                        for p_t3 in range(0, 2):
                            for d_t1 in range(0, 2):
                                for d_t2 in range(0, 2):
                                    for d_t3 in range(0, 2):
                                        constructed_state = {
                                            'player_total': s1,
                                            'player_trump1': p_t1,
                                            'player_trump2': p_t2,
                                            'player_trump3': p_t3,
                                            'dealer_total': s2,
                                            'dealer_trump1': d_t1,
                                            'dealer_trump2': d_t2,
                                            'dealer_trump3': d_t3,
                                        }
                                        player_score, dealer_score = self.score_state(
                                            constructed_state)

                                        if not (player_score >= 0 and player_score <= 31 and dealer_score >= 0 and dealer_score <= 31):
                                            continue

                                        self.encoder[frozenset(
                                            constructed_state.items())] = state_num
                                        self.decoder[state_num] = constructed_state
                                        state_num += 1

        print('total_states = ', state_num)

    def encode(self, type):
        if (type == 'bust'):
            return 0
        elif (type == 'win'):
            return 1
        elif (type == 'lose'):
            return 2
        else:
            return self.encoder[frozenset(self.state.items())]

    def decode(self,state_num):
        if(state_num == 0):
            return 'bust'
        elif state_num == 1:
            return 'win'
        elif state_num == 2:
            return 'lose'
        else:
            return self.decoder[state_num]

    def score_state(self, state_to_score):
        player_total = state_to_score['player_total']
        player_trumps = state_to_score['player_trump1'] + \
            state_to_score['player_trump2'] + state_to_score['player_trump3']

        player_score = 0
        for i in range(player_trumps, -1, -1):
            player_score = player_total + i * 10
            if(player_score <= 31):
                break

        dealer_total = state_to_score['dealer_total']
        dealer_trumps = state_to_score['dealer_trump1'] + \
            state_to_score['dealer_trump2'] + state_to_score['dealer_trump3']

        dealer_score = 0
        for i in range(dealer_trumps, -1, -1):
            dealer_score = dealer_total + i * 10
            if(dealer_score <= 31):
                break

        return player_score, dealer_score

    def generate_random_b_r(self):
        draw = choice(['+', '-'], 1, p=[2/3, 1/3])
        return draw

    def generate_random_number(self):
        draw = randint(low=1, high=10)
        return draw

    def check_and_return_next_state(self,state):
        player_score, dealer_score = self.score_state(state)

        if player_score < 0 or player_score > 31:
            return self.encode('bust'), True
        elif dealer_score < 0 or dealer_score > 31:
            return self.encode('win'), True
        else:
            return self.encode(''), False

    def reset(self):
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

        card_sign = self.generate_random_b_r()
        card_num = self.generate_random_number()

        if(card_sign == '+'):
            self.state['player_total'] = card_num
            if(card_num == 1):
                self.state['player_trump1'] = 1
            elif (card_num == 2):
                self.state['player_trump2'] = 1
            elif (card_num == 3):
                self.state['player_trump3'] = 1
        else:
            self.state['player_total'] = -1 * card_num

        card_sign = self.generate_random_b_r()
        card_num = self.generate_random_number()

        if(card_sign == '+'):
            self.state['dealer_total'] = card_num
            if(card_num == 1):
                self.state['dealer_trump1'] = 1
            elif (card_num == 2):
                self.state['dealer_trump2'] = 1
            elif (card_num == 3):
                self.state['dealer_trump3'] = 1
        else:
            self.state['dealer_total'] = -1 * card_num

        init_state, _ = self.check_and_return_next_state(self.state)
        return init_state

    def step(self, action):
        reward = 0
        done = False

        if action == 'hit':
            card_sign = self.generate_random_b_r()
            card_num = self.generate_random_number()

            if(card_sign == '+'):
                self.state['player_total'] += card_num
                if(card_num == 1):
                    self.state['player_trump1'] = 1
                elif (card_num == 2):
                    self.state['player_trump2'] = 1
                elif (card_num == 3):
                    self.state['player_trump3'] = 1
            else:
                self.state['player_total'] -= card_num

            next_state , done = self.check_and_return_next_state(self.state)

        else:
            while True:
                card_sign = self.generate_random_b_r()
                card_num = self.generate_random_number()

                if(card_sign == '+'):
                    self.state['dealer_total'] = card_num
                    if(card_num == 1):
                        self.state['dealer_trump1'] = 1
                    elif (card_num == 2):
                        self.state['dealer_trump2'] = 1
                    elif (card_num == 3):
                        self.state['dealer_trump3'] = 1
                else:
                    self.state['dealer_total'] = -1 * card_num

                _, dealer_score = self.score_state(self.state)

                if(dealer_score < 0 or dealer_score >= 25):
                    break
            # Complete dealer action sequencess
            done = 1
        return next_state, reward, done


sim = Simulator()
init_state = sim.reset()
print(sim.decode(init_state))
done = False
while not done:
    next_state, reward, done = sim.step('hit')
    print(sim.decode(next_state), reward, done)
