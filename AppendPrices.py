import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from datetime import datetime

stock = "GPL"

sma_200_list = []
sma_20_list = []
sma_50_list = []


stock_to_save = yf.Ticker(stock)

df_one = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock records\\all stocks\\unique\\" + stock + ".csv")

dates = df_one['Date'].tolist()

start_date_one = datetime.strptime(dates[0], "%Y-%m-%d").date()
start_date_two = datetime.strptime(dates[-1], "%Y-%m-%d").date()

# get historical market data
hist_one = stock_to_save.history(start=dates[0], end=start_date_two + relativedelta(days=+2))

# get historical market data
hist_two = stock_to_save.history(start=start_date_two - relativedelta(months=+12), end=dates[-1])


for date_index in range(len(hist_one)):
    sma_200 = hist_two['Close'].tolist()[-200 - date_index:]
    sma_200 = sum(sma_200) / len(sma_200)
    sma_200_list.append(sma_200)

    sma_20 = hist_two['Close'].tolist()[-20 - date_index:]
    sma_20 = sum(sma_20) / len(sma_20)
    sma_20_list.append(sma_20)

    sma_50 = hist_two['Close'].tolist()[-50- date_index :]
    sma_50 = sum(sma_50) / len(sma_50)
    sma_50_list.append(sma_50)

    print(sma_200, sma_50, sma_20)

sma_20_list.reverse()
sma_50_list.reverse()
sma_200_list.reverse()


df_one['SMA20'] = pd.Series(sma_20_list)
df_one['SMA50'] = pd.Series(sma_50_list)
df_one['SMA200'] = pd.Series(sma_200_list)

dates = df_one['Date'].tolist()


hist_close = [x for x in hist_one['Close']]
hist_open = [x for x in hist_one['Open']]

hist_low = [x for x in hist_one['Low']]
hist_high = [x for x in hist_one['High']]


df_one['Close'] = pd.Series(hist_close)
df_one['Open'] = pd.Series(hist_open)
df_one['Low'] = pd.Series(hist_low)
df_one['High'] = pd.Series(hist_high)


df_one = df_one.drop_duplicates(subset=['Date'])



df_one.to_csv("test.csv")
