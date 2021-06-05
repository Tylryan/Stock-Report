#!/usr/bin/python
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from pprint import pprint
from statsmodels.tsa.arima_model import ARIMA
from stock_sources import long_period_df, only_close, returns, historic_cumulative_returns
from sklearn.metrics import mean_squared_error
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)


ticker = 'GME'


def random_walk_benchmark(ticker):
    # Creating the initial dataframe with a bunch of information
    df = long_period_df(ticker)

    # Chopping that dataframe down to Close only information
    close_df = only_close(df)

    close_df['Predicted'] = close_df['Close'].shift(1)
    close_df.dropna(inplace=True)

    mse = np.sqrt(mean_squared_error(close_df['Close'], close_df['Predicted']))
    print(close_df.tail())
    print(f"MSE: {mse}")


if __name__ == '__main__':
    random_walk_benchmark(ticker)
