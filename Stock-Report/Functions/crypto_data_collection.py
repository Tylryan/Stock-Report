#!/usr/bin/python3.8
import requests
from pprint import pprint
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
pd.set_option('display.width', None)

ticker = 'BTC'


start = datetime.date(2019, 12, 2)
end = datetime.date(2021, 6, 2)
interval = '1HRS'

# Example intervals
# SEC, MIN, HRS, DAY


def get_close_data(
        ticker: str,
        start: datetime,
        end: datetime,
        api_key: str,
        interval: str = '1HRS'
):

    # Date range of the request
    limit = str(end - start).split()[0]
    # Distance between ticks
    interval = '1DAY'
    url = f'https://rest.coinapi.io/v1/exchangerate/{ticker}/USD/history?period_id={interval}&time_start={start}&time_end={end}&limit={limit}'
    # Authenticating the request
    headers = {'X-CoinAPI-Key': api_key}
    # Requesting the data
    response = requests.get(url, headers=headers).json()
    # Turning response to a dataframe
    df = pd.DataFrame(response)
    # Changing the column name to 'Date' for easier use
    df['Date'] = df['time_close']
    # Renaming the rate_close column to 'Close'
    df['Close'] = df['rate_close']
    # Only Retrieve the Date and Close Columns
    df = df[['Date', 'Close']]
    # Only Show Year Month Day
    df['Date'] = pd.to_datetime(df['Date'].str[:10])
    return df


def get_existing_data():
    df = pd.read_csv('test.csv', parse_dates=True)
    return df


if __name__ == '__main__':
    # API Request

    import read_config
    env_location = '../../Data/.env'
    user_name, password, crypto_api = read_config.export_variables(
        env_location)
    df = get_close_data(ticker, start, end, crypto_api)
    df.set_index('Date', inplace=True)
    df['Short'] = df.Close.rolling(window=24).mean()
    df['Long'] = df.Close.rolling(window=96).mean()
    df.plot(
        title=f"{ticker} | {start}-{end} | interval {interval}",
        figsize=(15, 7.5)
    )
    plt.show()
    # df.to_csv('test.csv', sep=',', index=False)
    # print(df)

    # # Messing with the data
    # df = get_existing_data()
    # print(df)
