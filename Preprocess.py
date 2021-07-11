import numpy as np
import os
import os.path
import functools
import pandas as pd
import glob

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs"

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        if len(x) > 1:
            return float(x.replace('B', '')) * 1000000000
        return 1000000000.0
    if 'T' in x:
        if len(x) > 1:
            return float(x.replace('T', '')) * 1000000000000
        return 1000000000000000.0

    return 0.0


def clean_data(df, folder):
    # convert all numbers formatted with letters to float value
    df['Market Cap'] = df['Market Cap'].apply(value_to_float)

    df['Shs Outstand'] = df['Shs Outstand'].apply(value_to_float)

    df['Shs Float'] = df['Shs Float'].apply(value_to_float)

    df['Sales'] = df['Sales'].apply(value_to_float)

    df['Avg Volume'] = df['Avg Volume'].apply(value_to_float)

    df['Income'] = df['Income'].apply(value_to_float)

    cols_to_check = ['Insider Own','Perf Week', 'EPS (ttm)', 'EPS next Y', 'EPS next Q', 'Insider Trans', 'Perf Month', 'Inst Own',
                     'Short Float', 'Perf Quarter', 'EPS this Y', 'Inst Trans', 'Perf Half Y', 'ROA', 'Perf Year',
                     'EPS next 5Y', 'ROE', 'Perf YTD', 'EPS past 5Y', 'ROI', '52W High', 'Dividend %', 'Sales past 5Y',
                     'Gross Margin', '52W Low', 'Sales Q/Q', 'Oper. Margin', 'EPS Q/Q', 'Profit Margin', 'SMA20', 'SMA50',
                     'SMA200', 'Change', 'Target Price', 'P/S', 'Short Ratio', 'Book/sh', 'Cash/sh', 'P/C', 'Dividend',
                     'P/FCF', 'Beta', 'Quick Ratio', 'ATR', 'Current Ratio', 'Price', 'Recom', 'P/E', 'RSI (14)', 'Forward P/E']

    df = df.drop(['Company', 'Sector', 'Industry', 'Country', 'Volatility', 'Optionable', 'Shortable', 'Date', 'Earnings', 'News', '52W Range', 'Index'], axis=1)

    # remove % from all specified columns to get the raw value
    df[cols_to_check] = df[cols_to_check].replace({'%':''}, regex=True)
    df = df.replace("-", np.nan)

    df[cols_to_check] = df[cols_to_check].fillna(0).astype('float')
    df[cols_to_check] = df[cols_to_check].fillna(0).astype('int')

    df[cols_to_check].apply(np.floor)

    df.to_csv(os.path.join(storage_path, f"{folder}.csv"))


file_list = []

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        file_list.append(path)

length = (len(next(os.walk(folder_path))[1]))

# extract tickers from scraped mass CSVs to generate individual stock CSVs
for unique_path in file_list[length:]:

    print(unique_path)

    try:
        df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None, error_bad_lines=False),
                           glob.glob(unique_path  + "/*.csv")))
    except Exception as err:
        print(err)

    if "unique" in unique_path:
        to_save = unique_path.split("\\")[-2]
        clean_data(df, to_save)
