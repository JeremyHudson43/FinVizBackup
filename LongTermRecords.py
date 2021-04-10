import pandas as pd
import os
import datetime
from pandas.tseries.offsets import BDay
import finviz
import csv

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

weekno = datetime.datetime.today().weekday()

if 6 > weekno > 0:

    with open(r"C:\Users\Frank Einstein\Desktop\long term records\list of tickers.txt", "r") as myfile:

        for line in myfile.readlines():

            stock = finviz.get_stock(line)

            stock['Date'] = str(last_business_day)

            filepath = r"C:\Users\Frank Einstein\Desktop\long term records"

            ticker_file = os.path.join(filepath, (line[:-2] + ".csv"))

            if not os.path.isfile(ticker_file):

                with open(ticker_file, 'a+') as f:
                        w = csv.DictWriter(f, stock.keys())
                        w.writeheader()
                        w.writerow(stock)
            else:
                with open(ticker_file, 'a+') as f:
                    w = csv.DictWriter(f, stock.keys())
                    w.writerow(stock)


