from ib_insync import *
import random
from datetime import *
import time
import pandas as pd

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

def sleep_until_market_open():
    now = datetime.now()  # time object

    StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')

    if StartTime > TimeNow:
        time_until_market_open = (StartTime - TimeNow).total_seconds()
        time.sleep(time_until_market_open)


def place_order(ticker, year, month, day, strike, right, qty):

    contract = Option(ticker, year + month + day, strike, right, "SMART")

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.close

    limit_price = bid
    take_profit = bid * 1.15
    stop_loss_price = bid * 0.9

    limit_price = 0.05 * round(limit_price / 0.05)
    take_profit = 0.05 * round(take_profit / 0.05)
    stop_loss_price = 0.05 * round(stop_loss_price / 0.05)

    print(limit_price, take_profit, stop_loss_price)

    buy_order = ib.bracketOrder(
               'BUY',
               quantity=qty,
               limitPrice=limit_price,
               takeProfitPrice=take_profit,
               stopLossPrice=stop_loss_price
           )

    for o in buy_order:
        ib.placeOrder(contract, o)


sleep_until_market_open()

# HYG March 18 $82 put ($0.45 bid)

# IHI March 18 $59 put ($1.10 bid)

# URA March 18 $22 put ($0.75 bid)

# DBA March 18 $20 call ($0.80 bid)

place_order('HYG', '2022', '03', '18', '82', 'P', 1)
place_order('IHI', '2022', '03', '18', '59', 'P', 1)
place_order('URA', '2022', '03', '18', '22', 'P', 1)
place_order('DBA', '2022', '03', '18', '20', 'C', 1)
