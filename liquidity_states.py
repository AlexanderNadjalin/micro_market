import numpy as np


def liquidity_state(state_0):
    # UH = Ultra High, H = High, M = Medium, L = Low, UL = Ultra Low
    states = ['UH', 'H', 'M', 'L', 'UL']
    transition_name = [['UHUH', 'UHH', 'UHM', 'UHL', 'UHUL'],
                       ['HUH', 'HH', 'HM', 'HL', 'HUL'],
                       ['MUH', 'MH', 'MM', 'ML', 'MUL'],
                       ['LUH', 'LH', 'LM', 'LL', 'LUL'],
                       ['ULUH', 'ULH', 'ULM', 'ULL', 'ULUL']]
    transition_prob = [[0.97, 0.025, 0.005, 0, 0],
                       [0.0125, 0.97, 0.0125, 0.005, 0],
                       [0.0025, 0.0125, 0.97, 0.0125, 0.0025],
                       [0, 0.005, 0.0125, 0.97, 0.0125],
                       [0, 0, 0.005, 0.025, 0.97]]

    prob_sum = sum(transition_prob[0]) + sum(transition_prob[1]) + sum(transition_prob[2]) + \
               sum(transition_prob[3]) + sum(transition_prob[4])
    if prob_sum != 5:
        print("Transition matrix probabilities do not sum to 1.")
        quit()

    new_state = ''
    if state_0 == 'UH':
        new_state = np.random.choice(transition_name[0], replace=True, p=transition_prob[0])
        new_state = new_state[2:]
    if state_0 == 'H':
        new_state = np.random.choice(transition_name[1], replace=True, p=transition_prob[1])
        new_state = new_state[1:]
    if state_0 == 'M':
        new_state = np.random.choice(transition_name[2], replace=True, p=transition_prob[2])
        new_state = new_state[1:]
    if state_0 == 'L':
        new_state = np.random.choice(transition_name[3], replace=True, p=transition_prob[3])
        new_state = new_state[1:]
    if state_0 == 'UL':
        new_state = np.random.choice(transition_name[4], replace=True, p=transition_prob[4])
        new_state = new_state[2:]

    return new_state
