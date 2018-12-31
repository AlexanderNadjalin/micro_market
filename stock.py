import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
from loguru import logger
import gbm, liquidity_states as ls


class Stock(object):
    def __init__(self, ticker: str, start_value: float, start_time: dt.datetime,
                 liquidity_orig: str):
        self.ticker = ticker
        self.start_value = start_value
        self.start_time = start_time
        self.bid = None
        self.ask = None
        self.last = start_value
        self.liquidity_orig = liquidity_orig
        self.liquidity_score = None
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
            last = gbm.random_price(tick_delta, self.last, self.rate, self.volatility)
            self.last = last
            liquidity_state = ls.liquidity_state(self.liquidity_orig)
            self.liquidity_score = ls.liquidity_score(liquidity_state)
            self.bid, self.ask = ls.bid_ask(liquidity_state, self.last)
            self.push_to_history(self.ticker, timer, self.bid, self.ask, last,
                                 self.liquidity_orig, self.liquidity_score)
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

    def dataframe_plot(self) -> None:
        """
        Plot a plotly time series plot from a pd.DataFrame.
        Save a html-file.

        :return: None.
        """
        file_name = self.ticker + '.html'

        trace_last = go.Scatter(x=self.history['time'],
                                y=self.history['last'],
                                mode='lines',
                                name='Last',
                                marker=dict(
                                    size=6,
                                    color='rgb(181, 32, 160)',
                                    line={'width': 0.5}
                                ))

        trace_ask = go.Scatter(x=self.history['time'],
                               y=self.history['ask'],
                               mode='lines',
                               name='Ask',
                               marker=dict(
                                   size=6,
                                   color='rgb(44, 169, 247)',
                                   symbol='pentagon',
                                   line={'width': 0.5}
                               ))

        trace_bid = go.Scatter(x=self.history['time'],
                               y=self.history['bid'],
                               mode='lines',
                               name='Bid',
                               opacity=0.85,
                               marker=dict(
                                   size=6,
                                   color='rgb(44, 169, 247)',
                                   symbol='pentagon',
                                   line={'width': 0.5}
                               ))

        trace_liq = go.Bar(x=self.history['time'],
                           y=self.history['liquidity_score'], yaxis='y2',
                           name='Liquidity Score',
                           marker=dict(
                               color='rgba(55, 128, 191, 0.7)',
                               line=dict(
                                   color='rgba(55, 128, 191, 1.0)')
                               ), opacity=0.5)

        # data = [trace_last, trace_ask, trace_bid, trace_liq]
        # layout = go.Layout(title=self.ticker, yaxis=dict(title='Last'),
        #                    yaxis2=dict(title='Liquidity score',
        #                    overlaying='y', side='right'))

        fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=False, vertical_spacing=0.1)
        fig.append_trace(trace_last, 1, 1)
        fig.append_trace(trace_bid, 1, 1)
        fig.append_trace(trace_ask, 1, 1)
        fig.append_trace(trace_liq, 2, 1)
        fig['layout'].update(height=600, width=900, title=self.ticker, bargap=0)
        # fig = go.Figure(data=data, layout=layout)

        try:
            pyo.plot(fig, filename=file_name)
            logger.info('Line plot created. File name: "' + file_name + '".')
        except Exception as e:
            logger.critical('Line plot creation failed. Exception: "' + str(e) + '".')

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
