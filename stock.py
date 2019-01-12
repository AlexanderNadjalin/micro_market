import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from loguru import logger
import gbm
import liquidity_states as ls


class Stock(object):
    def __init__(self, ticker: str, start_value: float, start_time: dt.datetime,
                 liquidity_orig: str):
        """

        Initialises the Stock object for simulation.

        :param ticker: The ticker name.
        :param start_value: Initial last price.
        :param start_time: String time of the simulation.
        :param liquidity_orig: Liquidity class:
            UH = Ultra High. Always super tight bid ask spread.
            H = High. Always tight bid ask spread.
            M = Medium. Always bid ask spread.
            L = Low. Often bid and ask. Wider spread.
            UL = Ultra Low. Sometime bid and ask. Super wide spread.
        """
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
        """

        Validate the Stock object. Errors logged and then aborted.

        :return: None.
        """
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
        """

        Save a tick to self.history as a DataFrame.

        :param ticker: Name of ticker.
        :param time: Timestamp of data point.
        :param bid: Bid value.
        :param ask: Ask value.
        :param last: Last value.
        :param liquidity: Current liquidity level as text.
        :param liquidity_score: Current liquidity level as number.
        :return: None.
        """
        length = len(self.history.index)
        self.history.loc[length] = [ticker, time, bid, ask, last, liquidity, liquidity_score]

    def period_ticks(self, start_time: dt.datetime, end_time: dt.datetime,
                     alpha: float, beta: float, volatility: float, rate: float):
        """

        Generate random tick values between two timestamps and save in self.history.

        :param start_time: Starting timestamp.
        :param end_time: Ending timestamp.
        :param alpha: Alpha parameter for gamma distribution.
        :param beta: Beta parameter for gamma distribution.
        :param volatility: Stock volatility (yearly, decimal form).
        :param rate: Interest rate (yearly, decimal form).
        :return: None.
        """
        timer = start_time
        counter = 0
        if self.volatility is None:
            self.volatility = volatility
        if self.rate is None:
            self.rate = rate
        while timer <= end_time:
            tick_delta = gbm.gamma_dist(alpha, beta)
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

    def plot_bid_ask_liq(self) -> plt.plot:
        """

        Create plots of bid/ask and liquidity score from self.history.

        :return: Plot obect.
        """
        df = self.history
        df.set_index(df['time'], inplace=True)
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex='all', sharey='none')

        df.plot(x='time', y='bid', ax=ax1, color='blue', linewidth=1)
        df.plot(x='time', y='ask', ax=ax1, color='red', linewidth=1)
        ax1.set(ylabel='Price')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M:%S"))

        ax1.legend(loc='lower center', ncol=2, fontsize=8)

        df.plot(x='time', y='liquidity_score', ax=ax2, color='black', linewidth=0.8, legend=None, rot=90, fontsize=7)
        ax2.set(ylabel='Liquidity Score')
        ax2.set_yticks([1, 2, 3, 4, 5])
        ax2.set_xticks([])

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
