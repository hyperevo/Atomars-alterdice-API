=================================
Atomars Python API Documentation
=================================

This is the documentation on how to use any of the functions in this API. Please check the tests folder for some code examples of some of the functions.

Most of the functions just return the JSON decoded response from the exchange API. Some of the later functions return properly formatted Decimals to retain precision.

Before making any requests, you must first login:


::

    api = AtomarsAPI(username, password)
    await api.login()


Creating the API class
~~~~~~~~~~~~~~~~~~~~~~~

**__init__(username, password, API_url = 'https://api.atomars.com/v1/', default_pair ='HLSETH')**

*Parameters:*
1. Username
2. Password
3. API url. https://api.atomars.com/v1/ for atomars, https://api.alterdice.com/v1/ for alterdice
4. Your default pair. Some functions will use this pair by default so you don't need to keep specifying the pair parameter.

None

**Example:**

::

    <<
    api = AtomarsAPI('my_account@test.com', '1337_hacker', 'https://api.atomars.com/v1/', 'HLSETH')
    >>


Logging in
~~~~~~~~~~~~~~~~~~~~~

**login() -> None:**

*Parameters:*

None

**Example:**

::

    <<
    await api.login()
    >>


Requesting balances
~~~~~~~~~~~~~~~~~~~~~

**get_balances(only_non_zero: bool = False) -> Dict:**

*Parameters:*

1. only_non_zero: boolean that determines whether to return only non zero balances or not

*Returns:*

A dictionary formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_balances()
    >>
    'HLS': {'balance': 19957756355391,
         'balance_available': 19957756355391,
         'currency': {'iso3': 'HLS', 'name': 'Helios Protocol'}},
    'HOT': {'balance': 0,
         'balance_available': 0,
         'currency': {'iso3': 'HOT', 'name': 'Holo'}},
    ...



Requesting balance of a single currency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_balance(currency: str) -> Dict**

*Parameters:*

1. currency: the ticker symbol

*Returns:*

A dictionary formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_balance('HLS')
    >>
    {'balance': 199577563553,
     'balance_available': 199577563553,
     'currency': {'iso3': 'HLS', 'name': 'Helios Protocol'}}

Limit buy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**limit_buy(price: float, volume: float, pair: str = None) -> int**

*Parameters:*

1. The price that you would like to buy at
2. The volume that you would like to buy
3. The pair you would like to buy

*Returns:*

This function returns the order id

**Example:**

::

    <<
    await api.limit_buy(0.0002, 100, "HLSETH")
    >>
    1337


Limit sell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**limit_sell(price: float, volume: float, pair: str = None) -> int**

*Parameters:*

1. The price that you would like to sell at
2. The volume that you would like to sell
3. The pair you would like to sell

*Returns:*

This function returns the order id

**Example:**

::

    <<
    await api.limit_sell(0.0002, 100, "HLSETH")
    >>
    1337


Get your order history
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_order_history() -> List[Dict]**

*Parameters:*

None

*Returns:*

A list formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_order_history()
    >>
    [{'id': 418138993,
     'pair': 'HLSBTC',
     'price': 1.1e-07,
     'price_done': 0,
     'rate': 2.6e-06,
     'status': 3,
     'time_create': 1571422528,
     'time_done': 1571422793,
     'type': 1,
     'type_trade': 0,
     'volume': 0.04453926,
     'volume_done': 0},
    {'id': 418138992,
     'pair': 'HLSBTC',
     'price': 6e-08,
     'price_done': 6e-08,
     'rate': 2.34e-06,
     'status': 2,
     'time_create': 1571422528,
     'time_done': 1571422764,
     'type': 1,
     'type_trade': 0,
     'volume': 0.02903803,
     'volume_done': 0.02903803}]


Get your active orders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_active_orders(pair: str = None) -> List[Dict]**

*Parameters:*

1. The pair that you would like active orders for. Leave blank to return all pairs.

*Returns:*

