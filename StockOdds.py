# Out of the [NUMBER] of other times [STOCK] was down / up [PERCENT] during a trading day,
# [PERCENT] of the time it traded higher / lower by the next day's market close.

# Out of the [NUMBER] of other times [STOCK] was down / up [PERCENT] during a trading day,
# [PERCENT] of the time it traded higher / lower by the market close 5 days later.

import yfinance as yf
import os
import pandas as pd
import datetime
from pandas.tseries.offsets import BDay

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\combined CSVs\\"

file_list = []

stocks = open("stocks.txt", "r").readlines()

for stock in stocks:

    try:
        # append latest day to each stock
        # calculate and append stock change percentage to a new column
        # input a change percentage
        # in final results dataframe, count how many times that change percentage occurred
        # From each of these percentages, find if the following day traded higher or lower
        # Find the percentage of the following day trading higher or lower
        # Find the percentage of the following 5 days trading higher or lower

        stock = stock.strip("\n").replace(".csv", "")

        # df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stock) + ".csv")

        df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\AAPL.csv")

        stock_to_save = yf.Ticker("AAPL")

        # get historical market data
        hist = stock_to_save.history(period="1d")

        hist = hist.iloc[0].to_dict()
        hist['Date'] = last_business_day

        df = df.append(hist, ignore_index=True)

        df.to_csv("C:\\Users\\Frank Einstein\\Desktop\\AAPL.csv")

    except Exception as err:
        print(err)


def percent(a, b):
    result = float(((b - a) * 100) / a)

    return result




# compare_prices()
