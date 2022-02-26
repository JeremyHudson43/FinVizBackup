from ib_insync.contract import Stock
from ib_insync import OptionChain, Option, IB
import pandas as pd
import random
from finviz.screener import Screener
import traceback
import pandas_ta as pta
import os
from datetime import datetime, timedelta
import finviz
import time
import functools
import glob



def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        if len(x) > 1:
            return float(x.replace('B', '')) * 1000000000
        return 1000000000.0
    if 'T' in x:
        if len(x) > 1:
            return float(x.replace('T', '')) * 1000000000000
        return 1000000000000000.0

    return 0.0


def get_option_data(ticker, price, ib):
    option_list = []

    chains = ib.reqSecDefOptParams(ticker.symbol, '', ticker.secType, ticker.conId)
    chain = next(c for c in chains)

    strikes = [strike for strike in chain.strikes if get_change(price, strike) < 25]

    expirations = sorted(exp for exp in chain.expirations if
                         (datetime.strptime(exp, '%Y%m%d') - datetime.now()).days < 90)

    rights = ['P', 'C']

    contracts_list = []

    for strike in strikes:
        ib.sleep(1)
        for expiration in expirations:
            for right in rights:
                contract = Option(ticker.symbol, expiration, strike, right, 'SMART')
                contracts_list.append(contract)

    contracts = ib.qualifyContracts(*contracts_list)
    options = ib.reqTickers(*contracts)

    for option in options:
        volume = option.volume

        if volume > 100:
            option_list.append(option)

            for strike in strikes:
                print(ticker.symbol, strike, price, volume)

    return option_list


def iterate(stock_list, path, williams_val, rsi_val):

    ib = IB()

    ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

    today = datetime.today().strftime('%Y-%m-%d')
    path = f'{path}\\{today}'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)

    # get 2 day data from IB API
    for ticker in stock_list:
        try:

            avg_vol = value_to_float(ticker['Avg Volume'])
            stock = ticker['Ticker']

            if avg_vol > 5000000:

                f = open(f"{path}\\checked.txt", "a+")
                f.close()

                checked_stocks = open(f"{path}\\checked.txt", "r").readlines()
                checked_stocks = [x.strip() for x in checked_stocks]

                print(checked_stocks)

                if stock not in checked_stocks:

                    f = open(f"{path}\\checked.txt", "a+")
                    f.write(stock + '\n')
                    f.close()

                    security = Stock(stock, 'SMART', 'USD')
                    ib.qualifyContracts(security)

                    [ticker_close] = ib.reqTickers(security)
                    price = ticker_close.marketPrice()

                    options = get_option_data(security, price, ib)

                    if len(options) > 0:

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

                            williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[
                                -1]
                            talib_rsi = pta.rsi(market_data['close'], length=2).iloc[-1]

                            print(williams_perc, talib_rsi)

                            market_data['Ticker'] = stock
                            market_data['RSI (2)'] = talib_rsi
                            market_data['Williams % (2)'] = williams_perc
                            market_data['Option Volume'] = option.volume
                            market_data['Option Type'] = right
                            market_data['Option Expiration'] = date
                            market_data['Option Strike'] = strike

                            if williams_val == -85 and right == 'C':

                                if williams_perc < williams_val or talib_rsi < rsi_val:
                                    # append to dataframe if it exists, else create new dataframe
                                    if os.path.isfile(f'{path}\\{stock}.csv'):
                                        df = pd.read_csv(f'{path}\\{stock}.csv')
                                        df = df.append(market_data)
                                        df.to_csv(f'{path}\\{stock}.csv', index=False)
                                    else:
                                        market_data.to_csv(f'{path}\\{stock}.csv', index=False)

                            elif williams_val == -15 and right == 'P':

                                if williams_perc > williams_val or talib_rsi > rsi_val:
                                    # append to dataframe if it exists, else create new dataframe
                                    if os.path.isfile(f'{path}\\{stock}.csv'):
                                        df = pd.read_csv(f'{path}\\{stock}.csv')
                                        df = df.append(market_data)
                                        df.to_csv(f'{path}\\{stock}.csv', index=False)
                                    else:
                                        market_data.to_csv(f'{path}\\{stock}.csv', index=False)

        except Exception as err:
            print(traceback.format_exc())

    try:

        df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None, error_bad_lines=False),
                           glob.glob(path + "/*.csv")))
        df.to_csv(f'{path}\\combined.csv', index=False)

    except Exception as err:
        print(traceback.format_exc())


path_one = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma_ETF'
path_two = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma_ETF'
path_three = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\above_ma'
path_four = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\below_ma'

williams_one = -85
williams_two = -15

rsi_one = 15
rsi_two = 85

stock_list_one = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o2000', 'sh_price_o1', 'ind_exchangetradedfund'],
                          table='Performance', order='price')
iterate(stock_list_one, path_one, williams_one, rsi_one)

stock_list_two = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o2000', 'sh_price_o1', 'ind_exchangetradedfund'],
                          table='Performance', order='price')
iterate(stock_list_two, path_two, williams_two, rsi_two)

stock_list_three = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o2000', 'sh_price_o1', 'ind_stocksonly'],
                            table='Performance', order='price')
iterate(stock_list_three, path_three, williams_one, rsi_one)

stock_list_four = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o2000', 'sh_price_o1', 'ind_stocksonly'],
                           table='Performance', order='price')
iterate(stock_list_four, path_four, williams_two, rsi_two)
