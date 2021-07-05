import pandas as pd
import datetime

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
       df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stocks[stock_num]).strip("\n") + ".csv")

       date_one = df['Date'].tolist()[1]
       date_two = df['Date'].tolist()[-1]

       print(date_one, date_two)

       if days_between(date_one, date_two) > 3650 * 2:

           first = df['Close'].tolist()[1]
           last = df['Close'].tolist()[-1]

           if abs(percent_func(first, last)) < 10:

              file.write(stocks[stock_num])

              counter+=1
              print(first, last)
              print(counter)
              print(stocks[stock_num])
   except Exception as err:
       print(err)



