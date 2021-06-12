import numpy as np
import pandas as pd
from pathlib import Path
import hvplot
import hvplot.pandas
from IPython.display import Markdown
import matplotlib as mpl

import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

import ta
from ta import add_all_ta_features
from ta.utils import dropna

pd.set_option("display.max_rows", 2000)
pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)


def initialize():
    """Initialize the dashboard, data storage, and account balances."""
    # @TODO: We will complete this later!
    pass


def build_dashboard(signals_df, portfolio_evaluation_df):
    """Build the dashboard."""
    # Create hvplot visualizations
    # Visualize exit position relative to close price
    Sell = signals_df[signals_df['Signal'] == -1.0]['Close'].hvplot.scatter(
    color='red',
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400,
    title= 'Ichimoku Cloud Trends')

    # Visualize entry position relative to close price
    Buy = signals_df[signals_df['Signal'] == 1.0]['Close'].hvplot.scatter(
    color='green',
    legend=False,
    ylabel='Price in $',
    width=1000,
    height=400,
    title= 'Ichimoku Cloud Trends')

    # Visualize close price for the investment
    Close_Price = signals_df[['Close']].hvplot(
    line_color='lightblue',
    legend=True,
    ylabel='Price in $',
    width=1000,
    height=400,
    title= 'Ichimoku Cloud Trends')

    # Visualize trend_ichimoku
    trend_ichimoku = signals_df[['trend_ichimoku_a','trend_ichimoku_b']].hvplot(
    ylabel='Price in $',
    legend=True,
    width=1000,
    height=400,
    title= 'Ichimoku Cloud Trends')
    
    portfolio_evaluation_table = portfolio_evaluation_df.hvplot.table(columns=["index", "Backtest"])
    

    # Build the dashboard
    entry_exit_plot = Close_Price * trend_ichimoku * Buy * Sell
    entry_exit_plot
    
    dashboard = entry_exit_plot + portfolio_evaluation_table 
    # dashboard.servable()
    return dashboard


def fetch_data(stock):
    """Fetches the latest prices."""
    # Set the file path and read CSV into a Pandas DataFrame
    # filepath = Path("../Resources/aapl.csv")
    
    #If you have a CSV file use this:
    #filepath = Path("AAPL.csv")
    #data_df = pd.read_csv(filepath)
    
    data_df = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = stock,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "60d",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "5m",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
    
    # Add all ta features
    data_df = add_all_ta_features(data_df, open="Open", high="High", low="Low", close="Close", volume="Volume")
    
    # Delete extra columns
    
    data_df = data_df.drop(['volume_adi', 'volume_obv', 'volume_cmf', 'volume_fi', 'volume_mfi', 'volume_em', 'volume_sma_em', 'volume_vpt',
              'volume_nvi', 'volume_vwap', 'volatility_atr', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'volatility_bbw',
              'volatility_bbp', 'volatility_bbhi', 'volatility_bbli', 'volatility_kcc', 'volatility_kch', 'volatility_kcl', 
              'volatility_kcw', 'volatility_kcp', 'volatility_kchi', 'volatility_kcli', 'volatility_dcl', 'volatility_dch', 
              'volatility_dcm', 'volatility_dcw', 'volatility_dcp', 'volatility_ui', 'trend_macd', 'trend_macd_signal', 'trend_macd_diff',
              'trend_sma_fast', 'trend_sma_slow', 'trend_ema_fast', 'trend_ema_slow', 'trend_adx', 'trend_adx_pos', 'trend_adx_neg', 
              'trend_vortex_ind_pos', 'trend_vortex_ind_neg', 'trend_vortex_ind_diff', 'trend_trix', 'trend_mass_index', 'trend_cci', 'trend_dpo',
              'trend_kst', 'trend_kst_sig', 'trend_kst_diff', 'trend_aroon_up', 'trend_aroon_down', 'trend_aroon_ind', 'trend_psar_up', 
              'trend_psar_down', 'trend_psar_up_indicator', 'trend_psar_down_indicator', 'trend_stc', 'momentum_rsi', 'momentum_stoch_rsi',
              'momentum_stoch_rsi_k', 'momentum_stoch_rsi_d', 'momentum_tsi', 'momentum_uo', 'momentum_stoch', 'momentum_stoch_signal', 'momentum_wr',
              'momentum_ao', 'momentum_kama', 'momentum_roc', 'momentum_ppo', 'momentum_ppo_signal', 'momentum_ppo_hist', 'others_dr', 'others_dlr',
              'others_cr', 'trend_ichimoku_conv' , 'trend_ichimoku_base'], axis=1)
    
   
    
    # Print the DataFrame
    
    print('----------------------------------------------------------------------------------')
    print()
    print(f'These are the last 10 values of the data')
    print()
    print(data_df.tail(10))
    return data_df


