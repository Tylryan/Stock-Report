#!/usr/bin/python3

import yfinance as yf
import pandas as pd
from time import sleep

# you will need to have data for at least 2 years to find the 50day moving average and the 100 day moving average.

# Then you will need to gather info from the past 60 days to get hourly info to determine whether the hourly price is above or below those moving averages.
# TODO Add send dataframes to a csv. If you have already received that stock in the past week, then don't send it again


def long_period_df(ticker, period='2y', interval='1d', threads=True):

    long_df = yf.download(
        ticker,
        period=period,
        threads=threads
    )
    return long_df


def short_period_df(ticker, period='60d', interval='1h', threads=True):
    short_df = yf.download(
        ticker,
        period=period,
        interval=interval,
        threads=threads
    )
    return short_df


def only_close(df):
    df = df['Close']
    return df


if __name__ == "__main__":
    ticker = ['AAPL', 'TSLA']

    long_df = long_period_df(ticker)
    long_close = only_close(long_df)
    short_df = short_period_df(ticker)
    short_close = only_close(short_df)

    print(f"\nThis is {ticker}'s 2y historical data\n")
    print(long_df)
    print(f"\nThis is {ticker}'s 2y historical data only close\n")
    print(long_close)
    print(f"\nThis is {ticker}'s 60d historical data\n")
    print(short_df)
    print(f"\nThis is {ticker}'s 60d historical data only close\n")
    print(short_close)
