import numpy as np


def liquidity_state(state_orig):
    """

    Transition the liquidity state depending on the non changing original liquidity state.
    Non changing because otherwise a stock classed as "UH" could move and become "UL" which is
    not desirable (certain stocks are always liquid Apple etc.).

    :param state_orig: Stocks original liquidity state:
            UH = Ultra High. Always super tight bid ask spread.
            H = High. Always tight bid ask spread.
            M = Medium. Always bid ask spread.
            L = Low. Often bid and ask. Wider spread.
            UL = Ultra Low. Sometime bid and ask. Super wide spread.
    :return: New liquidity state.
    """
    new_state = ''
    if state_orig == 'UH':
        transition_name = ['UHUH', 'UHH', 'UHM', 'UHL', 'UHUL']
        transition_prob = [0.97, 0.025, 0.005, 0, 0]
        new_state = np.random.choice(transition_name, replace=True, p=transition_prob)
        new_state = new_state[2:]
    if state_orig == 'H':
        transition_name = ['HUH', 'HH', 'HM', 'HL', 'HUL']
        transition_prob = [0.0125, 0.97, 0.0125, 0.005, 0]
        new_state = np.random.choice(transition_name, replace=True, p=transition_prob)
        new_state = new_state[1:]
    if state_orig == 'M':
        transition_name = ['MUH', 'MH', 'MM', 'ML', 'MUL']
        transition_prob = [0.0025, 0.0125, 0.97, 0.0125, 0.0025]
        new_state = np.random.choice(transition_name, replace=True, p=transition_prob)
        new_state = new_state[1:]
    if state_orig == 'L':
        transition_name = ['LUH', 'LH', 'LM', 'LL', 'LUL']
        transition_prob = [0, 0.005, 0.0125, 0.97, 0.0125]
        new_state = np.random.choice(transition_name, replace=True, p=transition_prob)
        new_state = new_state[1:]
    if state_orig == 'UL':
        transition_name = ['ULUH', 'ULH', 'ULM', 'ULL', 'ULUL']
        transition_prob = [0, 0, 0.005, 0.025, 0.97]
        new_state = np.random.choice(transition_name, replace=True, p=transition_prob)
        new_state = new_state[2:]

    return new_state


def liquidity_score(liquidity: str) -> int:
    """

    Translate from liquidity state (text) to liquidity state (numerical).

    :param liquidity: Liquidity state (text).
    :return: Liquidity score (numerical).
    """
    score = {'UH': 5, 'H': 4, 'M': 3, 'L': 2, 'UL': 1}
    return score[liquidity]


def bid_ask(liquidity: str, last: float) -> (float, float):
    """

    Generate bid and ask from liquidity state.

    :param liquidity: Stocks original liquidity state:
            UH = Ultra High. Always super tight bid ask spread.
            H = High. Always tight bid ask spread.
            M = Medium. Always bid ask spread.
            L = Low. Often bid and ask. Wider spread.
            UL = Ultra Low. Sometime bid and ask. Super wide spread.
    :param last: Last price.
    :return: Bid and ask. One or both may be NULL.
    """
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
