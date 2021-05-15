#!/usr/bin/python3

# External Libraries
import yfinance as yf
import pandas as pd
from time import sleep

# Personal Modules
from Functions.data_analysis import stock_report
from Functions.email_user import send_mail
import Functions.stock_sources
from Functions.read_config import export_variables
tickers = ['AAPL', 'GOOGL', 'PLUG']


username, password = export_variables()
report = stock_report(tickers)


def main():
    report = stock_report(tickers)
    send_mail(
        from_email=username,
        to_emails=username,
        report=report
    )


if __name__ == "__main__":
    main()
