import numpy as np
import datetime as dt
import math


def gamma_dist(alpha: float, beta: float) -> dt.timedelta:
    """

    Generate a random timedelta in seconds from a gamma distribution.
    https://en.wikipedia.org/wiki/Gamma_distribution.

    :param alpha: Alpha parameter.
    :param beta: Beta parameter.
    :return: Timedelta in seconds.
    """
    delta = np.random.gamma(alpha, beta)
    time_delta = dt.timedelta(seconds=delta)
    return time_delta


def random_price(time: dt.timedelta, last_s: float, r: float, vol: float):
    """

    Generate a random price from a Geometric Brownian Motion.
    https://en.wikipedia.org/wiki/Geometric_Brownian_motion.

    :param time: Timedelta, the amount of time in seconds for the GBM.
    :param last_s: Last price.
    :param r: Interest rate (yearly, decimal form).
    :param vol: Stock volatility (yearly, decimal form).
    :return: New last price.
    """
    delta_t = time.total_seconds() / (365 * 24)
    vol = vol / math.sqrt(252)
    rnd = last_s * np.exp((r - 0.5 * vol ** 2) * delta_t + vol * np.random.normal(0, 1) * math.sqrt(delta_t))
    return rnd
