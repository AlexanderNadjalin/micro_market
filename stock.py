import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from loguru import logger
import gbm, liquidity_states as ls


class Stock(object):
    def __init__(self, ticker: str, start_value: float, start_time: dt.datetime, liquidity: str):
        self.ticker = ticker
        self.start_value = start_value
        self.start_time = start_time
        self.bid = None
        self.ask = None
        self.last = start_value
        self.liquidity = liquidity
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
        if not isinstance(self.liquidity, str):
            logger.error('"liquidity" is not of type str. Aborted.')
            error = True
        if self.liquidity not in ['UH', 'H', 'M', 'L', 'UL']:
            logger.error('"liquidity" is not one of "UH", "H", "M", "L", "UL". Aborted.')
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

    def one_tick(self, alpha: float, theta: float, volatility: float, rate: float):
        tick_delta = gbm.gamma_dist(alpha, theta)
        self.tick_time = self.tick_time + tick_delta
        if self.volatility is None:
            self.volatility = volatility
        if self.rate is None:
            self.rate = rate
        self.last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
        self.push_to_history(self.ticker, self.tick_time, self.bid, self.ask, self.last, self.liquidity)

    def period_ticks(self, start_time: dt.datetime, end_time: dt.datetime,
                     alpha: float, theta: float, volatility: float, rate: float):
        timer = start_time
        counter = 0
        if self.volatility is None:
            self.volatility = volatility
        if self.rate is None:
            self.rate = rate
        while timer <= end_time:
            tick_delta = gbm.gamma_dist(alpha, theta)
            last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
            self.last = last
            self.liquidity = ls.liquidity_state(self.liquidity)
            self.bid, self.ask = ls.bid_ask(self.liquidity, self.last)
            self.push_to_history(self.ticker, timer, self.bid, self.ask, last, self.liquidity)
            timer += tick_delta
            counter += 1
        logger.info('Added ' + str(counter) + ' rows to ' + self.ticker + '.')

    def plot(self):
        plt.subplot(2, 1, 1)
        self.history.plot(x='time', y='last')
        self.history.plot(x='time', y='bid')
        self.history.plot(x='time', y='ask')
        plt.ylabel('Quotes')
        plt.xlabel('Time')
        plt.legend('best')
        plt.grid(True)
        plt.axis('tight')

        plt.subplot(2, 1, 2)

        return plt

    def __getattr__(self, item):
        """

        Map values to attributes.
        """
        value = self.__dict__.get(item)
        if not value:
            logger.error('"' + item + '" for Stock object "' + self.ticker + '" not found.')
            quit()
        else:
            return value
