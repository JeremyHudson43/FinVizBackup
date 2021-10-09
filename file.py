import pandas as pd
import pandas as pd
import glob
import numpy as np
import os
from pandas.tseries.offsets import BDay
import datetime
import finviz
import ctypes
import functools
import os.path

# final_path = "C:\\Users\\Frank Einstein\\Desktop\\all_filtered.csv"
# final_path = "E:\\filtered long term.csv"

path = "C:\\Users\\Frank Einstein\\Desktop\\all_stocks.csv"
final_path = "E:\\stock records\\insider"

# final_path = "E:\\stock stuff\\long term records"

# loop through low RSI unique folder and add all matching results for previous business day to text file list
# folder_path = "E:\\stock records\\low rsi\\unique"
# cross_path = "E:\\stock records\\cross above 30 RSI\\stocks below RSI 30.txt"
# cross_path_folder = "E:\\stock records\\cross above 30 RSI\\unique"

df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None,  error_bad_lines=False),
                    glob.glob(final_path+ "/*.csv")))

df = df[df.Transaction == 'Buy']

tickers = df['Ticker'].to_list()

for ticker in tickers:
    df_single_ticker = df[df.Ticker == ticker]

    column_values = df_single_ticker[["Relationship"]].values.ravel()
    unique_values = pd.unique(column_values)

    if len(unique_values) > 1:
        print(unique_values)


# df = df.drop(['News'], axis=1)

# df = pd.read_csv(final_path)

# df = df[df['ATR'].astype('float') > 5]

# df['Insider Own'] = df['Insider Own'].replace({'%':''}, regex=True)
# df = df.replace("-", np.nan)
# df['Insider Own'] = df['Insider Own'].replace({'-':''}, regex=True)
# df['SMA20'] = df['SMA20'].replace({'%':''}, regex=True)
# df['SMA50'] = df['SMA50'].replace({'%':''}, regex=True)

# df['Change'] = df['Change'].replace({'%':''}, regex=True)

# df = df[df['Sector'] != 'Shell Companies']
# df = df[df['Sector'] != 'Exchange Traded Fund']
# df = df[df['Industry'] != 'Biotechnology']
# df = df[df['Sector'] != 'Financial']
# df = df[df['Sector'] != 'Real Estate']


# df = df[df['Insider Own'].astype('float') > 10]

# df = df[df['Perf Year'].astype('float') >= 50]

# df = df[df['SMA200'].astype('float') > 0]
# df = df[df['SMA50'].astype('float') > 0]
# df = df[df['SMA20'].astype('float') > 0]


df.to_csv(path)
