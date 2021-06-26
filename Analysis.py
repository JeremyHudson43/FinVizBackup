import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas_datareader as web
import os.path
from pandas.tseries.offsets import BDay
from Preprocess import *

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\combined CSVs\\"

file_list = []


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
                            '2 Weeks': biweekly_data["Adj Close"][biweekly],
                            '1 Month': monthly_data["Adj Close"][monthly],
                            "2 Months": two_month_data["Adj Close"][two_months]
                           }

                    temp_df = pd.DataFrame(data, index=[0])
                    final_df = final_df.append(temp_df)

                except Exception as err:
                    print(err)

            final_df['W_Change'] = percent(final_df['Start Date'].mean(), final_df["1 Week"].mean())
            final_df['2W_Change'] = percent(final_df['Start Date'].mean(), final_df["2 Weeks"].mean())
            final_df['M_Change'] = percent(final_df['Start Date'].mean(), final_df["1 Month"].mean())
            final_df['2M_Change'] = percent(final_df['Start Date'].mean(), final_df["2 Months"].mean())

            folder_name = x.split("\\")[6]

            save_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\backtest results"

            final_df.to_csv(os.path.join(save_path, folder_name + "_" +
                                         str(start_date)) + "_backtest.csv", index=False)


compare_prices()
