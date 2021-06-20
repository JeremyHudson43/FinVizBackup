import pandas as pd
import glob
import os
from pandas.tseries.offsets import BDay
import datetime
import finviz
import ctypes
import functools

MessageBox = ctypes.windll.user32.MessageBoxW

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

# loop through low RSI unique folder and add all matching results for previous business day to text file list
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\low rsi\\unique"
cross_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI\\stocks below RSI 30.txt"
cross_path_folder = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI\\unique"

df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None,  error_bad_lines=False),
                    glob.glob(folder_path + "/*.csv")))

last_business_day = last_business_day.strftime("%m/%d/%Y")


df = df[df['RSI (14)'].between(24, 28)]

df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] == last_business_day]


def add_low_rsi_to_txt_file():
    # add ticker to text file
    file = open(cross_path, "a+")

    for index, row in df.iterrows():
        ticker = row['Ticker']
        file.write(ticker.strip() + '\n')

    file.close()


def check_for_breakout():
    file = open(cross_path, "r").readlines()

    for line in file:
        try:
            stock = finviz.get_stock(line.strip())

            first_story = [x[0] for x in finviz.get_news(line.strip())]

            stock['Date'] = str(last_business_day)
            stock['Ticker'] = line.strip()

            try:
                stock['News'] = first_story[0]
            except Exception as err:
                print(err)

            filepath = os.path.join(cross_path_folder, line.strip() + ".csv")

            argument = str(line.strip() + " is breaking out with an RSI of " + stock['RSI (14)'])

            if float(stock['RSI (14)']) > 30:
                MessageBox(None, argument, 'RSI Alert', 0)
                file.remove(line)

                with open(cross_path, 'w') as f:
                    f.writelines(file)
                    f.close()

                with open(filepath, 'a+') as f:

                    if os.stat(filepath).st_size != 0:
                        ticker_df = pd.read_csv(filepath, encoding='latin-1')
                        ticker_df = ticker_df.append(stock, ignore_index=True)
                    else:
                        ticker_df = pd.DataFrame(stock, index=[0])

                    ticker_df = ticker_df.drop_duplicates(keep=False)

                    ticker_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

        except Exception as err:
            print(err)


def remove_duplicates():
    content = open(cross_path, 'r').readlines()
    content_set = set(content)
    clean_data = open(cross_path, 'w')

    for line in content_set:
        clean_data.write(line)


add_low_rsi_to_txt_file()
check_for_breakout()
remove_duplicates()
