import asyncio

import tinvest as ti

TOKEN = "t.fPUeRgDE9xkUbo4JTCxF4257U0QVkigXRk80u_mHGkNxn7vFq3Y0hOdi4REbliwcNAZYaiyCZZb8rrR5qQlffQ"
figi = 'BBG004730N88'

async def main():
    #client = ti.AsyncClient(TOKEN, use_sandbox=True)

    async with ti.Streaming(TOKEN) as streaming:
        await streaming.candle.subscribe(figi, ti.CandleResolution.min1)
        await streaming.orderbook.subscribe(figi, 5)
        await streaming.instrument_info.subscribe(figi)
        async for event in streaming:
        #print(event.json())
            if event.event == 'candle':
                print(event.payload.c)
                print(event.payload.figi)
            if event.event == 'orderbook':
                print(event.payload.depth)


asyncio.run(main())