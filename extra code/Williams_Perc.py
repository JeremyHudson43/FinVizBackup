from ib_insync.contract import Stock
from ib_insync.ib import IB
import pandas as pd
import random
from finviz.screener import Screener

ib = IB()

ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

stock_list = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o500', 'sh_price_o1', 'ind_exchangetradedfund'], table='Performance', order='price')

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr

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

        market_data['Williams %'] = williams_perc

        if williams_perc < -95:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{stock}.csv')

    except Exception as err:
        print(err)

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

        market_data['Williams %'] = williams_perc

        if williams_perc > -5:
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

        market_data['Williams %'] = williams_perc

        if williams_perc < -95:
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

        market_data['Williams %'] = williams_perc

        if williams_perc > -5:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{stock}.csv')

    except Exception as err:
        print(err)
