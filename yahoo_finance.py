from datetime import datetime
import os

import yfinance as yf


periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

def get_ticker(ticker, interval, start_date=None, end_date=None, period=None):
    if start_date is None and end_date is None:
        if period is None:
            raise Exception('Either start and end dates or a period must be specified, but both are None')

    if start_date is not None and end_date is not None:
        if period is not None:
            raise Exception('Either start and end dates or a period must be specified, not both')

    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise Exception('Start date cannot be after end date')

    if period is not None:
        if period not in periods:
            raise Exception(f'Invalid period: {period} (valid periods: {periods})')

    if interval not in intervals:
        raise Exception(f'Invalid interval: {interval} (valid intervals: {intervals})')

    ticker = yf.Ticker(ticker)
    if period is not None:
        return ticker.history(period=period, interval=interval)

    if start_date is None:
        start_date = end_date - datetime.timedelta(days=365)
    if end_date is None:
        end_date = start_date + datetime.timedelta(days=365)
    return ticker.history(start=start_date, end=end_date, interval=interval)


def create_csv(ticker, interval, start_date=None, end_date=None, period=None):
    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    data = get_ticker(ticker, interval, start_date, end_date, period)
    # save only if there is data
    if len(data) > 0:
        min_date = data.index.min().strftime('%Y-%m-%d')
        max_date = data.index.max().strftime('%Y-%m-%d')
        path = f'datasets/{ticker}_{interval}_{min_date}_{max_date}.csv'
        data.to_csv(path)


if __name__ == '__main__':
    """tickers_list = ['APPL', 'AMZN', 'NFLX', 'GOOG', 'FB', 'MSFT', 'TSLA', 'NVDA', 'ADBE', 'TWTR']
    tickers_list.sort()  # actually not needed, just for readability
    for ticker in tickers_list:
        print(f'Creating csv for {ticker}')
        for interval in intervals:
            for period in periods:
                create_csv(ticker, interval, period=period)"""
    # Google every 2 minutes, from 2023-01-04 to 2023-01-10 17h (5 pm)
    create_csv('GOOG', '2m', start_date=datetime(2023, 1, 4), end_date=datetime(2023, 1, 10, 17))
