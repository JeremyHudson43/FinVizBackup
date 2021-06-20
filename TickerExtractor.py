import pandas as pd
import os
import finviz
import datetime
from pandas.tseries.offsets import BDay

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

file_list = []

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        file_list.append(path)

length = (len(next(os.walk(folder_path))[1]))

for unique_path in file_list[length:]:

    path = unique_path.replace("unique", "")

    csv_path = os.path.join(path, f"{last_business_day}.csv")

    if os.path.isfile(csv_path):

        df = pd.read_csv(csv_path)

        for index, row in df.iterrows():

            try:

                ticker = row['Ticker']

                print(f"Writing Ticker {ticker} to {unique_path}")

                only_ticker = df[df['Ticker'] == ticker]

                filepath = os.path.join(unique_path, f"{ticker}.csv")

                stock = finviz.get_stock(ticker)

                first_story = [x[0] for x in finviz.get_news(ticker)]

                stock['Date'] = str(last_business_day)
                stock['Ticker'] = ticker

                try:
                    stock['News'] = first_story[0]
                except Exception as e:
                    print(e)

                with open(filepath, 'a+') as f:

                    if os.stat(filepath).st_size != 0:
                        ticker_df = pd.read_csv(filepath, encoding='latin-1')
                        ticker_df = ticker_df.append(stock, ignore_index = True)
                    else:
                        ticker_df = pd.DataFrame(stock, index = [0])

                    ticker_df = ticker_df.drop_duplicates(keep=False)

                    ticker_df.to_csv(f, mode='a', header=f.tell() == 0, index = False)

            except Exception as e:
                print(e)