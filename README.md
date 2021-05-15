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
