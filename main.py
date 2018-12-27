import stock
import datetime as dt


def main():
    a = stock.Stock('ALEX', 100.0)
    start_time = dt.datetime(2018, 12, 27, 9)
    end_time = dt.datetime(2018, 12, 27, 9, 1)
    a.period_ticks(start_time, end_time, 1, 2, 0.2, 0.01)
    print(a.history)


if __name__ == '__main__':
    main()
