# Purpose
A program that predicts asset prices of the user's choice and informs them when they should buy or sell via an email.

# Plan
- Stock Prediction
    - ARIMA 
        - MSE
    - LSTM (If you have time)
        - Would be good practice
            - MSE

- Strategy
    - Indicators (Buy or Sell)
    - Classification (1s and 0s from Raquel's indicators)
        - *Use Stock prediction to then create predicted indicators.*
        - Make sure it's a good model
            - Precision Recall Curve
            - Show whether or not it's over or under sampled
            - Accuracy
            - Recall
            - Precision
            - Etc
- Email
    - If Buy or Sell, Email the user
    - Email should contain:
        1. A list of stocks that they should buy or sell.
        2. Current Price, Indicators, Future Price, Buy/Sell
        3. Graphs if possible
- Cron Job
    - Set up a scheduled cron job to run every hour

