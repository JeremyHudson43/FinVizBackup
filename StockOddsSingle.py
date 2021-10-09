# Out of the [NUMBER] of other times [STOCK] was down / up [PERCENT] during a trading day,
# [PERCENT] of the time it traded higher / lower by the market close 5 days later.

import yfinance as yf
import os
import pandas as pd
import datetime
from pandas.tseries.offsets import BDay
import traceback
today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\combined CSVs\\"

try:
    os.mkdir("C:\\Users\\Frank Einstein\\Desktop\\stock records\\prior probability one day\\" + str(last_business_day))
    os.mkdir("C:\\Users\\Frank Einstein\\Desktop\\stock records\\prior probability five days\\" + str(last_business_day))
except Exception as err:
    print("Bruh directory already exists")

file_list = []

stocks = open("stocks.txt", "r").readlines()

def percent_func(a, b):
    result = float(b - a) / a * 100.0

    return result


percent_change = []
percent = 0

stock = "AAPL"

df = pd.read_csv("E:\\stock history\\" + str(stock) + ".csv")

print(df)


close_list = df['Close'].tolist()

for item in close_list:
    item = "{:.2f}".format(item)

for x in range(len(close_list) - 1):
    change = percent_func(close_list[x], close_list[x + 1])
    change = "{:.1f}".format(change)

    percent_change.append(change)


percent_change.insert(0, 0)

df['Percent Change'] = percent_change


import numpy as np
for i in np.arange(-10, 10, 0.1):
    try:
        change_var = float("{:.1f}".format(i))
        print(change_var)

        winners_one = 0
        losers_one = 0
        losers_five = 0
        winners_five = 0

        difference = []
        difference_five = []

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
            difference.append(percent_func(only_close_prev_day[price_num], only_close_next_day[price_num]))
            if only_close_prev_day[price_num] > only_close_next_day[price_num]:
                losers_one+=1
            else:
                winners_one+=1

        filtered_df_prev_day['Difference'] = difference

        if sum(difference) / len(difference) > 0:
            filtered_df_prev_day['Mean Gain'] = filtered_df_prev_day['Difference'].mean()
        else:
            filtered_df_prev_day['Mean Loss'] = filtered_df_prev_day['Difference'].mean()

        if winners_one > losers_one:
            is_winner = True

        num_of_times = len(filtered_df['Percent Change'])

        # file = open("C:\\Users\\Frank Einstein\\Desktop\\stock records\\prior probability one day\\" + str(last_business_day) + "\\results_one_day.txt", "a+")

        average = "{:.1f}".format(sum(difference) / len(difference))

        if num_of_times > 10 and (winners_one > losers_one * 2):
            if float(change_var) > 0:

                output = f"Out of the {num_of_times} other times {stock} was up " \
                         f"{change_var}% during a trading day, there were {winners_one} winner(s) and " \
                         f"{losers_one} loser(s) by the end of \nthe next trading day for a mean change of " \
                         f"{average}%\n"

                print(output + "\n")
            elif float(change_var) < 0:

                output = f"Out of the {num_of_times} other times {stock} was down " \
                         f"{change_var}% during a trading day, there were {winners_one} winner(s) and " \
                         f"{losers_one} loser(s) by the end of \nthe next trading day for a mean change of " \
                         f"{average}%\n"

                print(output + "\n")

            filtered_df_prev_day.to_csv("E:\\stock records\\prior probability one day\\" + str(last_business_day) + "\\"
                                        + stock + ".csv")
            filtered_df_next_day.to_csv("E:\\stock records\\prior probability one day\\" + str(last_business_day) + "\\" +
                                         stock + ".csv", mode="a")

            # file.close()

            for price_num in range(len(only_close_prev_day)):
                difference_five.append(percent_func(only_close_prev_day[price_num], only_close_five_days[price_num]))
                if only_close_prev_day[price_num] > only_close_five_days[price_num]:
                    losers_five += 1
                else:
                    winners_five += 1

            filtered_df_prev_day['Difference'] = difference_five

            if sum(difference_five) / len(difference_five) > 0:
                filtered_df_prev_day['Mean Gain'] = filtered_df_prev_day['Difference'].mean()
            else:
                filtered_df_prev_day['Mean Loss'] = filtered_df_prev_day['Difference'].mean()

            if winners_five > losers_five:
                is_winner = True

            num_of_times = len(filtered_df['Percent Change'])

            # file = open("C:\\Users\\Frank Einstein\\Desktop\\stock records\\prior probability five days\\" + str(last_business_day) + "\\results_five_days.txt", "a+")

            average = "{:.1f}".format(sum(difference_five) / len(difference_five))

            print("average", average)

            if float(change_var) > 0:

                output = f"Out of the {num_of_times} other times {stock} was up " \
                         f"{change_var}% during a trading day, there were {winners_five} winner(s) and " \
                         f"{losers_five} loser(s) by the end of \nthe next 5 trading days for a mean change of " \
                         f"{average}%\n"

                # file.write(output + "\n")
                print(output + "\n")

            elif float(change_var) < 0:

                output = f"Out of the {num_of_times} other times {stock} was down " \
                         f"{change_var}% during a trading day, there were {winners_five} winner(s) and " \
                         f"{losers_five} loser(s) by the end of \nthe next 5 trading days for a mean change of " \
                         f"{average}%\n"

                # file.write(output + "\n")
                print(output + "\n")

            filtered_df_prev_day.to_csv("E:\\stock records\\prior probability five days\\" + str(last_business_day) + "\\"
                                        + stock + ".csv")
            filtered_df_five_days.to_csv("E:\\stock records\\prior probability five days\\" + str(last_business_day) + "\\" +
                                        stock + ".csv", mode="a")
            # file.close()

    except Exception as err:
        print(traceback.format_exc())

