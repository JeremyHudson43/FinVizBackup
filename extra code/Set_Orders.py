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


def place_order(ticker, year, month, day, strike, right):

    contract = Option(ticker, year + month + day, strike, right, "SMART")

    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(*[contract])[0]

    bid = contract_data.bid

    qty = 1

    limit_price = bid * 1.03
    take_profit = bid * 1.15
    stop_loss_price = bid * 0.5

    print(bid)

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
place_order('SPY', '2022', '02', '28', '437', 'P')
