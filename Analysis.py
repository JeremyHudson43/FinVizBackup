import numpy as np
import pandas as pd
import glob
import functools
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas_datareader as web
import os.path
from pandas.tseries.offsets import BDay

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\combined CSVs\\"

file_list = []


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

    df = df.drop(['Company', 'Sector', 'Industry', 'Country', 'Volatility', 'Optionable', 'Shortable', 'Earnings', 'Date',
                  'Date', 'Ticker', 'News', '52W Range', 'Index'], axis=1)

    # remove % from all specified columns to get the raw value
    df[cols_to_check] = df[cols_to_check].replace({'%':''}, regex=True)
    df = df.replace("-", np.nan)

    df[cols_to_check] = df[cols_to_check].fillna(0).astype('float')
    df[cols_to_check] = df[cols_to_check].fillna(0).astype('int')

    df[cols_to_check].apply(np.floor)

    df = df.mean(axis=0)

    df.to_csv(os.path.join(storage_path, f"{folder}.csv"))


def print_averages():
    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            path = os.path.join(root, name)

            print(path)

            try:
               df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None,  error_bad_lines=False),
                                    glob.glob(path + "\\unique" + "/*.csv")))

               print(df)
               clean_data(df, name)

            except Exception as err:
               print(err)


# print_averages()

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        file_list.append(path)

length = (len(next(os.walk(folder_path))[1]))


def percent(a, b):
    result = float(((b - a) * 100) / a)

    return result


def compare_prices():
    start_date_str = "2021-04-16"
    final_df = pd.DataFrame()

    for x in file_list[length:]:
        path = x.replace("unique", "")
        path = os.path.join(path, f'{start_date_str}.csv')

        if os.path.isfile(path):

            df = pd.read_csv(path)
            tickers = df['Ticker'].tolist()

            print(path)

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

            starting_price = str((start_date - BDay(1)).date())
            weekly = str((start_date + relativedelta(weeks=+1) - BDay(1)).date())
            biweekly = str((start_date + relativedelta(weeks=+2) - BDay(1)).date())
            monthly = str((start_date + relativedelta(months=+1) - BDay(1)).date())
            two_months = str((start_date + relativedelta(months=+2) - BDay(1)).date())

            print(weekly, biweekly, monthly)

            for y in range(len(tickers)):

                try:
                    print("Currently fetching",  f'{tickers[y]}')

                    starting_data = web.get_data_yahoo(tickers[y], starting_price, starting_price)

                    weekly_data = web.get_data_yahoo(tickers[y], weekly, weekly)

                    biweekly_data = web.get_data_yahoo(tickers[y], biweekly, biweekly)

                    monthly_data = web.get_data_yahoo(tickers[y], monthly, monthly)

                    two_month_data = web.get_data_yahoo(tickers[y], two_months, two_months)

                    data = {'Ticker': tickers[y],
                            'Start Date': starting_data["Adj Close"][starting_price],
                            '1 Week': weekly_data["Adj Close"][weekly],
                            '2 weeks': biweekly_data["Adj Close"][biweekly],
                            '1 Month': monthly_data["Adj Close"][monthly],
                            "2 Months": two_month_data["Adj Close"][two_months]
                           }

                    temp_df = pd.DataFrame(data, index=[0])
                    final_df = final_df.append(temp_df)

                except Exception as err:
                    print(err)

            final_df['W_Change'] = percent(final_df['Start Date'].mean(), final_df["1 Week"].mean())
            final_df['2W_Change'] = percent(final_df['Start Date'].mean(), final_df["2 Weeeks"].mean())
            final_df['M_Change'] = percent(final_df['Start Date'].mean(), final_df["1 Month"].mean())
            final_df['2M_Change'] = percent(final_df['Start Date'].mean(), final_df["2 Months"].mean())

            folder_name = x.split("\\")[6]

            save_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\backtest results"

            final_df.to_csv(os.path.join(save_path, folder_name + "_" +
                                         str(start_date)) + "_backtest.csv", index=False)


compare_prices()
