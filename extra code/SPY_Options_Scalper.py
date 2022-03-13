from ib_insync import *
import random
from datetime import *
import time
import pandas as pd
from dateutil import parser
import sys
import talib

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))


def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr

def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:40").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)


def sell_stock(ib, ticker):

   ib.reqGlobalCancel()

   qty = [v for v in ib.positions() if v.contract.secType == 'OPT' and v.contract.symbol == 'SPY'][0].position

   if qty > 0:

       order = Order(orderId=27, action='Sell', orderType='MKT', totalQuantity=qty)

       ib.placeOrder(ticker, order)

       print('\nSold ' + str(ticker) + " at the end of the day!")

       time.sleep(10)

       sys.exit(0)


def place_order(call, put, qty):

    extreme_value = False

    while not extreme_value:

        ticker_contract = Stock('SPY', 'SMART', 'USD')

        if not extreme_value:
            timeToSleep = (5*60 - time.time() % (5*60))

            print("Sleeping for " + str(timeToSleep) + " seconds")
            time.sleep(timeToSleep)

        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                ticker_contract,
                endDateTime='',
                durationStr='7 D',
                barSizeSetting='5 mins',
                whatToShow="TRADES",
                formatDate=1,
                useRTH=True,
                timeout=0
            ))

        twenty_one_ema = talib.EMA(market_data['close'].values, timeperiod=21).iloc[-2]
        eight_ema = talib.EMA(market_data['close'].values, timeperiod=8).iloc[-2]
        ten_ema = talib.EMA(market_data['close'].values, timeperiod=10).iloc[-2]
        one_hundred_ema = talib.EMA(market_data['close'].values, timeperiod=100).iloc[-2]
        two_hundred_sma = talib.SMA(market_data['close'].values, timeperiod=200).iloc[-2]

        last_close = market_data['close'].iloc[-2]

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-2]
        market_data['SMA'] = talib.SMA(market_data['close'], timeperiod=200)

        market_data['williams_perc'] = get_wr(market_data['high'], market_data['low'], market_data['close'], 2)

        market_data.to_csv('C:\\Users\\Frank Einstein\\Desktop\\results\\market_data.csv')

        print("\nLast Close: " + str(last_close) + '\n')
        print("Williams %: " + str(williams_perc) + '\n')
        print("200 SMA: " + str(two_hundred_sma) + '\n')
        print('200 EMA: ' + str(one_hundred_ema) + '\n')
        print("21 EMA: " + str(twenty_one_ema) + '\n')
        print("8 EMA: " + str(eight_ema) + '\n')
        print("10 EMA: " + str(ten_ema) + '\n')
        print('- - - - - - - - - - - - - - - - - - - - \n')

        if williams_perc <= -85 and twenty_one_ema < eight_ema \
                and last_close > one_hundred_ema and last_close > two_hundred_sma\
                and last_close > eight_ema:
            extreme_value = True
            contract = call

        elif williams_perc >= -15 and twenty_one_ema > eight_ema and\
                last_close < one_hundred_ema  and last_close < two_hundred_sma\
                and last_close < eight_ema:
            extreme_value = True
            contract = put
        else:
            print("Waiting for extreme value...\n")

    acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask
    delta = contract_data.bidGreeks.delta

    mid = (bid + ask) / 2

    if (mid * 100) > (acc_vals * 0.3):
        print("SPY option too big for account")

    else:

        limit_price = mid
        take_profit = mid + (delta * 0.4)
        stop_loss_price = mid - delta

        limit_price = round(limit_price, 2)
        take_profit = round(take_profit, 2)
        stop_loss_price = round(stop_loss_price, 2)

        buy_order = ib.bracketOrder(
                   'BUY',
                   quantity=qty,
                   limitPrice=limit_price,
                   takeProfitPrice=take_profit,
                   stopLossPrice=stop_loss_price
               )

        for o in buy_order:
           o.tif = 'GTC'
           ib.sleep(0.00001)
           ib.placeOrder(contract, o)

    return extreme_value, contract


# sleep_until_market_open()

ticker = 'SPY'

put_year = '2022'
put_month = '03'
put_day = '14'

call_year = '2022'
call_month = '03'
call_day = '14'

put_strike = '420'
call_strike = '430'

qty = 5

put = Option(ticker, put_year + put_month + put_day, put_strike, 'P',  "SMART")
call = Option(ticker, call_year + call_month + call_day, call_strike, 'C',  "SMART")

extreme_value, contract = place_order(call, put, qty)

if extreme_value:
    timeToSleep = (15 * 60 - time.time() % (15 * 60))
    print("Sleeping for " + str(timeToSleep) + " seconds")

    time.sleep(timeToSleep)
    sell_stock(ib, qty, contract)
