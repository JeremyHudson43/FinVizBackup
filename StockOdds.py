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

def percent_func(a, b):
    result = float(b - a) / a * 100.0

    return result


for stock_num in range(len(stocks)):

    percent_change = []
    percent = 0

    try:
        stock = stocks[stock_num].strip("\n").replace(".csv", "")

        df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stock) + ".csv")

        stock_to_save = yf.Ticker(stock)

        # get historical market data
        hist = stock_to_save.history(period="1d")

        hist = hist.iloc[0].to_dict()
        hist['Date'] = last_business_day

        # df = df.append(hist, ignore_index=True)

        close_list = df['Close'].tolist()

        for item in close_list:
            item = "{:.2f}".format(item)

        for x in range(len(close_list) - 1):
            change = percent_func(close_list[x], close_list[x + 1])
            change = "{:.1f}".format(change)

            percent_change.append(change)

        percent_change.insert(0, 0)

        df['Percent Change'] = percent_change

        change_var = percent_change[-1]

        # check dataframe next day after change % and see if lower or higher, increment counter
        # every time you see the specified %, then add up winners and losers to find percent

        winners = 0
        losers = 0

        df_mask = pd.to_numeric(df['Percent Change']) == change_var

        ### NEXT DAY
        filtered_df = df[df_mask]

        index_list = filtered_df.index.tolist()
        index_list_next_day = [x + 1 for x in index_list]

        df_mask_prev_day = df.index.isin(index_list)
        df_mask_next_day = df.index.isin(index_list_next_day)

        filtered_df_prev_day = df[df_mask_prev_day]
        filtered_df_next_day = df[df_mask_next_day]

        only_close_prev_day = filtered_df_prev_day['Close'].tolist()
        only_close_next_day = filtered_df_next_day['Close'].tolist()

        for price_num in range(len(only_close_next_day)):
            if only_close_prev_day[price_num] > only_close_next_day[price_num]:
                losers+=1
            else:
                winners+=1

        if winners != 0 and losers != 0:
           if winners > losers:
              percent = losers / winners
           else:
              percent = winners / losers

        percent = percent * 100
        num_of_times = len(filtered_df['Percent Change'])

        if float(change_var) > 0:
            file = open("results.txt", "a+")

            output = f"Out of the {num_of_times} of other times {stock} was up " \
                     f"{change_var}% during a trading day, {percent}% of the time it traded higher " \
                     f"by the next day's market close."
         else:
            output = f"Out of the {num_of_times} of other times {stock} was down " \
                  f"{change_var}% during a trading day, {percent}% of the time it traded lower " \
                  f"by the next day's market close."

        file.write(output + "\n")

        # filtered_df.to_csv("C:\\Users\\Frank Einstein\\Desktop\\"  + stock + ".csv")

    except Exception as err:
        print(err)




# compare_prices()
