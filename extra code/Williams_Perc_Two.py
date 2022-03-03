from ib_insync.contract import Stock
from ib_insync import OptionChain, Option, IB
import pandas as pd
import random
from finviz.screener import Screener
import traceback
import pandas_ta as pta
import os
from datetime import datetime
import functools
import glob


def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


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


def iterate(stock_list, path, williams_val, rsi_val, call_put, ETF):

    ib = IB()

    ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

    # get 2 day data from IB API
    for ticker in stock_list:
        try:

            avg_vol = value_to_float(ticker['Avg Volume'])
            stock = ticker['Ticker']

            security = Stock(stock, 'SMART', 'USD')
            ib.qualifyContracts(security)

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

            market_data = market_data.iloc[-1:]

            print(stock, williams_perc, talib_rsi)

            market_data['Ticker'] = stock
            market_data['RSI (2)'] = talib_rsi
            market_data['Williams % (2)'] = williams_perc
            market_data['Avg Volume'] = avg_vol
            market_data['Call/Put'] = call_put
            market_data["ETF"] = ETF

            if talib_rsi <= rsi_val and call_put == 'call':
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'{path}\\both\\{stock}.csv'):
                    df = pd.read_csv(f'{path}\\both\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'{path}\\both\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'{path}\\both\\{stock}.csv', index=False)

            elif talib_rsi >= rsi_val and call_put == 'put':
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'{path}\\both\\{stock}.csv'):
                    df = pd.read_csv(f'{path}\\both\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'{path}\\both\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'{path}\\both\\{stock}.csv', index=False)

            if williams_perc <= williams_val and call_put == 'call':
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'{path}\\both\\{stock}.csv'):
                    df = pd.read_csv(f'{path}\\both\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'{path}\\both\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'{path}\\both\\{stock}.csv', index=False)

            elif williams_perc >= williams_val and call_put == 'put':
                # append to dataframe if it exists, else create new dataframe
                if os.path.isfile(f'{path}\\both\\{stock}.csv'):
                    df = pd.read_csv(f'{path}\\both\\{stock}.csv')
                    df = df.append(market_data)
                    df.to_csv(f'{path}\\both\\{stock}.csv', index=False)
                else:
                    market_data.to_csv(f'{path}\\both\\{stock}.csv', index=False)

        except Exception as err:
            print(traceback.format_exc())

    ib.disconnect()


path = f'C:\\Users\\Frank Einstein\\PycharmProjects\\Williams_Alert\\results'

today = datetime.today().strftime('%Y-%m-%d')
path = f'{path}\\{today}'

# Check whether the specified path exists or not
isExist = os.path.exists(path)

if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)

both = f'{path}\\both'

os.mkdir(both)

williams_one = -90
williams_two = -10

rsi_one = 10
rsi_two = 90

stock_list_one = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o1000', 'sh_price_o1', 'ind_exchangetradedfund',
                                   'sh_opt_option', 'ipodate_more1'],
                           table='Performance', order='price')
iterate(stock_list_one, path, williams_one, rsi_one, 'call', True)

stock_list_two = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o1000', 'sh_price_o1', 'ind_exchangetradedfund',
                                   'sh_opt_option', 'ipodate_more1'],
                           table='Performance', order='price')
iterate(stock_list_two, path, williams_two, rsi_two, 'put', True)

stock_list_three = Screener(filters=['ta_sma200_pa', 'sh_avgvol_o1000', 'sh_price_o1', 'ind_stocksonly',
                                     'sh_opt_option', 'ipodate_more1'],
                             table='Performance', order='price')
iterate(stock_list_three, path, williams_one, rsi_one, 'call', False)

stock_list_four = Screener(filters=['ta_sma200_pb', 'sh_avgvol_o1000', 'sh_price_o1', 'ind_stocksonly',
                                    'sh_opt_option', 'ipodate_more1'],
                            table='Performance', order='price')
iterate(stock_list_four, path, williams_two, rsi_two, 'put', False)

try:

    df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None, error_bad_lines=False),
                       glob.glob(both + "/*.csv")))
    df = df.drop_duplicates(subset=['Ticker'])
    df.to_csv(f'{path}\\combined_both.csv', index=False)

except Exception as err:
    print(traceback.format_exc())
