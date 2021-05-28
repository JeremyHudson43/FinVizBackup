import pandas as pd
import os
import finviz
import csv
import datetime
from pandas.tseries.offsets import BDay

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

r = []

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

weekno = datetime.datetime.today().weekday()


for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        r.append(path)

    for x in r[25:]:

        path = x.replace("unique", "")

        check_path = os.path.join(path, str(last_business_day) + ".csv")

        if os.path.isfile(check_path):

            df = pd.read_csv(os.path.join(path, str(last_business_day) + ".csv"))

            for index, row in df.iterrows():

                ticker = row['Ticker']

                only_ticker = df[df['Ticker'] == ticker]

                filepath = os.path.join(x, (ticker + ".csv"))

                stock = finviz.get_stock(ticker)

                stock['Date'] = str(last_business_day)
                stock['Ticker'] = ticker

                if os.path.isfile(filepath):
                    ticker_df = pd.read_csv(filepath)

                    if not (ticker_df['Date'].str.contains(str(last_business_day)).any()):
                        with open(filepath, 'a') as f:
                            w = csv.DictWriter(f, stock.keys())
                            w.writerow(stock)
                            f.close()

                if not os.path.isfile(filepath):
                    with open(filepath, 'w+') as f:
                        w = csv.DictWriter(f, stock.keys())
                        w.writeheader()
                        w.writerow(stock)
                        f.close()