A List formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_active_orders('HLSETH')
    >>
    [{'id': 514806416,
      'pair': 'HLSETH',
      'price': 1.859e-05,
      'price_done': 0,
      'rate': 0.00018597,
      'status': 1,
      'time_create': 1575078912,
      'time_done': None,
      'type': 1,
      'type_trade': 0,
      'volume': 0.1,
      'volume_done': 0},...]


Delete an order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**delete_order(order_id: int) -> None**

*Parameters:*

1. The order id that you would like to delete

*Returns:*

None

**Example:**

::

    <<
    await api.delete_order(1337)
    >>


Get the ticker list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_ticker_list() -> List[Dict]**

*Parameters:*

None

*Returns:*

A List formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_ticker_list()
    >>
    {'base': 'HLS', 'pair': 'HLSBTC', 'quote': 'BTC'},
    {'base': 'HLS', 'pair': 'HLSETH', 'quote': 'ETH'},
    {'base': 'HLS', 'pair': 'HLSUSDT', 'quote': 'USDT'},
    ...


Get the order book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_order_book(pair: str = None) -> Dict**

*Parameters:*

1. The pair that you would like the order book for. Leave blank to use the default pair.

*Returns:*

A Dict formated as the exchange API sends it. See below.

**Example:**

::

    <<
    await api.get_order_book()
    >>
    {'buy': [{'count': 1, 'rate': 0.00018328, 'volume': 0.07408359},
             {'count': 1, 'rate': 0.00016, 'volume': 0.0708424},
             {'count': 3, 'rate': '0.000001', 'volume': 13900},
             {'count': 1, 'rate': '0.0000001', 'volume': 10000}],
    'sell': [{'count': 1, 'rate': 0.00018406, 'volume': 1.85251332},
             {'count': 1, 'rate': 0.00018505, 'volume': 52.93249219},
             {'count': 1, 'rate': 0.054, 'volume': 1000},
             {'count': 1, 'rate': 1, 'volume': 562}]}


Delete all of your active orders at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**delete_all_orders(pair: str = None, buy_or_sell: int = None) -> None**

*Parameters:*

1. The pair that you would like the order book for. Leave blank to use the default pair.
2. 0 for buy, 1 for sell.

*Returns:*

None

**Example:**

::

    <<
    await api.delete_all_orders('HLSETH', 1)
    >>


Find out if an order is complete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**is_order_complete(order_id: int) -> bool**

*Parameters:*

1. The order id.

*Returns:*

True if the order is complete, False if it isnt.

**Example:**

::

    <<
    await api.is_order_complete(1337)
    >>
    True


Get the lowest sell in the order book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_lowest_sell(pair: str = None, order_book: Dict = None) -> Decimal**

*Parameters:*

1. The pair that you would like the order book for. Leave blank to use the default pair.
2. An optional order book to use. If left blank, it will request the order book from the API.

*Returns:*

The lowest sell in Decimal format

**Example:**

::

    <<
    await api.get_lowest_sell('HLSETH')
    >>
    Decimal('0.00012049')


Get the highest buy in the order book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_highest_buy(pair: str = None, order_book: Dict = None) -> Decimal**

*Parameters:*

1. The pair that you would like the order book for. Leave blank to use the default pair.
2. An optional order book to use. If left blank, it will request the order book from the API.

*Returns:*

The highest buy in Decimal format

**Example:**

::

    <<
    await api.get_highest_buy('HLSETH')
    >>
    Decimal('0.00011893')


Get both the lowest sell and highest buy at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**get_lowest_sell_and_highest_buy(pair: str = None, order_book: Dict = None) -> Tuple[Optional[Decimal], Optional[Decimal]]**

*Parameters:*

1. The pair that you would like the order book for. Leave blank to use the default pair.
2. An optional order book to use. If left blank, it will request the order book from the API.

*Returns:*

The lowest sell (or none), and the highest buy (or none)

**Example:**

::

    <<
    await api.get_lowest_sell_and_highest_buy('HLSETH')
    >>
    (Decimal('0.00011957'), Decimal('0.00011823'))