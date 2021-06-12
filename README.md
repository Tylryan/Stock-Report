# Purpose
This application emails you if stocks or cryptocurrencies of your selection are below their normal price range (Below their 200 day moving average).

This allows the user to stay a little more out of touch with the markets while still being informed of good times to buy.

# What It's Not
This application is not meant for the user to use it all the time. It should just run in the background as a Linux cronjob or Windows taskmanager app. Because of this, I have not added any user inputs. In order to change things, such as the moving average, email information, you would have to go into the files and do so.

# Requirements
1. You need to have Gmail account that allows applications to send emails for you.
    - [Here is a link](https://support.google.com/accounts/answer/6010255?hl=en) to the documentation
1. `cd` inside the `Stock-Report` directory.
    - Then run this command `pip3 install -r requirements.txt`
    - This sets up your environment to be able to run the program.
2. Create a `.env` file in your Data directory with the following variables:
    - `export USERNAME=yourUserName`
    - `export PASSWORD=yourPassword`
    - Username = your Gmail address.
    - Password = your Gmail third party password.
3. I would set this program to run automatically via a [cron job](https://phoenixnap.com/kb/set-up-cron-job-linux#:~:text=The%20Cron%20daemon%20is%20a,other%20commands%20to%20run%20automatically.)

# Ichimoku Cloud Strategy

To build this strategy we use The Technical Analysis Library for Python, ta, and call the data for Tenakan-sen (trend-ichimoku-a) and Kinjun_sen (trend-ichimoku-b) to create the buy/sell signals for the crossover called 'trend_ichimoku':

'trend_ichimoku'= where ('trend_ichimoku_a' > 'trend_ichimoku_b', buy,sell).

![image](https://user-images.githubusercontent.com/75185700/121785107-76d5b680-cb7d-11eb-98f6-dcdbd6e0952b.png)

We tried this strategy in different time frames ( 5years/daily, 6months/hour and 60days/5min) being the most effective the shortest time frame, as we compared the back test Cumulative Returns of the strategy against the one holding the position for each period, as we show it bellow: 

Example for TSLA:

![image](https://user-images.githubusercontent.com/75185700/121785458-7dfdc400-cb7f-11eb-966e-4d97e0b9ba02.png)

![image](https://user-images.githubusercontent.com/75185700/121785488-9a016580-cb7f-11eb-85fa-6696c9c49f8f.png)

![image](https://user-images.githubusercontent.com/75185700/121785492-9ff74680-cb7f-11eb-9933-758c038923d0.png)

![image](https://user-images.githubusercontent.com/75185700/121785498-a71e5480-cb7f-11eb-8a72-9ee674b7ffdf.png)

Summing up,

The Strategy is more recommended to be use in a short time frame (60 days/5 min) where it shows the cumulate returns most of the time is better than holding the position for the same time frame.

In stocks with negative trend, the strategy can mitigate the loss compared to the one holding the position
