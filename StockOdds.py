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

def percent(a, b):
    result = float(b - a) / a * 100.0

    return result


for stock_num in range(len(stocks)):

    percent_change = []

    try:
        # input a change percentage
        # in final results dataframe, count how many times that change percentage occurred
        # From each of these percentages, find if the following day traded higher or lower
        # Find the percentage of the following day trading higher or lower
        # Find the percentage of the following 5 days trading higher or lower

        stock = stocks[stock_num].strip("\n").replace(".csv", "")

        df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stock) + ".csv")

        stock_to_save = yf.Ticker(stock)

        # get historical market data
        hist = stock_to_save.history(period="1d")

        hist = hist.iloc[0].to_dict()
        hist['Date'] = last_business_day

        df = df.append(hist, ignore_index=True)

        close_list = df['Close'].tolist()

        for x in range(len(close_list) - 1):
            percent_change.append(percent(close_list[x], close_list[x + 1]))

        percent_change.insert(0, 0)
        df['Percent Change'] = percent_change

        df.to_csv("C:\\Users\\Frank Einstein\\Desktop\\" + str(stock) + ".csv")

    except Exception as err:
        print(err)



# compare_prices()