def generate_signals(data_df):
    """Generates trading signals for a given dataset."""
    # Grab just the `date` and `close` from the IEX dataset
    signals_df = data_df.loc[:, ['Close','trend_ichimoku_a', 'trend_ichimoku_b']]

    # Set the `date` column as the index
    #signals_df = signals_df.set_index('Date', drop=False)

    # Set the short window and long windows
    signals_df['trend_ichimoku'] = 0.0

    
    # Generate the trading signal 0 or 1,
    # where 0 is when the trend_ichimoku_a is under the trend_ichimoku_b, and
    # where 1 is when the trend_ichimoku_a is higher (or crosses over) the trend_ichimoku_b
    
    signals_df['trend_ichimoku'] = np.where(
    signals_df['trend_ichimoku_a'] > signals_df['trend_ichimoku_b'], 1.0, 0.0)

    # Calculate the points in time at which a position should be taken, 1 or -1
    signals_df['Signal'] = signals_df['trend_ichimoku'].diff()

    return signals_df



def execute_backtest(signals_df):
    """Backtests signal data."""
    # Set initial capital
    initial_capital = float(100000)

    # Set the share size
    share_size = 500

    # Take a 500 share position where the dual moving average crossover is 1 (SMA50 is greater than SMA200)
    signals_df["Position"] = share_size * signals_df["Signal"]

    # Find the points in time where a 500 share position is bought or sold
    signals_df["Entry/Exit Position"] = signals_df["Position"]

    # Multiply share price by entry/exit positions and get the cumulatively sum
    signals_df["Portfolio Holdings"] = (
        signals_df["Close"] * signals_df["Entry/Exit Position"].cumsum()
    )

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    signals_df["Portfolio Cash"] = (
        initial_capital
        - (signals_df["Close"] * signals_df["Entry/Exit Position"]).cumsum()
    )

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    signals_df["Portfolio Total"] = (
        signals_df["Portfolio Cash"] + signals_df["Portfolio Holdings"]
    )

    # Calculate the portfolio daily returns
    signals_df["Portfolio Daily Returns"] = signals_df["Portfolio Total"].pct_change()

    # Calculate the cumulative returns
    signals_df["Portfolio Cumulative Returns"] = (
        1 + signals_df["Portfolio Daily Returns"]
    ).cumprod() - 1
    
    print('-------------------------------------------------------------------------------')
    print()
    print(f'Total Cummulative Return is')
    print(signals_df["Portfolio Cumulative Returns"].tail(1))

    return signals_df


def execute_trade_strategy():
    """Makes a buy/sell/hold decision."""
    # @TODO: We will complete this later!
    pass


