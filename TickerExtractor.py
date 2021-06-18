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

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        r.append(path)

length = (len(next(os.walk(folder_path))[1]))

for x in r[length:]:

    path = x.replace("unique", "")

    check_path = os.path.join(path, str(last_business_day) + ".csv")

    if os.path.isfile(check_path):

        df = pd.read_csv(os.path.join(path, str(last_business_day) + ".csv"))

        for index, row in df.iterrows():

            try:

                ticker = row['Ticker']

                only_ticker = df[df['Ticker'] == ticker]

                filepath = os.path.join(x, (ticker + ".csv"))

                stock = finviz.get_stock(ticker)

                first_story = [x[0] for x in finviz.get_news(ticker)]

                stock['Date'] = str(last_business_day)
                stock['Ticker'] = ticker

                try:
                    stock['News'] = first_story[0]
                except Exception as e:
                    print(e)

                if os.path.isfile(filepath):
                    ticker_df = pd.read_csv(filepath, encoding='latin-1')

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
            except Exception as e:
                print(e)
