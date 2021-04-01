import asyncio
import datetime
from time import sleep
import pandas as pd

import tinvest as ti
from tinvest import MarketOrderRequest, SandboxSetCurrencyBalanceRequest, LimitOrderRequest

from models import Journal, Traider, Stock, StrategyMACD_Day

TOKEN = "t.fPUeRgDE9xkUbo4JTCxF4257U0QVkigXRk80u_mHGkNxn7vFq3Y0hOdi4REbliwcNAZYaiyCZZb8rrR5qQlffQ"
figi = 'BBG004730N88'

years = [2021]
depth = 2
data = []
params = {'loss_level': 0.003,
          'profit_level': 0.02,
          'macd_level': 0,
          'target_stability': 0
          }

loss = params['loss_level']
profit = params['profit_level']
macd_level = params['macd_level']
target_stability = params['target_stability']


async def get_data(client, figi):
    print('Start update data')
    data = []
    start_date = datetime.datetime.now()
    end_date = start_date - datetime.timedelta(days=depth)

    res = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
    ).tolist()
    for date in res:
        response = await client.get_market_candles(figi=figi,
                                                   from_=datetime.datetime(date.year, date.month, date.day, 0, 0),
                                                   to=datetime.datetime(date.year, date.month, date.day, 23, 55),
                                                   interval=ti.CandleResolution.min5)
        for d in response.payload.candles:
            data_time = {
                'date': d.time.strftime('%e-%m-%Y %H:%M'),
                'Open': d.o,
                'High': d.h,
                'Low': d.l,
                'Close': d.c,
                'Volume': d.v,
                'figi': d.figi,
            }
            data.append(data_time)
    return data


async def main(broker_account_id=None):
    balance = 10000
    amount = 20

    journal = Journal(mode='debug')
    traider = Traider(balance, journal, amount)
    stock = Stock(traider, journal)
    client = ti.AsyncClient(TOKEN, use_sandbox=True)
    data = await get_data(client, figi)
    print('Amount of data:', len(data))
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    traider.trade(df, strategy=StrategyMACD_Day(loss_level=loss, profit_level=profit, macd_level=macd_level,
                                                target_stability=target_stability))
    stock.interval_trade(df[-1:])
    no_update = True
    async with ti.Streaming(TOKEN, receive_timeout=20, reconnect_timeout=10, heartbeat=20) as streaming:
        await streaming.candle.subscribe(figi, ti.CandleResolution.min5)
        async for event in streaming:

            if event.event == 'candle':
                pass
                # print(event.payload.figi, event.payload.c, event.payload.interval, event.payload.h, event.payload.time)

            if not (event.payload.time.strftime('%e-%m-%Y %H:%M') == data[-1]['date']) and no_update:
                no_update = False
                data = await get_data(client, figi)
                df = pd.DataFrame(data)
                df.set_index('date', inplace=True)
                traider.trade(df, strategy=StrategyMACD_Day(loss_level=loss, profit_level=profit, macd_level=macd_level,
                                                            target_stability=target_stability))
                stock.interval_trade(df[-1:])
            elif event.payload.time.strftime('%e-%m-%Y %H:%M') == data[-1]['date']:
                no_update = True
            #print(journal.get_orders())


asyncio.run(main())
