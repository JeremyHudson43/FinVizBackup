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


def get_percent(first, second):
    if first == 0 or second == 0:
        return 0
    else:
        percent = first / second * 100
    return percent


def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:45").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)

def sell_stock(ib, qty, ticker):

   ib.reqGlobalCancel()

   if qty > 0:

       order = Order(orderId=27, action='Sell', orderType='MKT', totalQuantity=qty)

       ib.placeOrder(ticker, order)

       print('\nSold ' + str(ticker) + " at the end of the day!")

       time.sleep(10)

       sys.exit(0)


def place_order(call, put, qty):

    extreme_value_call = False
    extreme_value_put = False

    while not extreme_value_put or not extreme_value_call:

        ticker_contract = Stock('SPY', 'SMART', 'USD')

        secondsToSleep = 900 - datetime.now().minute % 900
        print("Sleeping for " + str(secondsToSleep) + " seconds")

        time.sleep(secondsToSleep)

        market_data = pd.DataFrame(
            ib.reqHistoricalData(
                ticker_contract,
                endDateTime='',
                durationStr='14 D',
                barSizeSetting='15 mins',
                whatToShow="TRADES",
                formatDate=1,
                useRTH=True,
                timeout=0
            ))

        market_data.drop(market_data.tail(1).index, inplace=True)

        last_sma = talib.SMA(market_data['close'], timeperiod=200).iloc[-1]
        last_close = market_data['close'].iloc[-1]

        print(last_close, last_sma)

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        market_data['SMA'] = talib.SMA(market_data['close'], timeperiod=200)

        market_data['williams_perc'] = get_wr(market_data['high'], market_data['low'], market_data['close'], 2)

        market_data.to_csv('C:\\Users\\Frank Einstein\\Desktop\\results\\market_data.csv')

        if williams_perc < -90 and last_close > last_sma:
            extreme_value_call = True
        elif williams_perc > -10 and last_close < last_sma:
            extreme_value_put = True
        else:
            print("Waiting for extreme value...")

    acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    if extreme_value_put:
        contract = put
    elif extreme_value_call:
        contract = call

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask

    mid = (bid + ask) / 2

    if (mid * 100) > (acc_vals * 0.2):
        print("SPY option too big for account")

    else:

        limit_price = mid
        take_profit = mid * 1.1
        stop_loss_price = mid * 0.8

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

    secondsToSleep = 900 - datetime.now().minute % 900
    print("Sleeping for " + str(secondsToSleep) + " seconds")

    time.sleep(secondsToSleep)

    sell_stock(ib, qty, contract)


sleep_until_market_open()

ticker = 'SPY'

put_year = '2022'
put_month = '03'
put_day = '11'

call_year = '2022'
call_month = '03'
call_day = '11'

put_strike = '425'
call_strike = '430'

qty = 5

put = Option(ticker, put_year + put_month + put_day, put_strike, 'P',  "SMART")
call = Option(ticker, call_year + call_month + call_day, call_strike, 'C',  "SMART")

place_order(call, put, qty)
