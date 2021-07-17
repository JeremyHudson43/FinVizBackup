import pandas as pd
import functools
import glob
import numpy as np
import os
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import BDay
from datetime import datetime

final_path = "C:\\Users\\Frank Einstein\\Desktop\\all_combined.csv"



def forte_capital():
    df = pd.read_csv(final_path)

    df = df[df['Change'] > 0]
    df = df[df['SMA20'] > 0]
    df = df[df['SMA50'] > 0]
    df = df[df['SMA200'] > 0]
    df = df[df['Avg Volume'] > 500000]
    df = df[df['Short Float'] >= 5]
    df = df[df['Date'] == '2021-04-23']

    df.to_csv("Forte.csv")

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

def small_cap_rel_vol(date):
    df = pd.read_csv(final_path)
    df = df[df['Date'] == date]
    df = df.replace("-", np.nan)

    df = df[df['Rel Volume'].astype(float) > 2]
    df = df[df['SMA200'] < df['Close']]
    df = df[df['SMA50'] < df['Close']]
    df = df[df['Open'] < df['Close']]
    # df = df[df['SMA50'].between(df['Open'], df['Close'])]
    df = df[df['SMA20'].between(df['Open'], df['Close'])]

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

    df = df.drop(['Company', 'Sector', 'Industry', 'Country', 'Volatility', 'Optionable', 'Shortable',  'Earnings', 'News', '52W Range', 'Index'], axis=1)

    df = df[df['Market Cap'] < 2000000000]

    tickers = df['Ticker'].to_list()

    # remove % from all specified columns to get the raw value
    df[cols_to_check] = df[cols_to_check].replace({'%':''}, regex=True)

    df[cols_to_check] = df[cols_to_check].fillna(0).astype('float')

    df[cols_to_check].apply(np.floor)

    df.to_csv("Results.csv", encoding='utf-8')

    return tickers


def get_next_day(tickers, date):
    df = pd.read_csv(final_path)

    df = df[df['Date'] == date]

    boolean_series = df['Ticker'].isin(tickers)
    df = df[boolean_series]

    df = df.replace("-", np.nan)

    # convert all numbers formatted with letters to float value
    df['Market Cap'] = df['Market Cap'].apply(value_to_float)

    df['Shs Outstand'] = df['Shs Outstand'].apply(value_to_float)

    df['Shs Float'] = df['Shs Float'].apply(value_to_float)

    df['Sales'] = df['Sales'].apply(value_to_float)

    df['Avg Volume'] = df['Avg Volume'].apply(value_to_float)

    df['Income'] = df['Income'].apply(value_to_float)

    cols_to_check = ['Insider Own', 'Perf Week', 'EPS (ttm)', 'EPS next Y', 'EPS next Q', 'Insider Trans', 'Perf Month',
                     'Inst Own',
                     'Short Float', 'Perf Quarter', 'EPS this Y', 'Inst Trans', 'Perf Half Y', 'ROA', 'Perf Year',
                     'EPS next 5Y', 'ROE', 'Perf YTD', 'EPS past 5Y', 'ROI', '52W High', 'Dividend %', 'Sales past 5Y',
                     'Gross Margin', '52W Low', 'Sales Q/Q', 'Oper. Margin', 'EPS Q/Q', 'Profit Margin', 'SMA20',
                     'SMA50',
                     'SMA200', 'Change', 'Target Price', 'P/S', 'Short Ratio', 'Book/sh', 'Cash/sh', 'P/C', 'Dividend',
                     'P/FCF', 'Beta', 'Quick Ratio', 'ATR', 'Current Ratio', 'Price', 'Recom', 'P/E', 'RSI (14)',
                     'Forward P/E']

    df = df.drop(
        ['Company', 'Sector', 'Industry', 'Country', 'Volatility', 'Optionable', 'Shortable', 'Earnings', 'News',
         '52W Range', 'Index'], axis=1)

    # remove % from all specified columns to get the raw value
    df[cols_to_check] = df[cols_to_check].replace({'%': ''}, regex=True)

    df[cols_to_check] = df[cols_to_check].fillna(0).astype('float')

    df[cols_to_check].apply(np.floor)

    df.to_csv("Results_two.csv", encoding='utf-8')


first_date = datetime.strptime('2021-06-02', "%Y-%m-%d").date()
second_date = datetime.strptime('2021-06-08', "%Y-%m-%d").date()

for i in range(40):
    try:
        date_one = str((first_date + relativedelta(days=+1) - BDay(1)).date())
        date_two = str((second_date + relativedelta(days=+1) - BDay(1)).date())

        tickers = small_cap_rel_vol(date_one)
        get_next_day(tickers, date_two)

        df = pd.read_csv("Results.csv")
        df_two = pd.read_csv("Results_two.csv")

        close_one = df['Close'].tolist()
        close_two = df_two['Close'].tolist()

        winners = open("winners.txt", "a")

        winners.write("\n" + str(sum(close_one)) + ", ")
        winners.write(str(sum(close_two)) + "\n")
    except Exception as err:
        print(err)

