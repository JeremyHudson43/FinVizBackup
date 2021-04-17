# Find stocks that have between 24 and 28 RSI for last business day, add to text file
import pandas as pd
import glob
import os
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
import datetime
import finviz
import csv
import ctypes

MessageBox = ctypes.windll.user32.MessageBoxW


today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

# loop through low RSI unique folder and add all matching results for previous business day to text file list
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\low rsi\\unique"
cross_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI\\stocks below RSI 30.txt"
cross_path_folder = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\cross above 30 RSI"

df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(folder_path, "*.csv"))))

df = df[df['RSI (14)'].between(24, 28)]

def block_one():
    # add ticker to text file
    file = open(cross_path, "a+")  # append mode

    for index, row in df.iterrows():

        ticker = row['Ticker']

        if ticker.strip() not in file.readlines():
            file.write(ticker.strip() + '\n')

    file.close()

def block_two():
    file = open(cross_path, "r")  # append mode

    for line in file:
        stock = finviz.get_stock(line.strip())

        path = os.path.join(cross_path_folder, line.strip() + ".csv")

        argument = str(line.strip() + " is breaking out with an RSI of " + stock['RSI (14)'])

        if float(stock['RSI (14)']) > 32:
            MessageBox(None, argument, 'RSI Alert', 0)
            with open(path, 'a+') as f:
                w = csv.DictWriter(f, stock.keys())
                w.writeheader()
                w.writerow(stock)
                f.close()

def block_three():
  content = open(cross_path, 'r').readlines()
  content_set = set(content)
  clean_data = open(cross_path, 'w')

  for line in content_set:
      clean_data.write(line)

block_one()
block_two()
block_three()
