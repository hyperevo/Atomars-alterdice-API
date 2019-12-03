import asyncio

from atom_alter_API.api import AtomarsAlterdiceAPI

from test_config import API_login_username, API_login_password

import logging

from pprint import pprint

# Trading bot name for logging dir
trading_bot_name = "atomars_trading_bot_tester"

class TestClass():

    def __init__(self):
        self.api = AtomarsAlterdiceAPI(API_login_username, API_login_password)

    async def test_get_balances(self):
        await self.api.login()
        balances = await self.api.get_balances()
        pprint(balances)

        balances = await self.api.get_balances(True)
        pprint(balances)

    async def test_get_active_orders(self):
        await self.api.login()
        await self.api.limit_sell(0.00018597, volume=0.1, pair='HLSETH')
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

        # returns
        # {'buy': [{'count': 1, 'rate': 0.00018328, 'volume': 0.07408359},
        #          {'count': 1, 'rate': 0.00016, 'volume': 0.0708424},
        #          {'count': 3, 'rate': '0.000001', 'volume': 13900},
        #          {'count': 1, 'rate': '0.0000001', 'volume': 10000}],
        #  'sell': [{'count': 1, 'rate': 0.00018406, 'volume': 1.85251332},
        #           {'count': 1, 'rate': 0.00018505, 'volume': 52.93249219},
        #           {'count': 1, 'rate': 0.054, 'volume': 1000},
        #           {'count': 1, 'rate': 1, 'volume': 562}]}


if __name__ == "__main__":
    __spec__ = 'None'

    logger = logging.getLogger("Main")
    logger.info("Starting trading bot")

    testClass = TestClass()
    asyncio.ensure_future(testClass.test_get_balances())

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()



