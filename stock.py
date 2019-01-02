import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from loguru import logger
import gbm
import liquidity_states as ls


class Stock(object):
    def __init__(self, ticker: str, start_value: float, start_time: dt.datetime,
                 liquidity_orig: str):
        self.ticker = ticker
        self.start_value = start_value
        self.start_time = start_time
        self.last = start_value
        self.liquidity_orig = liquidity_orig
        self.liquidity_score = None
        self.bid, self.ask = ls.bid_ask(liquidity_orig, self.last)
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
        if not isinstance(self.liquidity_orig, str):
            logger.error('"liquidity_orig" is not of type str. Aborted.')
            error = True
        if self.liquidity_orig not in ['UH', 'H', 'M', 'L', 'UL']:
            logger.error('"liquidity_orig" is not one of "UH", "H", "M", "L", "UL". Aborted.')
            error = True
        if error:
            quit()
        else:
            cols = ['ticker', 'time', 'bid', 'ask', 'last', 'liquidity_orig', 'liquidity_score']
            self.history = pd.DataFrame(columns=cols)
            self.liquidity_score = ls.liquidity_score(self.liquidity_orig)
            self.push_to_history(self.ticker, self.start_time, self.bid, self.ask, self.start_value,
                                 self.liquidity_orig, self.liquidity_score)

            logger.info('Created Stock object "' + self.ticker + '".')

    def push_to_history(self, ticker, time, bid, ask, last, liquidity, liquidity_score):
        length = len(self.history.index)
        self.history.loc[length] = [ticker, time, bid, ask, last, liquidity, liquidity_score]

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
            timer += tick_delta
            last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
            self.last = last
            liquidity_state = ls.liquidity_state(self.liquidity_orig)
            self.liquidity_score = ls.liquidity_score(liquidity_state)
            self.bid, self.ask = ls.bid_ask(liquidity_state, self.last)
            self.push_to_history(self.ticker, timer, self.bid, self.ask, last,
                                 self.liquidity_orig, self.liquidity_score)
            counter += 1
        logger.info('Added ' + str(counter) + ' rows to ' + self.ticker + '.')

    def plot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex='all', sharey='none')

        self.history.plot(x='time', y='bid', ax=ax1, color='blue', linewidth=1)
        self.history.plot(x='time', y='ask', ax=ax1, color='red', linewidth=1)
        ax1.set(ylabel='Price')
        ax1.legend(loc='lower center', ncol=2, fontsize=8)

        self.history.plot(x='time', y='liquidity_score', ax=ax2, color='black', linewidth=1, legend=None)
        ax2.set(ylabel='Liquidity Score')
        ax2.set_yticks([1, 2, 3, 4, 5])

        plt.xlabel('Time')

        plt.savefig(self.ticker + '.png')

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
