#!/usr/bin/python

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pprint import pprint
from statsmodels.tsa.arima_model import ARIMA
from stock_sources import long_period_df, only_close, returns, historic_cumulative_returns

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
df = long_period_df('AMD')

close_df = only_close(df)

standard_returns = close_df.pct_change().dropna()

best_order = []

# Here we are training on the data up until January 2021
for d in range(1, 2):
    for q in range(1, 3):
        for p in range(1, 3):
            order = (p, d, q)
            # Estimate and ARMA model using statsmodels (use order=(2, 1))
            model = ARIMA(
                np.array(standard_returns[:'2021-01']), order=order)

            # Fit the model and assign it to a variable called results
            results = model.fit()
            aic = results.aic
            order_results = [aic, order]
            best_order.append(order_results)


sorted(best_order)[0]
pprint(best_order)
optimal_order = best_order[1][1]

# Now we are actually testing the model on unseen data
model = ARIMA(standard_returns['2021-01':], order=optimal_order)
results = model.fit()


# Put this in your presentation just in case they ask for it.
print(results.summary())

only_forecast_graph = pd.DataFrame(results.forecast(steps=5)[0]).plot(
    title="5-Day Forecast of TSLA Returns",
    figsize=(15, 7.5),
    fontsize='large'
)

# The forecast will be appended to the actual return dataframe
forecast_df = pd.DataFrame(results.forecast(
    steps=5)[0], columns=['Simple Return'])

standard_returns['Simple Return'] = standard_returns['Close']
standard_returns.drop(columns='Close', inplace=True)
forecast = standard_returns.append(forecast_df)
forecast['Cumulative Returns'] = (1 + forecast['Simple Return']).cumprod()

time_frame = str(forecast.index[0])[:10]
forecast['Actual Price'] = close_df.Close[time_frame:]
forecast['Predicted Price'] = forecast['Cumulative Returns'] * \
    close_df['Close'][0]
print(forecast.tail(20))
# close, returns = returns(close_df)

# cumulative_returns = historic_cumulative_returns(close)
