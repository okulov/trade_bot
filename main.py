import asyncio
import csv
import json
from datetime import datetime

import tinvest as ti
import asyncio
from tinvest import AsyncClient

TOKEN = "t.fPUeRgDE9xkUbo4JTCxF4257U0QVkigXRk80u_mHGkNxn7vFq3Y0hOdi4REbliwcNAZYaiyCZZb8rrR5qQlffQ"

# async def main():
#     client = tinvest.AsyncClient(TOKEN, use_sandbox=True)
#     response = await client.get_portfolio()  # tinvest.PortfolioResponse
#     print(response.payload)
#
#     await client.close()
#
# asyncio.run(main())



figi = {
    'figi_sber': 'BBG004730N88',
    'figi_yandex': 'BBG006L8G4H1',
    'figi_tin': 'BBG00QPYJ5H0',
    'figi_aeroflot': 'BBG004S683W7',
    'figi_bashneft': 'BBG004S68758',
    'figi_gazprom': 'BBG004730RP0',
}

years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]


# years = [2015]


async def main():
    # client = AsyncClient(TOKEN, use_sandbox=True)
    # await client.get_accounts()
    # await client.get_market_candles(figi=figi, from_=datetime(2021, 1, 25), to=datetime(2021, 1, 27), interval=ti.CandleResolution.day)
    # await client.close()

    client = ti.AsyncClient(TOKEN, use_sandbox=True)
    # response = await client.get_accounts()  # tinvest.PortfolioResponse
    data = []
    data_time = {}
    for key, figi_code in figi.items():
        for year in years:
            response = await client.get_market_candles(figi=figi_code, from_=datetime(year, 3, 12, 0, 0),
                                                       to=datetime(year + 1, 3, 11, 23, 45),
                                                       interval=ti.CandleResolution.day)
            for d in response.payload.candles:
                data_time = {
                    'date': d.time.strftime('%e-%m-%Y'),
                    'Open': d.o,
                    'High': d.h,
                    'Low': d.l,
                    'Close': d.c,
                    'Volume': d.v,
                    'figi': d.figi,
                }
                data.append(data_time)

    await client.close()
    # print(data[1])
    # print(len(data))

    with open('data/day_data.csv', 'w', newline='') as f_n:
        F_N_WRITER = csv.DictWriter(f_n, fieldnames=list(data[0].keys()),
                                    quoting=csv.QUOTE_NONNUMERIC)
        F_N_WRITER.writeheader()
        for d in data:
            F_N_WRITER.writerow(d)

    # await client.close()

    # async with ti.Streaming(TOKEN) as streaming:
    #     await streaming.candle.subscribe('BBG0013HGFT4', ti.CandleResolution.min1)
    #     await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
    # await streaming.instrument_info.subscribe('BBG004730N88')
    # async for event in streaming:
    #     print(event.json())
    #         if event.event == 'candle':
    #             print(event.payload.c)
    #             print(event.payload.figi)
    #         if event.event == 'orderbook':
    #             print(event.payload.depth)


asyncio.run(main())
