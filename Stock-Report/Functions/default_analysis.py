#!/usr/bin/python

import stock_sources
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def default_analysis(long_close_df, current_price_close_df, sensitivity: float = 0.025):

    # Finding the moving averages
    # long_close_df.reset_index(inplace=True)
    # long_close_df['Date'] = long_close_df['Date'].apply(
    #     lambda x: str(x)[:10])
    # long_close_df.set_index('Date', inplace=True)
    long_close_df['50ma'] = long_close_df['Close'].rolling(window=50).mean()
    long_close_df['100ma'] = long_close_df['Close'].rolling(window=100).mean()

    # # If the current price is near either, email me.
    # current_50_ma = long_close_df['50ma'].tail(1).values
    # current_100_ma = long_close_df['100ma'].tail(1).values

    # # Current price
    # current_price = current_price_close_df.Close.values
    # # Conditions to be met
    # conditions = [
    #     # If the current price is plus or minus 5% of the 50 day moving average.
    #     (current_price <= current_50_ma *
    #      1.05) & (current_price > current_50_ma * 0.95),
    #     # If the current price is plus or minus 5% of the 200 day moving average.
    #     (current_price <= current_100_ma *
    #      1.05) & (current_price > current_100_ma * 0.95),
    # ]
    return long_close_df[['Close', '50ma', '100ma']]


def plot_dataframe(ticker, df):
    start = str(df.index[-200])[:10]
    end = str(df.index[-6])[:10]

    actual_close = df['Close'][-200:-4]
    actual_50 = df['50ma'][-200:-4]
    actual_100 = df['100ma'][-200:-4]

    predicted_close = df['Close'][-5:]
    predicted_50 = df['50ma'][-5:]
    predicted_100 = df['100ma'][-5:]

    actual_close.plot(
        title=f"{ticker} from {start} to {end} + 5",
        c="b",
        legend=True,
        grid=True
    )
    actual_50.plot(c="yellow", legend=True)
    actual_100.plot(c="orange", legend=True)

    predicted_close.plot(c="red", legend=True)
    predicted_50.plot(c="green", legend=True)
    predicted_100.plot(c="black", legend=True)
    # plt.show()
    plt.savefig("./Functions/Email/stock_image1.png",
                orientation="landscape")


def plot_dataframe_zoomed(ticker, df):
    start = str(df.index[-50])[:10]
    end = str(df.index[-6])[:10]
    actual_close = df['Close'][-50:-4]
    actual_50 = df['50ma'][-50:-4]
    actual_100 = df['100ma'][-50:-4]

    predicted_close = df['Close'][-5:]
    predicted_50 = df['50ma'][-5:]
    predicted_100 = df['100ma'][-5:]

    actual_close.plot(
        title=f"{ticker} from {start} to {end} + 5",
        c="b",
        legend=True,
        grid=True
    )
    actual_50.plot(c="yellow", legend=True)
    actual_100.plot(c="orange", legend=True)

    predicted_close.plot(c="red", legend=True)
    predicted_50.plot(c="green", legend=True)
    predicted_100.plot(c="black", legend=True)
    # plt.show()
    plt.savefig("./Functions/Email/stock_image2.png",
                orientation="landscape")


if __name__ == "__main__":
    ticker = "AAPL"
    long_df = stock_sources.long_period_df(ticker)
    current_price_df = stock_sources.current_price(ticker)
    df = default_analysis(
        long_df,
        current_price_df,
        sensitivity=0.01
    )
    da = default_analysis(long_df, current_price_df)
    print(da)
    plot_dataframe(ticker, long_df)
    plot_dataframe_zoomed(ticker, long_df)
