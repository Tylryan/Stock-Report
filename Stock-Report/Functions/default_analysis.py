#!/usr/bin/python

import stock_sources


def default_analysis(long_close_df, current_price_close_df, sensitivity: float = 0.025):

    # Finding the moving averages
    long_close_df['50ma'] = long_close_df.Close.rolling(window=50).mean()
    long_close_df['100ma'] = long_close_df.Close.rolling(window=100).mean()

    # If the current price is near either, email me.
    current_50_ma = long_close_df['50ma'].tail(1).values
    current_100_ma = long_close_df['100ma'].tail(1).values

    # Current price
    current_price = current_price_close_df.Close.values
    # Conditions to be met
    conditions = [
        # If the current price is plus or minus 5% of the 50 day moving average.
        (current_price <= current_50_ma *
         1.05) & (current_price > current_50_ma * 0.95),
        # If the current price is plus or minus 5% of the 200 day moving average.
        (current_price <= current_100_ma *
         1.05) & (current_price > current_100_ma * 0.95),
    ]
    # If any conditions are met, return True
    if any(conditions) == True:
        print(current_price)
        print(current_50_ma)
        print(current_100_ma)
        return True
    else:
        return False


if __name__ == "__main__":
    ticker = "AAPL"
    long_df = stock_sources.long_period_df(ticker)
    current_price_df = stock_sources.current_price(ticker)
    df = default_analysis(
        long_df,
        current_price_df,
        sensitivity=0.01
    )
    print(df)