def evaluate_metrics(signals_df):
    """Generates evaluation metrics from backtested signal data."""
    # Prepare DataFrame for metrics
    metrics = [
        "Annual Return",
        "Cumulative Returns",
        "Annual Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
    ]

    columns = ["Backtest"]

    # Initialize the DataFrame with index set to evaluation metrics and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

    # Calculate cumulative return
    portfolio_evaluation_df.loc["Cumulative Returns"] = signals_df[
        "Portfolio Cumulative Returns"
    ][-1]

    # Calculate annualized return
    portfolio_evaluation_df.loc["Annual Return"] = (
        signals_df["Portfolio Daily Returns"].mean() * 252
    )

    # Calculate annual volatility
    portfolio_evaluation_df.loc["Annual Volatility"] = (
        1 + signals_df["Portfolio Daily Returns"].std() * np.sqrt(252)
    )

    # Calculate Sharpe Ratio
    portfolio_evaluation_df.loc["Sharpe Ratio"] = (
        signals_df["Portfolio Daily Returns"].mean() * 252
    ) / (signals_df["Portfolio Daily Returns"].std() * np.sqrt(252))

    # Calculate Downside Return
    sortino_ratio_df = signals_df[["Portfolio Daily Returns"]].copy()
    sortino_ratio_df.loc[:, "Downside Returns"] = 0

    target = 0
    mask = sortino_ratio_df["Portfolio Daily Returns"] < target
    sortino_ratio_df.loc[mask, "Downside Returns"] = (
        sortino_ratio_df["Portfolio Daily Returns"] ** 2
    )
    portfolio_evaluation_df

    # Calculate Sortino Ratio
    down_stdev = np.sqrt(sortino_ratio_df["Downside Returns"].mean()) * np.sqrt(252)
    expected_return = sortino_ratio_df["Portfolio Daily Returns"].mean() * 252
    sortino_ratio = expected_return / down_stdev

    portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio
    
    return portfolio_evaluation_df

def trade_evaluation(signals_df):
    
    """Generates Trade Entry and Exit table from signal data."""
    
    trade_evaluation_df = pd.DataFrame(
    columns=[
        'Stock', 
        'Entry Date', 
        'Exit Date', 
        'Shares', 
        'Entry Share Price', 
        'Exit Share Price', 
        'Entry Portfolio Holding', 
        'Exit Portfolio Holding', 
        'Profit/Loss'])

    # Initialize iterative variables
    entry_date = ''
    exit_date = ''
    entry_portfolio_holding = 0
    exit_portfolio_holding = 0
    share_size = 0
    entry_share_price = 0
    exit_share_price = 0

    # Loop through signal DataFrame
    # If `Entry/Exit` is 1, set entry trade metrics
    # Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit,
    # Then append the record to the trade evaluation DataFrame
    for index, row in signals_df.iterrows():
        if row['Signal'] == 1:
            entry_date = index
            entry_portfolio_holding = abs(row['Portfolio Holdings'])
            share_size = row['Entry/Exit Position']
            entry_share_price = row['Close']

        elif row['Signal'] == -1:
            exit_date = index
            exit_portfolio_holding = abs(row['Close'] * row['Entry/Exit Position'])
            exit_share_price = row['Close']
            profit_loss =  entry_portfolio_holding - exit_portfolio_holding
            trade_evaluation_df = trade_evaluation_df.append(
                {
                    'Stock': 'stock',
                    'Entry Date': entry_date,
                    'Exit Date': exit_date,
                    'Shares': share_size,
                    'Entry Share Price': entry_share_price,
                    'Exit Share Price': exit_share_price,
                    'Entry Portfolio Holding': entry_portfolio_holding,
                    'Exit Portfolio Holding': exit_portfolio_holding,
                    'Profit/Loss': profit_loss
                },
                ignore_index=True)
            
    print('------------------------------------------------------------------------------')
    print()
    print(f'Trades Executed')
    print(trade_evaluation_df)
   
    return trade_evaluation_df

def main():
    """Main Event Loop."""
    stock = input('Type in stock ticker:')
    data_df = fetch_data(stock)
    signals_df = generate_signals(data_df)
    tested_signals_df = execute_backtest(signals_df)
    signals_df = trade_evaluation(signals_df)
    portfolio_evaluation_df = evaluate_metrics(tested_signals_df)
    dashboard = build_dashboard(tested_signals_df, portfolio_evaluation_df) 
    hvplot.show(dashboard)
    #dashboard.servable()
    return

main()















