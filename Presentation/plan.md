# Purpose
A program that predicts asset prices of the user's choice and informs them when they should buy or sell via an email.

# Plan
- Stock Prediction
    - ARIMA 
        - MSE
    - Random Walk
        - MSE
    - LSTM (If you have time)
        - Would be good practice
            - MSE
    - Use whichever has the lowest MSE

- Strategy
    - Indicators (Buy or Sell)
        - Maybe if:
            - Predicted or current price is above or below 200 day moving average

    Don't really need this one as this will automatically happen with predicted prices
    > - Classification (1s and 0s from Raquel's indicators)
    >     - *Use Stock prediction to then create predicted indicators.*
    >     - Make sure it's a good model
    >         - Precision Recall Curve
    >         - Show whether or not it's over or under sampled
    >         - Accuracy
    >         - Recall
    >         - Precision
    >         - Etc
- Email
    - If Buy or Sell, Email the user
    - Email should contain:
        1. A list of stocks that they should buy or sell.
            - Send email if:
                - Predicted Price is a buy or sell
                    - Predicts 5 days in advance
                - If current price is a buy or sell.
                    - Current price is updated hourly
        2. Current Price, Indicators, Future Price, Buy/Sell
        3. Graphs if possible

- Cron Job
    - Set up a scheduled cron job to run every hour

