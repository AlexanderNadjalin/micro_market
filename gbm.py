import numpy as np
import datetime as dt
import math


def gamma_dist(alpha, theta):
    delta = np.random.gamma(alpha, theta)
    time_delta = dt.timedelta(seconds=delta)
    return time_delta


def random_price(time, last_s, r, vol):
    dt_sec = time.total_seconds()
    vol_per_second = vol / math.sqrt(252 * 24 * 60 * 60)
    vol_per_dt = vol_per_second * dt_sec
    rnd = last_s * np.exp((r - vol_per_dt ** 2 / 2) * dt_sec + vol_per_dt * np.random.normal(0, 1) * math.sqrt(dt_sec))
    return rnd
