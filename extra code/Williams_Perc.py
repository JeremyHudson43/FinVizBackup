from ib_insync.contract import Stock
from ib_insync.ib import IB
import pandas as pd
import random
from finviz.screener import Screener
import traceback

ib = IB()

ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

stock_list = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o500', 'sh_price_o1', 'ind_exchangetradedfund'], table='Performance', order='price')

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


def rsi_func(df, periods=2, ema=False):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, in_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods).mean()
        ma_down = down.rolling(window=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi

# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        print(stock)

        security = Stock(stock, 'SMART', 'USD')

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='3 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        rsi = rsi_func(market_data, periods=2, ema=False)

        market_data['Williams %'] = williams_perc
        market_data['RSI'] = rsi

        if williams_perc < -90 and rsi < 10:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{stock}.csv')

    except Exception as err:
        print(traceback.format_exc())

stock_list = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o500', 'sh_price_o1', 'ind_exchangetradedfund'], table='Performance', order='price')

# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        print(stock)

        security = Stock(stock, 'SMART', 'USD')

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='3 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        rsi = rsi_func(market_data, periods=2, ema=False)

        market_data['Williams %'] = williams_perc
        market_data['RSI'] = rsi

        if williams_perc > -10 and rsi > 90:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{stock}.csv')

    except Exception as err:
        print(err)

stock_list = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o500', 'sh_price_o1', 'ind_stocksonly'], table='Performance', order='price')

# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        print(stock)

        security = Stock(stock, 'SMART', 'USD')

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='3 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        rsi = rsi_func(market_data, periods=2, ema=False)

        market_data['Williams %'] = williams_perc
        market_data['RSI'] = rsi

        if williams_perc < -90 and rsi < 10:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{stock}.csv')

    except Exception as err:
        print(err)

stock_list = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o500', 'sh_price_o1', 'ind_stocksonly'], table='Performance', order='price')

# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        print(stock)

        security = Stock(stock, 'SMART', 'USD')

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='3 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        rsi = rsi_func(market_data, periods=2, ema=False)

        market_data['Williams %'] = williams_perc
        market_data['RSI'] = rsi

        if williams_perc > -10 and rsi > 90:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{stock}.csv')

    except Exception as err:
        print(err)
