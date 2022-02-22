from ib_insync.contract import Stock
from ib_insync import OptionChain, Option, IB
import pandas as pd
import random
from finviz.screener import Screener
import traceback
import pandas_ta as pta

ib = IB()

ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

stock_list = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o500', 'sh_price_o1', 'ind_exchangetradedfund'], table='Performance', order='price')

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr

def get_option_data(ticker):
    chains = ib.reqSecDefOptParams(ticker.symbol, '', ticker.secType, ticker.conId)

    chain = next(c for c in chains)

    strikes = [strike for strike in chain.strikes]
    expirations = sorted(exp for exp in chain.expirations)[:3]
    rights = ['P', 'C']

    contracts = [Option(ticker.symbol, expiration, strike, right, 'SMART')
                 for right in rights
                 for expiration in expirations
                 for strike in strikes]

    contracts = ib.qualifyContracts(*contracts)

    tickers = ib.reqTickers(*contracts)

    for ticker in tickers:
        volume = ticker.volume
        if volume > 50:
            return volume


# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        security = Stock(stock, 'SMART', 'USD')

        ib.qualifyContracts(security)

        option_volume = get_option_data(security)

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='7 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]

        market_data['Williams %'] = williams_perc

        talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

        print(talib_rsi)

        if option_volume > 50:
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

        ib.qualifyContracts(security)

        option_volume = get_option_data(security)

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='7 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

        market_data['Williams %'] = williams_perc

        if williams_perc > -10 and talib_rsi > 90 and option_volume > 50:
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

        ib.qualifyContracts(security)

        option_volume = get_option_data(security)

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='7 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

        market_data['Williams %'] = williams_perc

        if williams_perc < -90 and talib_rsi < 10 and option_volume > 50:
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

        ib.qualifyContracts(security)
        option_volume = get_option_data(security)

        # Fetching historical data when market is closed for testing purposes
        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                security,
                endDateTime='',
                durationStr='7 D',
                barSizeSetting='1 day',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                timeout=0
            ))

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

        market_data['Williams %'] = williams_perc

        if williams_perc > -10 and talib_rsi > 90 and option_volume > 50:
            market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{stock}.csv')

    except Exception as err:
        print(err)
