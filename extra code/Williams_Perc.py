from ib_insync.contract import Stock
from ib_insync import OptionChain, Option, IB
import pandas as pd
import random
from finviz.screener import Screener
import traceback
import pandas_ta as pta
import os
from datetime import datetime

ib = IB()

ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr

def get_option_data(ticker):

    option_list = []

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

    options = ib.reqTickers(*contracts)

    for option in options:
        volume = option.volume
        if volume > 50:
            option_list.append(option)

    return option_list


stock_list = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o500', 'sh_price_o1', 'ind_exchangetradedfund'], table='Performance', order='price')

# get 2 day data from IB API
for x in stock_list:
    try:

        stock = x['Ticker']

        security = Stock(stock, 'SMART', 'USD')

        ib.qualifyContracts(security)

        options = get_option_data(security)

        for option in options:

            date = option.contract.lastTradeDateOrContractMonth
            right = option.contract.right
            strike = option.contract.strike

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
            market_data['Option Volume'] = option.volume
            market_data['Option Type'] = right
            market_data['Option Expiration'] = date
            market_data['Option Strike'] = strike

            talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

            today = datetime.today().strftime('%Y-%m-%d')

            path = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{today}'

            # Check whether the specified path exists or not
            isExist = os.path.exists(path)

            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            if williams_perc < -90 and talib_rsi < 10 and option.volume > 50:
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{today}\\{stock}.csv'):
                    df = pd.read_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{today}\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{today}\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF\\{today}\\{stock}.csv', index=False)


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

        options = get_option_data(security)

        for option in options:

            date = option.contract.lastTradeDateOrContractMonth
            right = option.contract.right
            strike = option.contract.strike

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
            market_data['Option Volume'] = option.volume
            market_data['Option Type'] = right
            market_data['Option Expiration'] = date
            market_data['Option Strike'] = strike

            today = datetime.today().strftime('%Y-%m-%d')

            path = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{today}'

            # Check whether the specified path exists or not
            isExist = os.path.exists(path)

            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            if williams_perc > -10 and talib_rsi > 90 and option.volume > 50:

                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{today}\\{stock}.csv'):
                    df = pd.read_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{today}\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{today}\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF\\{today}\\{stock}.csv', index=False)


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

        options = get_option_data(security)

        for option in options:

            date = option.contract.lastTradeDateOrContractMonth
            right = option.contract.right
            strike = option.contract.strike

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
            market_data['Option Volume'] = option.volume
            market_data['Option Type'] = right
            market_data['Option Expiration'] = date
            market_data['Option Strike'] = strike

            today = datetime.today().strftime('%Y-%m-%d')

            path = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{today}'

            # Check whether the specified path exists or not
            isExist = os.path.exists(path)

            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            if williams_perc < -90 and talib_rsi < 10 and option.volume > 50:
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{today}\\{stock}.csv'):
                    df = pd.read_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{today}\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{today}\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma\\{today}\\{stock}.csv', index=False)


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

        options = get_option_data(security)

        for option in options:

            date = option.contract.lastTradeDateOrContractMonth
            right = option.contract.right
            strike = option.contract.strike

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
            market_data['Option Volume'] = option.volume
            market_data['Option Type'] = right
            market_data['Option Expiration'] = date
            market_data['Option Strike'] = strike
            
            today = datetime.today().strftime('%Y-%m-%d')

            path = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{today}'

            # Check whether the specified path exists or not
            isExist = os.path.exists(path)

            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            if williams_perc > -10 and talib_rsi > 90 and option.volume > 50:

                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{today}\\{stock}.csv'):
                    df = pd.read_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{today}\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{today}\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma\\{today}\\{stock}.csv', index=False)

    except Exception as err:
        print(err)
