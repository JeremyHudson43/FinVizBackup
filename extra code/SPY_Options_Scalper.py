from ib_insync import *
import random
from datetime import *
import time
import pandas as pd
from dateutil import parser
import sys
import talib
import math

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))


def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


def check_time():
    # check if it is before 2:00 PM
    if datetime.now().hour == 14:
        return True
    else:
        return False


def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:40").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)


def sell_stock(ib, contract, orders):

   for order in orders:
       try:
        ib.cancelOrder(order)
       except Exception as e:
           print(e)

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


def finish_order(ib, contract, orders):
    acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask
    delta = abs(contract_data.bidGreeks.delta)

    mid = (bid + ask) / 2

    qty = ((acc_vals // mid) // 100)

    limit_price = mid
    take_profit = mid + (delta * 0.45)
    stop_loss_price = mid - (delta * 0.3)

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
        orders.append(o)

    return contract, orders


def place_order():

    orders = []

    extreme_value = False

    while not extreme_value:

        past_two = check_time()

        if past_two:
            sys.exit(0)

        elif not past_two:

            ticker = 'SPY'

            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day

            year = str(year)
            month = str(month)
            day = str(day)

            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day

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

            one_hundred_sma = talib.SMA(market_data['close'].values, timeperiod=100)[-1]
            five_ema = talib.EMA(market_data['close'].values, timeperiod=5)[-1]

            last_close = market_data['close'].iloc[-1]

            williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]

            print("\nLast Close: " + str(last_close) + '\n')
            print("Williams %: " + str(williams_perc) + '\n')
            print('100 SMA: ' + str(one_hundred_sma) + '\n')
            print('5 EMA: ' + str(five_ema) + '\n')

            print('- - - - - - - - - - - - - - - - - - - - \n')

            call_strike = math.ceil(last_close)
            put_strike = math.floor(last_close)

            if williams_perc <= -80 and last_close > one_hundred_sma and last_close > five_ema:

                extreme_value = True

                call = Option(ticker, year + month + day, call_strike, 'C', "SMART")

                contract = call

                contract, orders = finish_order(ib, contract, orders)

                return extreme_value, contract, orders

            elif williams_perc >= -20 and last_close < one_hundred_sma and last_close < five_ema:

                extreme_value = True

                put = Option(ticker, year + month + day, put_strike, 'P', "SMART")

                contract = put

                contract, orders = finish_order(ib, contract, orders)

                return extreme_value, contract, orders


            else:
                print("Waiting for extreme value...\n")


sleep_until_market_open()


extreme_value, contract, orders = place_order()

if extreme_value:
    timeToSleep = 600
    print("Sleeping for " + str(timeToSleep) + " seconds")

    time.sleep(timeToSleep)
    sell_stock(ib, contract, orders)
from ib_insync import *
import random
from datetime import *
import time
import pandas as pd
from dateutil import parser
import sys
import talib
import math

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))


def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = 100 * ((close - highh) / (highh - lowl))
    return wr


def check_time():
    # check if it is before 2:00 PM
    if datetime.now().hour == 14:
        return True
    else:
        return False


def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:40").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)


def sell_stock(ib, contract, orders):

   for order in orders:
       try:
        ib.cancelOrder(order)
       except Exception as e:
           print(e)

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


def finish_order(ib, contract, orders):
    acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask
    delta = abs(contract_data.bidGreeks.delta)

    mid = (bid + ask) / 2

    qty = ((acc_vals // mid) // 100)

    limit_price = mid
    take_profit = mid + (delta * 0.45)
    stop_loss_price = mid - (delta * 0.3)

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
        orders.append(o)

    return contract, orders


def place_order():

    orders = []

    extreme_value = False

    while not extreme_value:

        past_two = check_time()

        if past_two:
            sys.exit(0)

        elif not past_two:

            ticker = 'SPY'

            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day

            year = str(year)
            month = str(month)
            day = str(day)

            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day

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

            one_hundred_sma = talib.SMA(market_data['close'].values, timeperiod=100)[-1]
            five_ema = talib.EMA(market_data['close'].values, timeperiod=5)[-1]

            last_close = market_data['close'].iloc[-1]

            williams_perc = get_wr(market_data['high'], market_data['low'], market_data['close'], 2).iloc[-1]

            print("\nLast Close: " + str(last_close) + '\n')
            print("Williams %: " + str(williams_perc) + '\n')
            print('100 SMA: ' + str(one_hundred_sma) + '\n')
            print('5 EMA: ' + str(five_ema) + '\n')

            print('- - - - - - - - - - - - - - - - - - - - \n')

            call_strike = math.ceil(last_close)
            put_strike = math.floor(last_close)

            if williams_perc <= -80 and last_close > one_hundred_sma and last_close > five_ema:

                extreme_value = True

                call = Option(ticker, year + month + day, call_strike, 'C', "SMART")

                contract = call

                contract, orders = finish_order(ib, contract, orders)

                return extreme_value, contract, orders

            elif williams_perc >= -20 and last_close < one_hundred_sma and last_close < five_ema:

                extreme_value = True

                put = Option(ticker, year + month + day, put_strike, 'P', "SMART")

                contract = put

                contract, orders = finish_order(ib, contract, orders)

                return extreme_value, contract, orders


            else:
                print("Waiting for extreme value...\n")


sleep_until_market_open()


extreme_value, contract, orders = place_order()

if extreme_value:
    timeToSleep = 600
    print("Sleeping for " + str(timeToSleep) + " seconds")

    time.sleep(timeToSleep)
    sell_stock(ib, contract, orders)
