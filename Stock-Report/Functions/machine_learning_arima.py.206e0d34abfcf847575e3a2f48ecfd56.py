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


def arima_prediction(close, test_percent=0.8):

    ######################## GETTING DATA ################################
    # Creating the initial dataframe with a bunch of information
    df = long_period_df(ticker)

    # Chopping that dataframe down to Close only information
    close_df = only_close(df)

    # Finding the percent change of the closing data
    standard_returns = close_df.pct_change().dropna()

    ######################## SPLITTING THE DATA ##########################
    # Creating a train test split
    observances = len(standard_returns)
    # Train consists of the first 80% of the close df
    train = standard_returns.iloc[:math.ceil(observances * test_percent), :]
    # Test Consists of last 20% of the close df
    test = standard_returns.iloc[math.ceil(observances * test_percent):, :]

    ######################## OPTIMAL ORDER FOR TRAINING DATA #############
    best_order = []

    # Here we are training on the data up until January 2021
    for d in range(1, 2):
        for q in range(1, 5):
            for p in range(1, 5):
                order = (p, d, q)
                # Using the Training data in this case to find the best order
                model = ARIMA(
                    np.array(train), order=order)

                # Fit the model and assign it to a variable called results
                results = model.fit()
                # This is one of the performance indicators.
                # The other one is MSE
                aic = results.aic
                order_results = [aic, order]
                best_order.append(order_results)

    # Sort the orders by AIC and give me
    sorted(best_order)
    print(best_order)
    pprint(best_order)
    optimal_order = best_order[-1][1]
    print(optimal_order)
    ########################## TRAINING DATA ################################
    print('\n\n\n\nTRAINING')
    train_model = ARIMA(train, order=optimal_order)
    train_results = train_model.fit()

    # # Forecasting the same number of days as the length of the test data
    train_forecast = pd.DataFrame(
        train_results.forecast(len(test))[0],
        columns=['Close']
    )
    # # HEERE
    # # Add the predicted returns to the actual returns dataframe
    train_predictions = train.append(train_forecast)
    # # Create a cumulative returns column
    train_predictions['Cumulative Returns'] = (
        1 + train_predictions['Close']).cumprod()
    # # Getting just the day month year of the index
    train_time_frame = str(train_predictions.index[0])[:10]
    all_actual_prices_df = pd.DataFrame(close_df[1:])

    # # Getting the actual prices to compare to the predicted prices
    train_predictions['Actual Price'] = all_actual_prices_df.Close.values
    train_predictions['Predicted Price'] = train_predictions['Cumulative Returns'] * \
        all_actual_prices_df['Close'][0]

    # # training_df = pd.DataFrame(
    # #     {
    # #         "Actual Returns": test.Close,
    # #         "Predicted Returns": train_results.forecast(steps=len(test))[0],
    # #         "Actual Price": close_df[len(test):]
    # #     },
    # #     index=test.Close.index
    # # )

    # ########################### PERFORMANCE OF TRAINING ######################
# #     training_df['Predicted Price'] = (1 + training_df["Predicted Returns"]).cumprod() * \
# #         training_df['Actual Price'][0]
    # # training_df['Predicted'] = train_results.forecast(steps=len(test))[0]
    # # training_df['Actual'] = test.Close

    # # print(train_results.summary())
    # print('\n\n\nDONE TRAINING\n\n\n\n')

    # # Now we are actually testing the model on unseen data
    # ########################### TESTING DATA #################################
    model = ARIMA(test, order=optimal_order)
    # # model = ARIMA(standard_returns['2021-01':], order=optimal_order)
    results = model.fit()

    # # Put this in your presentation just in case they ask for it.
    # # print(results.summary())
    # ######################### FORECATING WITH TEST DATA ####################
    # only_forecast_graph = pd.DataFrame(results.forecast(steps=5)[0]).plot(
    #     title="5-Day Forecast of TSLA Returns",
    #     figsize=(15, 7.5),
    #     fontsize='large'
    # )

    # # The forecast will be appended to the actual return dataframe
    # forecast_df = pd.DataFrame(results.forecast(
    #     steps=5)[0], columns=['Simple Return'])

    # standard_returns['Simple Return'] = standard_returns['Close']
    # standard_returns.drop(columns='Close', inplace=True)
    # forecast = standard_returns.append(forecast_df)
    # forecast['Cumulative Returns'] = (1 + forecast['Simple Return']).cumprod()

    # time_frame = str(forecast.index[0])[:10]
    # forecast['Actual Price'] = close_df.Close[time_frame:]
    # forecast['Predicted Price'] = forecast['Cumulative Returns'] * \
    #     close_df['Close'][0]
    # print('\n\n\nTraining Mean Squared Error')

    # # Training 100 days out is not helpful. I only want to predict max 5 days out
    # # So I only want the mse on max 5 days out.
    # train_mse = np.sqrt(mean_squared_error(train_predictions['Actual Price'][:-95],
                                           # train_predictions['Predicted Price'].values[:-95]))
    # # print(training_df)
    print(train_predictions[:-95].tail(10))
    # print(train_mse)
    # print(optimal_order)
    # sorted(best_order)[0]
    # print(best_order)
    # return forecast


forecast=arima_prediction('AAPL')
# # print(forecast)
# # close, returns = returns(close_df)

# # cumulative_returns = historic_cumulative_returns(close)
