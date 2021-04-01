import asyncio
from datetime import datetime

import tinvest as ti
from tinvest import MarketOrderRequest, SandboxSetCurrencyBalanceRequest, LimitOrderRequest

TOKEN = "t.fPUeRgDE9xkUbo4JTCxF4257U0QVkigXRk80u_mHGkNxn7vFq3Y0hOdi4REbliwcNAZYaiyCZZb8rrR5qQlffQ"
figi = 'BBG004730N88'


async def main(broker_account_id=None):
    client = ti.AsyncClient(TOKEN, use_sandbox=True)

    # async with ti.Streaming(TOKEN) as streaming:
    #     await streaming.candle.subscribe(figi, ti.CandleResolution.min1)
    #     await streaming.orderbook.subscribe(figi, 5)
    #     await streaming.instrument_info.subscribe(figi)
    #     async for event in streaming:
    #     #print(event.json())
    #         if event.event == 'candle':
    #             print(event.payload.c)
    #             print(event.payload.figi)
    #         if event.event == 'orderbook':
    #             print(event.payload.depth)

    # body = SandboxSetCurrencyBalanceRequest(
    #         balance=10000,
    #         currency='RUB',
    # )
    # await client.set_sandbox_currencies_balance(body, broker_account_id)


    # body = MarketOrderRequest(
    #         lots=1,
    #         operation='Buy'
    # )
    # response = await client.post_orders_market_order(figi, body, broker_account_id)
    # print(response)

    # body = LimitOrderRequest(
    #         lots=2,
    #         operation='Buy',
    #         price=200.85,
    # )
    # await client.post_orders_limit_order(figi, body, broker_account_id)

    # orders = await client.get_orders(broker_account_id)
    # print(orders)

    # clear = await client.clear_sandbox_account(broker_account_id)
    # print(clear)

    acc = await client.get_accounts()
    print(acc)

    portfolio = await client.get_portfolio(broker_account_id)
    for p in portfolio.payload.positions:
        print(p)

    p_curr = await client.get_portfolio_currencies(broker_account_id)
    for p_ in p_curr.payload.currencies:
        print(p_)

    operations = await client.get_operations(datetime(2021, 3, 31, 0, 0), datetime(2021, 3, 31, 23, 45), figi, None)
    for q in operations.payload.operations:
        print(q.figi, q.price, q.operation_type.value, q.quantity)

    # instr = await client.get_market_search_by_figi(figi)
    # print(instr)

    book = await client.get_market_orderbook(figi, 1)
    for b in book.payload:
        print(b)
    print(book.payload.close_price)

asyncio.run(main())
