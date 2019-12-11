import asyncio

from atom_alter_API.api import AtomarsAlterdiceAPI

from test_config import API_login_username, API_login_password

import logging

from pprint import pprint

class TestClass():

    def __init__(self):
        self.api = AtomarsAlterdiceAPI(API_login_username, API_login_password)

    async def test_get_balances(self):
        await self.api.login()
        balances = await self.api.get_balances()
        pprint(balances)

        balances = await self.api.get_balances(True)
        pprint(balances)

    async def test_get_balance(self):
        await self.api.login()
        balance = await self.api.get_balance('HLS')
        pprint(balance)

        # Returns
        # {'balance': 199577563553,
        #  'balance_available': 199577563553,
        #  'currency': {'iso3': 'HLS', 'name': 'Helios Protocol'}}

    async def test_get_order_history(self):
        await self.api.login()
        order_history = await self.api.get_order_history()
        pprint(order_history)

        # Returns
        # [{'id': 418138993,
        #  'pair': 'HLSBTC',
        #  'price': 1.1e-07,
        #  'price_done': 0,
        #  'rate': 2.6e-06,
        #  'status': 3,
        #  'time_create': 1571422528,
        #  'time_done': 1571422793,
        #  'type': 1,
        #  'type_trade': 0,
        #  'volume': 0.04453926,
        #  'volume_done': 0},
        # {'id': 418138992,
        #  'pair': 'HLSBTC',
        #  'price': 6e-08,
        #  'price_done': 6e-08,
        #  'rate': 2.34e-06,
        #  'status': 2,
        #  'time_create': 1571422528,
        #  'time_done': 1571422764,
        #  'type': 1,
        #  'type_trade': 0,
        #  'volume': 0.02903803,
        #  'volume_done': 0.02903803}]

    async def test_get_active_orders(self):
        await self.api.login()
        #await self.api.limit_sell(0.00018597, volume=0.1, pair='HLSETH')
        active_orders = await self.api.get_active_orders('HLSETH')
        pprint(active_orders)

        # Returns
        # [{'id': 514806416,
        #   'pair': 'HLSETH',
        #   'price': 1.859e-05,
        #   'price_done': 0,
        #   'rate': 0.00018597,
        #   'status': 1,
        #   'time_create': 1575078912,
        #   'time_done': None,
        #   'type': 1,
        #   'type_trade': 0,
        #   'volume': 0.1,
        #   'volume_done': 0},...]

    async def test_ticker_list(self):
        await self.api.login()
        ticker_list = await self.api.get_ticker_list()
        pprint(ticker_list)

        # Returns
        # {'base': 'HLS', 'pair': 'HLSBTC', 'quote': 'BTC'},
        # {'base': 'HLS', 'pair': 'HLSETH', 'quote': 'ETH'},
        # {'base': 'HLS', 'pair': 'HLSUSDT', 'quote': 'USDT'},
        # ...

    async def test_get_order_book(self):
        await self.api.login()
        order_book = await self.api.get_order_book()
        pprint(order_book)

        # Returns
        # {'buy': [{'count': 1, 'rate': 0.00018328, 'volume': 0.07408359},
        #          {'count': 1, 'rate': 0.00016, 'volume': 0.0708424},
        #          {'count': 3, 'rate': '0.000001', 'volume': 13900},
        #          {'count': 1, 'rate': '0.0000001', 'volume': 10000}],
        #  'sell': [{'count': 1, 'rate': 0.00018406, 'volume': 1.85251332},
        #           {'count': 1, 'rate': 0.00018505, 'volume': 52.93249219},
        #           {'count': 1, 'rate': 0.054, 'volume': 1000},
        #           {'count': 1, 'rate': 1, 'volume': 562}]}

    async def test_get_lowest_sell(self):
        await self.api.login()
        lowest_sell = await self.api.get_lowest_sell('HLSETH')
        pprint(lowest_sell)

        # Returns
        # Decimal('0.00012049')

    async def test_get_highest_buy(self):
        await self.api.login()
        highest_buy = await self.api.get_highest_buy('HLSETH')
        pprint(highest_buy)

        # Returns
        # Decimal('0.00011893')

    async def test_get_lowest_sell_and_highest_buy(self):
        await self.api.login()
        both = await self.api.get_lowest_sell_and_highest_buy('HLSETH')
        pprint(both)

        # Returns
        # Decimal('0.00012049')



if __name__ == "__main__":
    __spec__ = 'None'

    logger = logging.getLogger("Main")
    logger.info("Starting trading bot")

    testClass = TestClass()
    #asyncio.ensure_future(testClass.test_get_balances())
    #asyncio.ensure_future(testClass.test_get_balance())
    #asyncio.ensure_future(testClass.test_get_order_history())
    #asyncio.ensure_future(testClass.test_get_lowest_sell())
    #asyncio.ensure_future(testClass.test_get_highest_buy())
    asyncio.ensure_future(testClass.test_get_lowest_sell_and_highest_buy())

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()



