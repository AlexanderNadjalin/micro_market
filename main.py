import stock
import datetime as dt


def main():
    start_time = dt.datetime(2018, 12, 27, 9)
    end_time = dt.datetime(2018, 12, 27, 17, 30)
    a = stock.Stock('ALEX', 100.0, start_time, 'UH')

    a.period_ticks(start_time, end_time, 7.5, 2, 0.2, 0.005)

    p = a.plot()
    p.show()

    print(a.history)


if __name__ == '__main__':
    main()
