import pandas as pd
import datetime as dt
from loguru import logger
import gbm


class Stock(object):
    def __init__(self, ticker: str, start_value: float):
        self.ticker = ticker
        self.start_value = start_value
        self.start_time = dt.datetime.now()
        self.bid = None
        self.ask = None
        self.last = start_value
        self.liquidity = None
        self.volatility = None
        self.rate = None
        self.tick_time = self.start_time
        self.history = pd.DataFrame()

        self._validate()

    def _validate(self):
        error = False
        if not isinstance(self.ticker, str):
            logger.error('"ticker" is not of type string. Aborted.')
            error = True
        if not isinstance(self.start_value, float):
            logger.error('"start_value" is not of type float. Aborted.')
            error = True
        if error:
            quit()
        else:
            cols = ['ticker', 'time', 'bid', 'ask', 'last', 'liquidity']
            self.history = pd.DataFrame(columns=cols)
            self.push_to_history(self.ticker, self.start_time, self.bid, self.ask, self.start_value, self.liquidity)

            logger.info('Created Stock object "' + self.ticker + '".')

    def push_to_history(self, ticker, time, bid, ask, last, liquidity):
        length = len(self.history.index)
        self.history.loc[length] = [ticker, time, bid, ask, last, liquidity]

    def one_tick(self, alpha: int, theta: int, volatility: float, rate: float):
        tick_delta = gbm.gamma_dist(alpha, theta)
        self.tick_time = self.tick_time + tick_delta
        if self.volatility is None:
            self.volatility = volatility
        if self.rate is None:
            self.rate = rate
        self.last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
        self.push_to_history(self.ticker, self.tick_time, self.bid, self.ask, self.last, self.liquidity)

    def period_ticks(self, start_time: dt.datetime, end_time: dt.datetime,
                     alpha: int, theta: int, volatility: float, rate: float):
        timer = start_time
        if self.volatility is None:
            self.volatility = volatility
        if self.rate is None:
            self.rate = rate
        while timer <= end_time:
            tick_delta = gbm.gamma_dist(alpha, theta)
            last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
            self.push_to_history(self.ticker, timer, self.bid, self.ask, last, self.liquidity)
            timer += tick_delta

    def __getattr__(self, item):
        """
        Map values to attributes.
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)
