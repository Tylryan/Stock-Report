#!/usr/bin/python

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import datetime
from pprint import pprint
from statsmodels.tsa.arima_model import ARIMA
from stock_sources import long_period_df, only_close, returns, historic_cumulative_returns
from crypto_data_collection import get_close_data
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

######################## GETTING DATA ################################
# Creating the initial dataframe with a bunch of information


def arima_prediction(close_df, test_percent=0.8):

    ######################## SPLITTING THE DATA ##########################
    original_close_df = close_df
    close_df = close_df.pct_change().dropna()
    # Creating a train test split
    observances = len(close_df)
    # Train consists of the first 80% of the close df
    train = close_df.iloc[:math.ceil(
        observances * test_percent), :]
    # Test Consists of last 20% of the close df
    test = close_df.iloc[math.ceil(
        observances * test_percent):, :]

    ######################## OPTIMAL ORDER FOR TRAINING DATA #############
    best_order = []

    for d in range(0, 3):
        for q in range(1, 5):
            for p in range(1, 5):
                order = (p, d, q)
                # Using the Training data in this case to find the best order
                model = ARIMA(
                    np.array(train), order=order)
                try:

                    # Fit the model and assign it to a variable called results
                    results = model.fit(disp=0)
                except Exception as e:
                    print(e)
                # This is one of the performance indicators.
                # The other one is MSE
                aic = results.aic
                order_results = (aic, order)
                best_order.append(order_results)

    print("Done Training")
    # Sort the orders by AIC and give me
    best_order = sorted(best_order)
    optimal_order = best_order[0][1]
    second_best_order = best_order[1][1]

    ########################## TRAINING DATA ################################
    train_model = ARIMA(train, order=optimal_order)

    train_results = train_model.fit(disp=0)
    train_score = train_results.summary()
    train_forecast = pd.DataFrame(
        train_results.forecast(len(test))[0],
        columns=['Close']
    )

    # Add the predicted returns to the actual returns dataframe
    train_predictions = train.append(train_forecast)
    train_predictions['Predicted Returns'] = train_predictions['Close']
    # train_predictions.drop(columns='Close', inplace=True)
    # Create a cumulative returns column
    all_actual_prices_df = pd.DataFrame(original_close_df[1:])
    train_predictions['Predicted Price'] = (
        1 + train_predictions['Predicted Returns']).cumprod() * all_actual_prices_df.Close.values[0]
    # Getting the actual prices to compare to the predicted prices
    train_predictions['Actual Price'] = all_actual_prices_df.Close.values
    # Cutting down the predictions to only 5 days
    train_prediction_5_day = train_predictions[:-95].dropna()
    train_prediction_5_day = train_prediction_5_day[[
        'Actual Price', 'Predicted Price']]
    ######################### COMPARE TRAINING TO ACTUAL DATA #################
    # Finding the MSE of those predictions
    train_mse = np.sqrt(mean_squared_error(
        train_prediction_5_day['Actual Price'],
        train_prediction_5_day['Predicted Price'])
    )
  # ########################### TESTING DATA #################################
    print("Starting Test")
    try:
        test_model = ARIMA(test, order=optimal_order)
        test_results = test_model.fit(disp=0)
    except Exception as e:
        print(e)
    finally:
        test_model = ARIMA(test, order=second_best_order)
        test_results = test_model.fit(disp=0)

    test_forecast = pd.DataFrame(
        test_results.forecast(5)[0],
        columns=['Close'],
        index=pd.date_range(
            start=pd.to_datetime(test.index[-1]) + datetime.timedelta(1),
            periods=5,
            freq="D"
        )
    )

    # Add the predicted returns to the actual returns dataframe
    test_predictions = close_df.append(test_forecast)
    # Create a cumulative returns column
    test_predictions['Close'] = (
        1 + test_predictions['Close']).cumprod() * all_actual_prices_df.Close.values[0]
    test_predictions.index.rename('Date', inplace=True)
    # Getting the actual prices to compare to the predicted prices
    ######################### COMPARE TRAINING TO ACTUAL DATA #################
    return train_mse, test_predictions


if __name__ == '__main__':

    ticker = 'AAPL'
    df = long_period_df(ticker)

    # Chopping that dataframe down to Close only information
    close_df = only_close(df)

    # Finding the percent change of the closing data
    standard_returns = close_df.pct_change().dropna()

    mse, test_prediction = arima_prediction(close_df)
    print(test_prediction)

    # # print('\n\n\n\nCrypto Data')
    # ticker = 'BTC'

    # end = datetime.date.today()
    # start = end - datetime.timedelta(days=505)

    # import read_config
    # env_location = '../../Data/.env'
    # user_name, password, crypto_api = read_config.export_variables(
    #     env_location)
    # crypto_df = get_close_data(ticker, start, end, crypto_api)

    # arima_prediction(crypto_df)
