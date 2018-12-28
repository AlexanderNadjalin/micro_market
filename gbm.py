import numpy as np
import datetime as dt
import math


def gamma_dist(alpha, theta):
    delta = np.random.gamma(alpha, theta)
    time_delta = dt.timedelta(seconds=delta)
    return time_delta


def random_price(time, last_s, r, vol):
    dt = time.total_seconds() / (365 * 24)
    vol = vol / math.sqrt(252)
    rnd = last_s * np.exp((r - 0.5 * vol ** 2) * dt + vol * np.random.normal(0, 1) * math.sqrt(dt))
    return rnd
