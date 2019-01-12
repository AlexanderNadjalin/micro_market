import stock
import datetime as dt


def main():
    start_time = dt.datetime(2018, 12, 27, 9)
    end_time = dt.datetime(2018, 12, 27, 10)
    a = stock.Stock('TEST', 100.0, start_time, 'H')

    a.period_ticks(start_time, end_time, 7.5, 2, 0.6, 0.005)

    plt = a.plot_bid_ask_liq()
    plt.show()


if __name__ == '__main__':
    main()
