# Find stocks that have between 24 and 28 RSI for last business day, add to text file
import pandas as pd
import glob
import os
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
import datetime
import finviz
import csv
import ctypes
import functools


MessageBox = ctypes.windll.user32.MessageBoxW

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

# loop through low RSI unique folder and add all matching results for previous business day to text file list
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\low rsi\\unique"
cross_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI\\stocks below RSI 30.txt"
cross_path_folder = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI\\unique"

df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None,  error_bad_lines=False),
                    glob.glob(folder_path + "/*.csv")))

formattedLBD = str(last_business_day).split('-')
proper_format = formattedLBD[1] + "/" + formattedLBD[2] + "/" + formattedLBD[0]

df = df[df['RSI (14)'].between(24, 28)]

df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] == proper_format]


def block_one():
    # add ticker to text file
    file = open(cross_path, "a+")  # append mode

    for index, row in df.iterrows():

        ticker = row['Ticker']

        if ticker.strip() not in file.readlines():
            file.write(ticker.strip() + '\n')

    file.close()


def block_two():
    file = open(cross_path, "r").readlines()  # append mode

    for line in file:
        try:
            stock = finviz.get_stock(line.strip())

            first_story = [x[0] for x in finviz.get_news(line.strip())]

            stock['Date'] = str(last_business_day)
            stock['Ticker'] = line.strip()

            try:
                stock['News'] = first_story[0]
            except:
                print("error")

            path = os.path.join(cross_path_folder, line.strip() + ".csv")

            argument = str(line.strip() + " is breaking out with an RSI of " + stock['RSI (14)'])

            if float(stock['RSI (14)']) > 30:
                MessageBox(None, argument, 'RSI Alert', 0)
                file.remove(line)

                with open(cross_path, 'w') as f:
                    f.writelines(file)
                    f.close()

                if os.path.isfile(path):
                    ticker_df = pd.read_csv(path)

                    if not (ticker_df['Date'].str.contains(str(last_business_day)).any()):
                        with open(path, 'a') as f:
                            w = csv.DictWriter(f, stock.keys())
                            w.writerow(stock)
                            f.close()

                if not os.path.isfile(path):
                    with open(path, 'w+') as f:
                        w = csv.DictWriter(f, stock.keys())
                        w.writeheader()
                        w.writerow(stock)
                        f.close()
        except:
            print("error")


def block_three():
    content = open(cross_path, 'r').readlines()
    content_set = set(content)
    clean_data = open(cross_path, 'w')

    for line in content_set:
        clean_data.write(line)


block_one()
block_two()
block_three()
