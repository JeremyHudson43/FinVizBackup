from ib_insync import *
import random
from datetime import *
import time
import pandas as pd
import pandas_ta as pta
import talib

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


ticker_contract = Stock('EWA', 'SMART', 'USD')

market_data = pd.DataFrame(
    ib.reqHistoricalData(
        ticker_contract,
        endDateTime='',
        durationStr='15 Y',
        barSizeSetting='1 week',
        whatToShow="TRADES",
        formatDate=1,
        useRTH=True,
        timeout=0
    ))

# market_data.to_csv('SPY_historical_data.csv')
# market_data = pd.read_csv('SPY_historical_data.csv')

talib_rsi = pta.rsi(market_data['close'], length=2)
williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2)
market_data['Williams % (2)'] = williams_perc
market_data['RSI (2)'] = talib_rsi

market_data['Change'] = ((market_data.close - market_data.open) / market_data.close * 100)
market_data['Change'] = market_data['Change'].shift(-1)

market_data['SMA (200)'] = talib.SMA(market_data['close'], timeperiod=200)

williams_list = market_data['Williams % (2)'].to_list()
rsi_list = market_data['RSI (2)'].to_list()
change_list = market_data['Change'].to_list()
sma_list = market_data['SMA (200)'].to_list()
close_list = market_data['close'].to_list()
high_list = market_data['high'].to_list()
open_list = market_data['open'].to_list()

win_list_williams = []
win_list_rsi = []
both = []

final = []

for william, rsi, change, sma, close in zip(williams_list, rsi_list, change_list, sma_list, close_list):
    if william <= -90 and change >= 0 and close >= sma:
        win_list_williams.append('Next Day Green Bull')
    elif william <= -90 and change <= 0 and close >= sma:
        win_list_williams.append('Next Day Red Bull')
    elif william >= -10 and change <= 0 and close <= sma:
        win_list_williams.append('Next Day Green Bear')
    elif william >= -10 and change >= 0 and close <= sma:
        win_list_williams.append('Next Day Red Bear')
    else:
        win_list_williams.append('Criteria Not met')


market_data['Win_williams'] = win_list_williams
print(market_data['Win_williams'].value_counts())
# market_data = market_data[market_data['Win_williams'] != 'Criteria Not met']

market_data.to_csv('C:\\Users\\Frank Einstein\\Desktop\\SPY_Williams_Backtest.csv')

