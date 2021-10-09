import pandas as pd
import datetime
import os
import yfinance as yf

stocks = open("C:\\Users\\Frank Einstein\\PycharmProjects\\FinVizScraper\\stocks.txt", "r").readlines()

counter  = 0

def percent_func(a, b):
    result = float(b - a) / a * 100.0

    return result

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

for stock_num in range(len(stocks)):
   file = open("C:\\Users\\Frank Einstein\\PycharmProjects\\FinVizScraper\\boring stocks.txt", "a+")
   try:

       import yfinance as yf

       # set start and end dates
       start_date = '2021-09-01'
       end_date = '2021-10-01'

       df = yf.download(stocks[stock_num].strip("\n"), start_date, end_date, period="1d", interval="60m")

       df.to_csv(stocks[stock_num].strip("\n") + ".csv")

       df = pd.read_csv(stocks[stock_num].strip("\n") + ".csv")

       os.remove(stocks[stock_num].strip("\n")+ ".csv")

       # df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stocks[stock_num]).strip("\n") + ".csv")

       # date_one = df['Date'].tolist()[1]
       # date_two = df['Date'].tolist()[-1]

       date_one = '2021-09-01'
       date_two = '2021-10-02'

       print(date_one, date_two)

       # if 3650 * 3 > days_between(date_one, date_two) > 3650:

       print(df['Close'].tolist())

       first = df['Close'].tolist()[1]

       second = df['Close'].tolist()[7]
       third = df['Close'].tolist()[14]

       fourth = df['Close'].tolist()[-1]

       if abs(percent_func(first, second)) < 1 and abs(percent_func(second, third)) < 1 and abs(percent_func(third, fourth)) < 1:

          file.write(stocks[stock_num])
          counter+=1

          print(date_one, date_two)
          print(counter)
          print(stocks[stock_num])

   except Exception as err:
       print(err)



