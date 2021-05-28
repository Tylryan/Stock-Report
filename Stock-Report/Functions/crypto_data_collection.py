#!/usr/bin/python3.8
import requests
from pprint import pprint
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

pd.set_option('display.width', None)
# api_key = '33430961257a61d00efd2cadbeaedfeb'
api_key = 'F0E551BF-744B-4490-A465-B6A8B6EF0966'

ticker = 'BTC'

start = datetime.date(2019, 4, 1)
end = datetime.date(2021, 5, 27)

def get_close_data(ticker: str, start: datetime, end: datetime, api_key: str):
    # Date range of the request
    limit = str(end - start).split()[0]
    # Converting an easy datetime format to the required format
    start_converted = str(start) + 'T00:00'
    end_converted = str(start) + 'T00:00'

    # What increments would you like to see
    interval = '1DAY'
    url = f'https://rest.coinapi.io/v1/exchangerate/{ticker}/USD/history?period_id={interval}&time_start={start}&time_end={end}&limit={limit}'
    # Authenticating the request
    headers = {'X-CoinAPI-Key': api_key}
    # Requesting the data
    response = requests.get(url, headers=headers).json()
    print(response)
    # Turning that data into a dataframe
    df = pd.DataFrame(response)
    # # df['time_close'] = pd.to_datetime(df['time_close'], format="%Y-%m-%d")
    df['Date'] = df['time_close']
    df.set_index('Date', inplace=True)

    # excess_time = df.iloc[:, :3]
    # df = df.iloc[:, 3:]
    # Only retrieving the Closing Price
    df = pd.DataFrame(df.iloc[:,-1])
    return df


if __name__ == '__main__':
    df = get_close_data(ticker, start, end, api_key)

    print(df)

