import asyncio
import aiohttp

from typing import Dict, List, Any, Tuple, Optional
from decimal import Decimal

from .constants import (
    LIMIT_TRADE,
    BUY,
    SELL,
    HTTP_STATUS_SUCCESS)
from .utils.logging import BaseLoggingService

from .utils.mathematical import (
    sha256,
    generate_request_id,
    float_to_string,
    to_decimal)

from .exceptions import HTTPRequestError, HeaderCreationError, LoginError, BadRequestError, UnauthorizedError, \
    APIOperationStatusError, APIResponseError, APIExecutionError

http_status_errors = dict([(400, BadRequestError),
                          (401, UnauthorizedError),
                          (500, HTTPRequestError),
                          ])


def check_http_response_for_errors(response, resp_status, resp_headers):
    if resp_status != HTTP_STATUS_SUCCESS:
        if resp_status in http_status_errors:
            raise http_status_errors[resp_status]("Received an unknown bad response from server. \n"
                                   "response: {} \n"
                                   "status: {} \n"
                                   "header: {}"
                                   .format(response, resp_status, resp_headers))
        else:
            raise HTTPRequestError("Received an unknown bad response from server. \n"
                                   "response: {} \n"
                                   "status: {} \n"
                                   "header: {}"
                                   .format(response, resp_status, resp_headers))

def check_post_response_status(response, url):
    # post responses should all have status in the response, and it should = true or 1
    if 'status' not in response or response['status'] == False or response['status'] == 0:
        raise APIOperationStatusError("URL: {}\n"
                                      "RESPONSE: {}".format(
            url, response
        ))

