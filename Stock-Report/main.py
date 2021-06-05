#!/usr/bin/python3

# adding Folder_2 to the system path
import sys
sys.path.insert(
    0, '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions')
# External Libraries


# Personal Modules
stock_ticker = 'AAPL'
crypto_ticker = 'BTC'


def main():
    from read_config import export_variables
    # from email_user import send_mail
    from data_analysis import stock_report
    from new_crypto_data_collection import get_close_data
    from arma_test import arima_prediction
    import os
    from time import sleep
    import pandas as pd
    import yfinance as yf
    import stock_sources
    import read_config
    import datetime
    print('End')

    ####################### Stock Data ######################################
    stock_df = stock_sources.long_period_df(stock_ticker)
    stock_close_df = stock_sources.only_close(stock_df)

    print(stock_close_df)

    ####################### Crypto Data ####################################

    env_location = '../Data/.env'
    user_name, password, crypto_api = read_config.export_variables(
        env_location)
    ticker = 'BTC'

    end = datetime.date.today()
    # 2 Years according to stock data
    start = end - datetime.timedelta(days=505)
    crypto_close_df = get_close_data(ticker, start, end, crypto_api)
    print(crypto_close_df)
    ####################### Predictions #####################################

    stock_prediction_mse, stock_prediction = arima_prediction(stock_close_df)
    print(f"Stock Prediction MSE {stock_prediction_mse}")
    # crypto_prediction_mse, crypto_prediction = arima_prediction(
    #     crypto_close_df)
    # username, password = export_variables()
    # report = stock_report(tickers)

    # report = stock_report(tickers)
    # send_mail(
    #     from_email=username,
    #     to_emails=username,
    #     report=report
    # )


if __name__ == "__main__":
    main()
