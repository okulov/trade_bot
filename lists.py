import asyncio
import tinvest as ti
import json

TOKEN = "t.fPUeRgDE9xkUbo4JTCxF4257U0QVkigXRk80u_mHGkNxn7vFq3Y0hOdi4REbliwcNAZYaiyCZZb8rrR5qQlffQ"


async def async_save_to_file(list, name_file):
    with open(name_file, 'w') as f:
        json.dump(list, f)


async def async_lists(TOKEN, name_file='list_instruments.json'):
    client = ti.AsyncClient(TOKEN, use_sandbox=True)
    list = {}

    bonds = await client.get_market_bonds()
    list['bonds'] = []
    figi_bonds = {}
    for i in bonds.payload.instruments:
        figi_bonds['figi'] = i.figi
        figi_bonds['status'] = False
        list['bonds'].append(figi_bonds)
    print(list)

    etfs = await client.get_market_etfs()
    list['etfs'] = []
    figi_etfs = {}
    for i in etfs.payload.instruments:
        figi_etfs['figi'] = i.figi
        figi_etfs['status'] = False
        list['etfs'].append(figi_etfs)
    print(list['etfs'])

    stocks = await client.get_market_stocks()
    list['stocks'] = []
    figi_stocks = {}
    for i in stocks.payload.instruments:
        figi_stocks['figi'] = i.figi
        figi_stocks['status'] = False
        list['stocks'].append(figi_stocks)
    print(list['stocks'])
    await client.close()
    await async_save_to_file(list, name_file)
    return list


def save_to_file(list, name_file):
    with open(name_file, 'w') as f:
        json.dump(list, f)


def sync_lists(TOKEN, name_file='list_instruments.json'):
    list = {}
    client = ti.SyncClient(TOKEN, use_sandbox=True)

    bonds = client.get_market_bonds()
    list['bonds'] = []
    for i in bonds.payload.instruments:
        figi_bonds = {}
        figi_bonds['figi'] = i.figi
        figi_bonds['status'] = False
        list['bonds'].append(figi_bonds)
    print(list)

    etfs = client.get_market_etfs()
    list['etfs'] = []
    for i in etfs.payload.instruments:
        figi_etfs = {}
        figi_etfs['figi'] = i.figi
        figi_etfs['status'] = False
        list['etfs'].append(figi_etfs)
    print(list['etfs'])

    stocks = client.get_market_stocks()
    list['stocks'] = []
    for i in stocks.payload.instruments:
        figi_stocks = {}
        figi_stocks['figi'] = i.figi
        figi_stocks['status'] = False
        list['stocks'].append(figi_stocks)
    print(list['stocks'])
    save_to_file(list, name_file)
    return list



if __name__ == '__main__':
    #async_client = ti.AsyncClient(TOKEN, use_sandbox=True)
    #asyncio.run(async_lists(TOKEN))

    # sync_client = ti.SyncClient(TOKEN, use_sandbox=True)
    sync_lists(TOKEN)