class AtomarsAlterdiceAPI(BaseLoggingService):
    secret: str = None
    token: str = None
    default_pair: str = None
    active_orders: List = []

    def __init__(self, username, password, API_url = 'https://api.atomars.com/v1/', default_pair ='HLSETH'):
        self.secret = None
        self.token = None
        self.default_pair = default_pair
        self.active_orders = []
        self.username = username
        self.password = password
        self.base_url = API_url

    #
    # Networking functionality
    #
    async def send_post_request_and_get_response(self, url, payload, headers = None, check_response_for_errors = True) -> Dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(json=payload, url = url, headers= headers) as resp:
                    response = await resp.json()
                    resp_headers = resp.headers
                    resp_status = resp.status
        except Exception as e:
            raise HTTPRequestError(e)

        if check_response_for_errors:
            check_http_response_for_errors(response, resp_status, resp_headers)
            check_post_response_status(response, url)

        return response


    async def send_get_request_and_get_response(self, url, params) -> Dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url = url, params=params) as resp:
                    response = await resp.json()
                    resp_headers = resp.headers
                    resp_status = resp.status
        except Exception as e:
            raise HTTPRequestError(e)

        check_http_response_for_errors(response, resp_status, resp_headers)

        return response

    #
    # Header and signature functionality
    #
    def get_signed_headers(self, payload) -> Dict:
        if self.token is None:
            raise HeaderCreationError("Cannot create signed headers because we don't have our token. Make sure you are logged in first.")

        headers = {
            'login-token': self.token,
            'x-auth-sign': self.get_sig_from_payload(payload)
        }
        return headers

    def get_sig_from_payload(self, payload):
        if self.secret is None:
            raise HeaderCreationError("Cannot create signature because we don't have our secret. Make sure you are logged in first.")

        raw_sig = self._get_sig_from_payload(payload) + str(self.secret)
        sha256_sig = sha256(raw_sig)
        return sha256_sig

    def _get_sig_from_payload(self, payload):
        if isinstance(payload, dict):
            sorted_keys = sorted(payload.keys())
            to_return = ''
            for key in sorted_keys:
                to_return += str(self._get_sig_from_payload(payload[key]))
            return to_return
        elif isinstance(payload, Decimal):
            return str(payload)
        elif isinstance(payload, float):
            decimal = Decimal(payload)
            return str(decimal)
        elif isinstance(payload, str) or isinstance(payload, int):
            return str(payload)
        else:
            raise HeaderCreationError("I don't know how to create signature with this payload.")


    #
    # API Commands
    #
    async def login(self) -> None:
        self.logger.debug('Executing login')
        url = self.base_url + 'login'
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = await self.send_post_request_and_get_response(url, payload)
        if 'status' not in response or response['status'] == False:
            raise LoginError("Login failed. Errors: {}".format(response['errors']))
        else:
            self.logger.debug('login Succeeded')

        self.secret = response['data']['secret']
        self.token = response['token']



    async def get_balances(self, only_non_zero: bool = False) -> Dict:
        self.logger.debug('Executing get_balance')
        url = self.base_url + 'private/balances'
        payload = {
            'request_id': generate_request_id(),
        }
        headers = self.get_signed_headers(payload)

        response = await self.send_post_request_and_get_response(url, payload, headers)

        if 'data' in response and 'list' in response['data']:
            self.logger.debug('get_balances Succeeded')
            balances = response['data']['list']
            if only_non_zero:
                nonzero_balances = {}
                for pair in balances:
                    if float(balances[pair]['balance']) > 0:
                        nonzero_balances[pair] = balances[pair]
                return nonzero_balances
            else:
                return balances

        raise APIResponseError("No balances were returned.")

    async def get_balance(self, currency: str) -> float:
        balances = await self.get_balances()

        if currency in balances:
            return balances[currency]
        else:
            raise APIResponseError("No balance found for currency {}".format(currency))


    async def limit_buy(self, price: float, volume: float, pair: str = None) -> int:
        if pair is None:
            pair = self.default_pair

        price = float_to_string(price)
        volume = float_to_string(volume)

        self.logger.debug('Executing limit_buy with price: {}, volume: {}, pair: {}'.format(price, volume, pair))

        url = self.base_url + 'private/create-order'
        payload = {
            'type_trade': LIMIT_TRADE,
            'type': BUY,
            'rate': price,
            'volume': volume,
            'pair': pair,
            'request_id': generate_request_id(),
        }

        headers = self.get_signed_headers(payload)

        response = await self.send_post_request_and_get_response(url, payload, headers)

        if 'data' in response and 'id' in response['data']:
            self.logger.debug('limit_buy Succeeded for order id {}'.format(response['data']['id']))
            return response['data']['id']

        raise APIResponseError('limit_buy Failed. Response {}'.format(response))


    async def limit_sell(self, price: float, volume: float, pair:str = None) -> int:
        if pair is None:
            pair = self.default_pair

        price = float_to_string(price)
        volume = float_to_string(volume)

        self.logger.debug('Executing limit_sell with price: {}, volume: {}, pair: {}'.format(price, volume, pair))

        url = self.base_url + 'private/create-order'
        payload = {
            'type_trade': LIMIT_TRADE,
            'type': SELL,
            'rate': price,
            'volume': volume,
            'pair': pair,
            'request_id': generate_request_id(),
        }

        headers = self.get_signed_headers(payload)

        response = await self.send_post_request_and_get_response(url, payload, headers)

        if 'data' in response and 'id' in response['data']:
            self.logger.debug('limit_sell Succeeded for order id {}'.format(response['data']['id']))
            return response['data']['id']

        raise APIResponseError('limit_sell Failed. Response {}'.format(response))


    async def get_order_history(self) -> Dict:
        self.logger.debug('Executing get_order_history')
        url = self.base_url + 'private/history'
        payload = {
            'request_id': generate_request_id()
        }
        headers = self.get_signed_headers(payload)

        response = await self.send_post_request_and_get_response(url, payload, headers)

        if 'data' in response and 'list' in response['data']:
            self.logger.debug('get_order_history Succeeded')
            return response['data']['list']

        raise APIResponseError('get_order_history Failed. Response {}'.format(response))

    async def get_active_orders(self, pair: str = None) -> List:
        self.logger.debug('Executing get_active_orders')
        url = self.base_url + 'private/orders'
        payload = {
            'request_id': generate_request_id(),
        }

        headers = self.get_signed_headers(payload)

        response = await self.send_post_request_and_get_response(url, payload, headers)

        self.logger.debug('get_active_orders Succeeded')

        if 'data' not in response:
            raise APIResponseError('get_active_orders Failed. Response {}'.format(response))

        if len(response['data']) == 0:
            self.active_orders = []
        else:
            self.active_orders = response['data']['list']

        if pair is not None:
            #filter by pair
            filtered_active_orders = []
            for order in self.active_orders:
                if order['pair'] == pair:
                    filtered_active_orders.append(order)
        else:
            filtered_active_orders = self.active_orders
        return filtered_active_orders

    async def is_order_complete(self, order_id) -> bool:
        order_history = await self.get_order_history()

        for order in order_history:
            if order['id'] == order_id:
                return True
        return False


    async def delete_order(self, order_id: int) -> None:
        self.logger.debug('Executing delete_order')
        url = self.base_url + 'private/delete-order'
        payload = {
            'request_id': generate_request_id(),
            'order_id': order_id,
        }

        headers = self.get_signed_headers(payload)

        # Don't reject errors automatically because an 'Order not found' means it was already deleted, which is a success.
        response = await self.send_post_request_and_get_response(url, payload, headers, check_response_for_errors= False)

        if 'status' in response:
            if response['status'] == True:
                self.logger.debug('delete_order Succeeded')
            else:
                if response['status'] == False and response['error'] == 'Order not found':
                    self.logger.debug('delete_order Succeeded - order already deleted')
                else:
                    raise APIExecutionError('delete_order Failed. Response {}'.format(response))
        else:
            raise APIExecutionError('delete_order Failed. Response {}'.format(response))

    async def delete_all_orders(self, pair: str = None, buy_or_sell: int = None) -> None:
        # Made it async
        if pair is None:
            pair = self.default_pair
        self.logger.debug('Executing async_delete_all_orders for pair {}'.format(pair))

        #refresh our active orders
        active_orders = await self.get_active_orders()
        tasks = []
        for order in active_orders:
            if order['pair'] == pair:
                if buy_or_sell is not None:
                    if order['type'] == buy_or_sell:
                        tasks.append(asyncio.ensure_future(self.delete_order(order['id'])))
                else:
                    tasks.append(asyncio.ensure_future(self.delete_order(order['id'])))

        # Just async.wait all of the delete_orders directly
        if len(tasks) > 0:
            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


    async def get_ticker_list(self) -> List[Dict]:
        url = self.base_url + 'public/symbols'
        self.logger.debug('Executing get_ticker_list')
        params = {}
        response = await self.send_get_request_and_get_response(url, params)

        if 'data' not in response:
            raise APIResponseError('get_ticker_list failed. Response {}'.format(response))

        self.logger.debug('get_ticker_list Succeeded')
        return response['data']



    async def get_order_book(self, pair: str = None):
        if pair is None:
            pair = self.default_pair
        url = self.base_url + 'public/book'
        self.logger.debug('Executing get_order_book for pair {}'.format(pair))
        params = {
            'pair': pair,
        }
        response = await self.send_get_request_and_get_response(url, params)

        if 'data' not in response:
            self.logger.debug('get_order_book Failed. Response {}'.format(response))

        self.logger.debug('get_order_book Succeeded')
        return response['data']

    async def get_lowest_sell(self, pair: str = None, order_book: Dict = None) -> float:
        if pair is None:
            pair = self.default_pair

        if order_book is None:
            order_book = await self.get_order_book(pair)

        sell_prices = [to_decimal(x['rate']) for x in order_book['sell']]
        sell_prices.sort()

        if len(sell_prices) == 0:
            raise APIExecutionError("We were unable to get the lowest sell because there are no sell orders")

        return sell_prices[0]

    async def get_highest_buy(self, pair: str = None, order_book: Dict = None) -> float:
        if pair is None:
            pair = self.default_pair

        if order_book is None:
            order_book = await self.get_order_book(pair)

        buy_prices = [to_decimal(x['rate']) for x in order_book['buy']]
        buy_prices.sort()

        if len(buy_prices) == 0:
            raise APIExecutionError("We were unable to get the highest buy because there are no buy orders")

        return buy_prices[-1]

    async def get_lowest_sell_and_highest_buy(self, pair: str = None, order_book: Dict = None) -> Tuple[Optional[float], Optional[float]]:
        if pair is None:
            pair = self.default_pair

        if order_book is None:
            order_book = await self.get_order_book(pair)

        try:
            highest_buy = await self.get_highest_buy(pair, order_book)
        except APIExecutionError:
            highest_buy = None

        try:
            lowest_sell = await self.get_lowest_sell(pair, order_book)
        except APIExecutionError:
            lowest_sell = None

        if highest_buy is None and lowest_sell is None:
            raise APIExecutionError("We were unable to get the highest buy and lowest sell because there are no orders")

        return lowest_sell, highest_buy




