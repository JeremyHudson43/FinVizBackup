from ib_insync import *
import random
from datetime import *
import time
import pandas as pd
from dateutil import parser

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:31").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)


def place_order(ticker, year, month, day, strike, right, qty):

    contract = Option(ticker, year + month + day, strike, right, "SMART")

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid
    ask = contract_data.ask

    mid = (bid + ask) / 2
    mid = ask

    limit_price = mid
    take_profit = mid * 1.20
    stop_loss_price = mid * 0.50

    limit_price = 0.05 * round(limit_price / 0.05)
    take_profit = 0.05 * round(take_profit / 0.05)
    stop_loss_price = 0.05 * round(stop_loss_price / 0.05)

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
        o.transmit = True
        o.tif = 'GTC'
        ib.sleep(0.001)
        ib.placeOrder(contract, o)


# sleep_until_market_open()

place_order('SPY', '2022', '03', '11', '438', 'P', 2)
# place_order('UVXY', '2022', '03', '11', '18', 'P', 1)
