import numpy as np
from loguru import logger


def liquidity_state(state_0):
    # UH = Ultra High, H = High, M = Medium, L = Low, UL = Ultra Low
    # states = ['UH', 'H', 'M', 'L', 'UL']
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
        logger.error("Transition matrix probabilities do not sum to 1.")
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


def bid_ask(liquidity, last):
    bid = last
    ask = last
    if liquidity == 'UH':
        spread = last * 0.0005
        bid = last - spread / 2
        ask = last + spread / 2
    if liquidity == 'H':
        spread = last * 0.001
        bid = last - spread / 2
        ask = last + spread / 2
    if liquidity == 'M':
        spread = last * 0.005
        bid = last - spread / 2
        ask = last + spread / 2
    if liquidity == 'L':
        spread = last * 0.01
        if np.random.normal(0, 1) >= 0.2:
            bid = last - spread / 2
        else:
            bid = None
        if np.random.normal(0, 1) >= 0.2:
            ask = last + spread / 2
        else:
            ask = None
    if liquidity == 'UL':
        spread = last * 0.0005
        if np.random.normal(0, 1) >= 0.7:
            bid = last - spread / 2
        else:
            bid = None
        if np.random.normal(0, 1) >= 0.7:
            ask = last + spread / 2
        else:
            ask = None
    return bid, ask
