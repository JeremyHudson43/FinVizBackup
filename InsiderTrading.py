import pandas as pd
import finviz
import datetime
from pandas.tseries.offsets import BDay
import os.path
from finviz.screener import Screener

file_list = []

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

unique_path = 'E:\\stock records\\insider'

filters = []
stock_list = Screener(filters=filters, table='Performance', order='price')

for stock in stock_list:

    try:

        ticker = stock['Ticker']

        filepath = os.path.join(unique_path, f"{ticker}.csv")

        stock = finviz.get_stock(ticker)

        insider = finviz.get_insider(ticker)[0]
        insider['Ticker'] = ticker

        print(f"Writing Insider {ticker} to {unique_path}")

        # appends new stock data to CSV if it exists, else create CSV
        if os.path.isfile(filepath):
           ticker_df = pd.read_csv(filepath, encoding='latin-1', error_bad_lines=False)
           ticker_df = ticker_df.append(insider, ignore_index=True)

        else:
           ticker_df = pd.DataFrame(insider, index=[0])

        ticker_df = ticker_df.drop_duplicates(subset=['Date'])
        ticker_df.to_csv(filepath, index=False, mode='w+')

    except Exception as e:
        print(e)
