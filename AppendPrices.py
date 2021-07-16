import pandas as pd
import yfinance as yf

stock = "GPL"

df_one = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock records\\all stocks\\unique\\" + stock + ".csv")

df_two = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock history\\" + str(stock) + ".csv")

sma_200 = df_two['Close'].tolist()[-200:]
sma_200 = sum(sma_200) / len(sma_200)

sma_20 = df_two['Close'].tolist()[-20:]
sma_20 = sum(sma_20) / len(sma_20)

sma_50 = df_two['Close'].tolist()[-50:]
sma_50 = sum(sma_50) / len(sma_50)


stock_to_save = yf.Ticker(stock)

dates = df_one['Date'].tolist()

# get historical market data
hist = stock_to_save.history(start=dates[0], end=dates[-1])

hist_close = [x for x in hist['Close']]
hist_open = [x for x in hist['Open']]

hist_low = [x for x in hist['Low']]
hist_high = [x for x in hist['High']]


df_one['Close'] = pd.Series(hist_close)
df_one['Open'] = pd.Series(hist_open)
df_one['Low'] = pd.Series(hist_low)
df_one['High'] = pd.Series(hist_high)

df_one = df_one.drop_duplicates(subset=['Date'])



df_one.to_csv("test.csv")
