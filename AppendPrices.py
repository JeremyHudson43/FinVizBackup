import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from datetime import datetime
from os import listdir
from os.path import isfile, join

mypath = "E:\\stock stuff\\long term records"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for stock in onlyfiles:

    try:

        stock = stock[:-4]

        sma_200_list_final = []
        sma_20_list_final = []
        sma_50_list_final = []

        stock_to_save = yf.Ticker(stock)

        df_one = pd.read_csv("E:\\stock stuff\\long term records\\" + stock + ".csv")

        dates = df_one['Date'].tolist()

        start_date_one = datetime.strptime(dates[0], "%Y-%m-%d").date()
        start_date_two = datetime.strptime(dates[-1], "%Y-%m-%d").date()

        # get historical market data
        hist = stock_to_save.history(start=dates[0], end=start_date_two + relativedelta(days=+2))

        close_prices = df_one['Price'].tolist()
        sma_20_list = df_one['SMA20'].tolist()
        sma_50_list = df_one['SMA50'].tolist()
        sma_200_list = df_one['SMA200'].tolist()

    except Exception as err:
        print(err)

    for date_index in range(len(sma_20_list)):

        try:

            print(sma_200_list[date_index], stock)

            sma_200 = (close_prices[date_index] / (100 + float(sma_200_list[date_index].replace("%", "")))) * 100
            sma_200_list_final.append(sma_200)

            sma_20 = (close_prices[date_index] / (100 + float(sma_20_list[date_index].replace("%", "")))) * 100
            sma_20_list_final.append(sma_20)

            sma_50 = (close_prices[date_index] / (100 + float(sma_50_list[date_index].replace("%", "")))) * 100
            sma_50_list_final.append(sma_50)

        except Exception as err:
            print(err)

    df_one['SMA20'] = pd.Series(sma_20_list_final)
    df_one['SMA50'] = pd.Series(sma_50_list_final)
    df_one['SMA200'] = pd.Series(sma_200_list_final)

    dates = df_one['Date'].tolist()

    hist_close = [x for x in hist['Close']]
    hist_open = [x for x in hist['Open']]

    hist_low = [x for x in hist['Low']]
    hist_high = [x for x in hist['High']]

    df_one['Close'] = pd.Series(hist_close)
    df_one['Open'] = pd.Series(hist_open)
    df_one['Low'] = pd.Series(hist_low)
    df_one['High'] = pd.Series(hist_high)

    df_one = df_one.drop_duplicates(subset=['Date'])

    df_one.to_csv("E:\\stock stuff\\filtered long term\\" + stock + ".csv")

    # filter to June 1st
    # follow backtesting algo text file