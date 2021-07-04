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

def ratio(a, b):
    a = float(a)
    b = float(b)
    if b == 0:
        return a
    return ratio(b, a % b)

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

        change_var = float(percent_change[-1])

        percent_change.insert(0, 0)

        df['Percent Change'] = percent_change

        # check dataframe next day after change % and see if lower or higher, increment counter
        # every time you see the specified %, then add up winners and losers to find percent

        winners_one = 0
        losers_one = 0
        losers_five = 0
        winners_five = 0

        is_winner = False

        df_mask = pd.to_numeric(df['Percent Change']) == change_var

        ### NEXT DAY
        filtered_df = df[df_mask]

        index_list = filtered_df.index.tolist()
        index_list_next_day = [x + 1 for x in index_list]
        index_list_five_days = [x + 5 for x in index_list]

        df_mask_prev_day = df.index.isin(index_list)
        df_mask_next_day = df.index.isin(index_list_next_day)
        df_mask_five_days = df.index.isin(index_list_five_days)

        filtered_df_prev_day = df[df_mask_prev_day]
        filtered_df_next_day = df[df_mask_next_day]
        filtered_df_five_days = df[df_mask_five_days]

        filtered_df_prev_day = filtered_df_prev_day[:-1]

        only_close_prev_day = filtered_df_prev_day['Close'].tolist()
        only_close_next_day = filtered_df_next_day['Close'].tolist()
        only_close_five_days = filtered_df_five_days['Close'].tolist()

        for price_num in range(len(only_close_prev_day)):
            if only_close_prev_day[price_num] > only_close_five_days[price_num]:
                losers_one+=1
            else:
                winners_one+=1

        if winners_one != 0 and losers_one != 0:
           if winners_one > losers_one:
              is_winner = True
              percent = losers_one / winners_one
           else:
              percent = winners_one / losers_one

        print(stock, winners_one, losers_one)

        percent = percent * 100
        percent = "{:.1f}".format(percent)

        num_of_times = len(filtered_df['Percent Change'])

        file = open("results.txt", "a+")

        if num_of_times > 0:

            if float(change_var) > 0:

                output = f"Out of the {num_of_times} other times {stock} was up " \
                         f"{change_var}% during a trading day, there was {winners_one} winner(s) and" \
                         f"{losers_one} loser(s)"

                file.write(output.replace("-", "") + "\n")

            elif float(change_var) < 0:

                output = f"Out of the {num_of_times} other times {stock} was up " \
                         f"{change_var}% during a trading day, there was {winners_one} winner(s) and" \
                         f"{losers_one} loser(s)"

                file.write(output.replace("-", "")  + "\n")

            filtered_df_prev_day.to_csv("C:\\Users\\Frank Einstein\\Desktop\\records\\" + stock + ".csv")
            filtered_df_five_days.to_csv("C:\\Users\\Frank Einstein\\Desktop\\records\\" + stock + ".csv", mode="a")

    except Exception as err:
        print(err)
