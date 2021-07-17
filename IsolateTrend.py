import numpy as np
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import BDay
from datetime import datetime
import pandas as pd

final_path = "E:\\filtered_df.csv"

path = "E:\\merged CSVs.csv"


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
    columns = ['SMA200', 'SMA50', 'SMA20', 'Open', 'Close', 'Market Cap', 'Change', 'Date', 'Ticker', 'Rel Volume', 'RSI (14)', 'Industry']

    df = pd.read_csv(final_path, usecols=columns)

    # df['Market Cap'] = df['Market Cap'].apply(value_to_float)

    df = df[df.Industry != 'Exchange Traded Fund']
    df = df[df.Industry != 'Shell Companies']

    df = df[df['Date'] == date]
    df = df.replace("-", np.nan)

    df = df[df['Change'].astype(float) > 3]

    df = df[df['SMA200'].astype(float) < df['Close']]
    df = df[df['SMA50'].astype(float) < df['Close']]

    df = df[df['SMA20'].between(df['Open'], df['Close'])]

    df = df[df['Open'].astype(float) < df['Close']]

    # remove % from all specified columns to get the raw value
    df['Change'] = df['Change'].replace({'%':''}, regex=True)

    # df = df[df['Market Cap'].astype(float) < 300000000]

    df['Change'] = df['Change'].fillna(0).astype('float')

    tickers = df['Ticker'].to_list()

    df.to_csv("Results.csv", encoding='utf-8')

    return tickers


def get_next_day(tickers, date):
    columns = ['SMA200', 'SMA50', 'SMA20', 'Open', 'Close', 'Market Cap', 'Change', 'Date', 'Ticker', 'Rel Volume']

    df = pd.read_csv(final_path, usecols=columns)

    df['Market Cap'] = df['Market Cap'].apply(value_to_float)

    df = df[df['Date'] == date]

    boolean_series = df['Ticker'].isin(tickers)
    df = df[boolean_series]

    df.to_csv("Results_two.csv", encoding='utf-8')

    return df['Ticker'].to_list()


first_date = datetime.strptime('2021-06-03', "%Y-%m-%d").date()

winner = 0
loser = 0

winner_sum = 0
loser_sum = 0

date_dup = []

for i in range(40):
    try:
        date_one = str((first_date + relativedelta(days=+i) - BDay(1)).date())
        date_two = str((first_date + relativedelta(days=+i+1) - BDay(1)).date())

        if date_one not in date_two and [date_one, date_two] not in date_dup:

           date_dup.append([date_one, date_two])

           tickers = small_cap_rel_vol(date_one)

           tickers_two = get_next_day(tickers, date_two)

           df = pd.read_csv("Results.csv")
           df_two = pd.read_csv("Results_two.csv")

           close_one = df['Close'].tolist()
           close_two = df_two['Close'].tolist()

           if sum(close_one) < sum(close_two) and sum(close_one) != 0 and sum(close_two) - sum(close_one) < 200:
                winner_sum+=sum(close_two) - sum(close_one)
                winner+=1
           elif sum(close_one) > sum(close_two) and sum(close_one) != 0 and sum(close_one) - sum(close_two) < 200:
               loser_sum+=sum(close_one) - sum(close_two)
               loser+=1

           winners = open("winners2.txt", "a")

           winners.write(str(sum(close_one)) + ", ")
           winners.write(str(sum(close_two)) + "\n")

           winners.close()

           print(str(sum(close_one)), str(sum(close_two)), "(" + str(winner_sum) + ")", "(" + str(loser_sum) + ")",
                 winner, loser, tickers_two, date_one, date_two)

    except Exception as err:
        print(err)
