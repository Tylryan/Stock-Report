#!/usr/bin/python3

import sys
import os
from time import sleep
import pandas as pd
import yfinance as yf
import datetime
sys.path.insert(
    0, '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions')


# Tickers to watch
stock_ticker = 'QQQ'
crypto_ticker = 'BTC'

# Can be changed to a more desired location
env_location = '../Data/.env'


def main():
    ####################### IMPORTS ##########################################

    # Personal Modules
    from read_config import export_variables
    # from email_user import send_mail
    from data_analysis import stock_report
    from crypto_data_collection import get_close_data
    from arma_test import arima_prediction
    import stock_sources
    import read_config
    from random_walk import random_walk_benchmark
    from default_analysis import default_analysis

    # Personal information to be used in the program
    email, password, crypto_api = read_config.export_variables(
        env_location)

    ####################### Stock Data ######################################
    stock_df = stock_sources.long_period_df(stock_ticker)
    stock_close_df = stock_sources.only_close(stock_df)

    print(stock_close_df)

    ####################### Stock Predictions ###############################
    stock_train_prediction_mse, stock_prediction_df = arima_prediction(
        stock_close_df)
    print(f"Stock Prediction MSE {stock_train_prediction_mse}")

    ###################### Stock Benchmark #################################

    stock_prediction_benchmark_mse = random_walk_benchmark(stock_close_df)
    print(stock_prediction_benchmark_mse)

    ####################### Crypto Data ####################################

    end = datetime.date.today()
    2 Years according to stock data
    start = end - datetime.timedelta(days=505)
    crypto_close_df = get_close_data(crypto_ticker, start, end, crypto_api)
    print(crypto_close_df)

    ####################### Crypto Predictions ###############################

    crypto_train_prediction_mse, crypto_prediction = arima_prediction(
        crypto_close_df
    )
    crypto_prediction_mse, crypto_prediction = arima_prediction(
        crypto_close_df)
    report = stock_report(tickers)

    ###################### Crypto Prediction Benchmark #######################

    crypto_prediction_benchmark_mse = random_walk_benchmark(crypto_close_df)

    good_stock_prediction = False
    # good_crypto_prediction = False

    good_stock_prediction = True if stock_train_prediction_mse < stock_prediction_benchmark_mse else False
    good_crypto_prediction = True if crypto_train_prediction_mse < crypto_prediction_benchmark_mse else False

    print('\n\n\n\n\n\n\n')
    print(good_stock_prediction)

    print('\n\n\n\n\n\n\n')
    print(f"Good Crypto Prediction: {good_crypto_prediction}")

    # If stock_train_prediction_mse IS LESS than random_walk_benchmark, then use it.
    # Else Don't and only email the user moving averages graph

    ####################### Default Analysis ################################

    current_stock_price = stock_sources.current_price(stock_ticker)

    stock_default_analysis_response = default_analysis(
        stock_prediction_df, current_stock_price)

    print(f"Default Stock Analysis Says: {stock_default_analysis_response}")
    print(len(stock_prediction_df))

    ####################### STRATEGY #######################################

    # If this is True, email them everything

    ####################### EMAIL ##########################################

    # Should contain: MSEs, Predictions, Current Price, Moving Average Chart
    # If no move to be made, moving averaage chart should be sent regardless along with a different title

    # report = stock_report(tickers)
    # send_mail(
    #     from_email=username,
    #     to_emails=username,
    #     report=report
    # )


if __name__ == "__main__":
    main()
