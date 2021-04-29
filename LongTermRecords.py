import datetime
from pandas.tseries.offsets import BDay
import finviz
import csv
import pandas as pd
import os

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"
long_term_path = r"C:\Users\Frank Einstein\Desktop\long term records"
list_of_tickers = r"C:\Users\Frank Einstein\Desktop\long term records\list of tickers.txt"

r = []


def block_one():

    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            path = os.path.join(root, name)
            r.append(path)


    for x in r[29:]:

        path = x.replace("unique", "")
        check_path = os.path.join(path, str(last_business_day) + ".csv")

        if os.path.isfile(check_path):

            df = pd.read_csv(os.path.join(path, str(last_business_day) + ".csv"))

            for index, row in df.iterrows():

                ticker = row['Ticker']

                # add ticker to text file
                file = open(list_of_tickers, "a+")  # append mode
                if ticker not in file.readlines():
                    file.write(ticker + '\n')

                file.close()


def block_two():

    # add ticker to text file
    file = open(list_of_tickers, "r")  # append mode

    for line in file.readlines():

        try:

            line = line.strip('\n')

            stock = finviz.get_stock(line)

            first_story = [x[0] for x in finviz.get_news(line.strip())]

            stock['Date'] = str(last_business_day)
            stock['Ticker'] = line

            try:
                stock['News'] = first_story[0]
            except:
                print("error")

            ticker_file = os.path.join(long_term_path, line + ".csv")

            if not os.path.isfile(ticker_file):

                with open(ticker_file, 'w+') as f:
                    w = csv.DictWriter(f, stock.keys())
                    w.writeheader()
                    w.writerow(stock)
                    f.close()
        except:
            print("error")


def block_three():

    for root, dirs, files in os.walk(long_term_path):
        for filename in files:
            if filename.endswith(".csv"):

                replaced_file = filename.replace(".csv", "")

                stock = finviz.get_stock(replaced_file)

                first_story = [x[0] for x in finviz.get_news(replaced_file.strip())]
                stock['Date'] = str(last_business_day)
                stock['Ticker'] = replaced_file

                try:
                    stock['News'] = first_story[0]
                except:
                    print("error")

                ticker_file = os.path.join(long_term_path, filename)

                ticker_df = pd.read_csv(ticker_file, encoding='latin-1')

                if not(ticker_df['Date'].str.contains(str(last_business_day)).any()):

                    with open(ticker_file, 'a') as f:
                        w = csv.DictWriter(f, stock.keys())
                        w.writerow(stock)
                        f.close()


def block_four():
    content = open(list_of_tickers, 'r').readlines()
    content_set = set(content)
    clean_data = open(list_of_tickers, 'w')

    for line in content_set:
        clean_data.write(line)


block_one()
block_two()
block_three()
block_four()
