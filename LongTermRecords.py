import os
import datetime
from pandas.tseries.offsets import BDay
import finviz
import csv
import pandas as pd
import os

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

weekno = datetime.datetime.today().weekday()

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"
long_term_path = r"C:\Users\Frank Einstein\Desktop\long term records"
list_of_tickers = r"C:\Users\Frank Einstein\Desktop\long term records\list of tickers.txt"

r = []

if 6 > weekno > 0:

    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            path = os.path.join(root, name)
            r.append(path)

    for x in r[24:]:

        path = x.replace("unique", "")
        check_path = os.path.join(path, str(last_business_day) + ".csv")

        if os.path.isfile(check_path):

            df = pd.read_csv(os.path.join(path, str(last_business_day) + ".csv"))

            for index, row in df.iterrows():

                ticker = row['Ticker']

                # add ticker to text file
                file = open(list_of_tickers, "a+")  # append mode
                if ticker not in file.readlines():
                    file.write(ticker + "\n")
                    file.close()

if 6 > weekno > 0:

    # add ticker to text file
    file = open(list_of_tickers, "r")  # append mode

    for line in file.readlines():
        stock = finviz.get_stock(line)

        stock['Date'] = str(last_business_day)

        ticker_file = os.path.join(long_term_path, line[:-2] + ".csv")

        if not os.path.isfile(ticker_file):

            with open(ticker_file, 'w+') as f:
                    w = csv.DictWriter(f, stock.keys())
                    w.writeheader()
                    w.writerow(stock)

        else:
            with open(ticker_file, 'a') as f:
                w = csv.DictWriter(f, stock.keys())
                w.writerow(stock)

