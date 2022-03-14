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


def sell_stock(ib, contract):

   ib.reqGlobalCancel()

   option = [v for v in ib.positions() if v.contract.secType == 'OPT' and v.contract.symbol == 'SPY'][0]
   qty = option.position

   if qty > 0:

       contract_data = ib.reqTickers(*[contract])[0]
       lmt_price = (contract_data.bid + contract_data.ask) / 2

       order = Order(orderId=270, action='Sell', orderType='LMT', lmtPrice=lmt_price, totalQuantity=qty)

       ib.placeOrder(contract, order)

       print('\nSold ' + str(contract.symbol) + " at the end of the day!")

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

        two_hundred_ema = talib.EMA(market_data['close'].values, timeperiod=200)[-1]
        one_hundred_ema = talib.EMA(market_data['close'].values, timeperiod=100)[-1]
        fifty_ema = talib.EMA(market_data['close'].values, timeperiod=50)[-1]
        twenty_ema = talib.EMA(market_data['close'].values, timeperiod=20)[-1]

        last_close = market_data['close'].iloc[-1]

        williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]
        market_data['SMA'] = talib.SMA(market_data['close'], timeperiod=200)

        market_data['williams_perc'] = get_wr(market_data['high'], market_data['low'], market_data['close'], 2)

        market_data.to_csv('C:\\Users\\Frank Einstein\\Desktop\\results\\market_data.csv')

        print("\nLast Close: " + str(last_close) + '\n')
        print("Williams %: " + str(williams_perc) + '\n')
        print('200 EMA: ' + str(two_hundred_ema) + '\n')
        print('100 EMA: ' + str(one_hundred_ema) + '\n')
        print('50 EMA: ' + str(fifty_ema) + '\n')
        print("20 EMA: " + str(twenty_ema) + '\n')
        print('- - - - - - - - - - - - - - - - - - - - \n')

        if williams_perc <= -90 and last_close > two_hundred_ema and last_close > one_hundred_ema and last_close > fifty_ema and last_close > twenty_ema:
            extreme_value = True
            contract = call

        elif williams_perc >= -10 and last_close < two_hundred_ema and last_close < one_hundred_ema and last_close < fifty_ema and last_close < twenty_ema:
            extreme_value = True
            contract = put
        else:
            print("Waiting for extreme value...\n")

    acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask
    delta = abs(contract_data.bidGreeks.delta)

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


sleep_until_market_open()

ticker = 'SPY'

put_year = '2022'
put_month = '03'
put_day = '16'

call_year = '2022'
call_month = '03'
call_day = '16'

put_strike = '410'
call_strike = '430'

qty = 1

put = Option(ticker, put_year + put_month + put_day, put_strike, 'P',  "SMART")
call = Option(ticker, call_year + call_month + call_day, call_strike, 'C',  "SMART")

extreme_value, contract = place_order(call, put, qty)

if extreme_value:
    timeToSleep = 300
    print("Sleeping for " + str(timeToSleep) + " seconds")

    time.sleep(timeToSleep)
    sell_stock(ib, contract)
