import hashlib
import time

from eth_utils import to_bytes
from decimal import Decimal
from random import uniform
from random import randint
from random import choices

from atom_alter_API.constants import(
    NUM_DECIMALS,
    BUY,
    SELL
)


import random

def sha256(input_text):
    input_bytes = to_bytes(text=input_text)
    hash = hashlib.sha256(input_bytes).hexdigest()
    return hash

def get_random_buy_or_sell():
    return random.randint(0, 1)

def get_weighted_buy_or_sell(current_price, low_price_start_buying_more, low_price_no_more_sells):
    # if the price is below the low price threshold, it will return buy more often
    current_price = float(current_price)
    low_price_start_buying_more = float(low_price_start_buying_more)
    low_price_no_more_sells = float(low_price_no_more_sells)
    population = [BUY,SELL]
    if current_price >= low_price_start_buying_more:
        weights = [0.5,0.5]
    elif current_price < low_price_start_buying_more and current_price >= low_price_no_more_sells:
        prob_sell = (current_price-low_price_no_more_sells)/(low_price_start_buying_more-low_price_no_more_sells)
        prob_sell = 0.5*prob_sell
        weights = [1-prob_sell, prob_sell]
    else:
        weights = [1,0]

    return choices(population, weights)[0]

def generate_request_id():
    return randint(1000000000000,10000000000000)
    #return int(time.time()*1000)

def float_to_string(input):
    if isinstance(input, str):
        return input
    output = "{:.{}f}".format(input, NUM_DECIMALS)
    return output

def to_decimal(input):
    input_string = float_to_string(input)
    return Decimal(input_string)

def add_random_percentage(amount, max_percentage):
    amount = to_decimal(amount)
    percentage = uniform(-1*max_percentage, max_percentage)
    amount_change = amount*Decimal(percentage/100)
    return Decimal(amount+amount_change)

def scale_by_random_percentage(amount, max_percentage):
    amount = to_decimal(amount)
    percentage = uniform(0, max_percentage)
    scaled_amount = amount*Decimal(percentage/100)
    return Decimal(scaled_amount)

def calculate_order_amount_based_on_current_balance(initial_balance, current_balance, max_sold_per_day, num_orders):
    print('calculating calculate_order_amount_based_on_current_balance with parameters {} {} {} {}'.format(initial_balance, current_balance, max_sold_per_day, num_orders))
    if current_balance == 0:
        return Decimal(0)
    amount_sold = initial_balance - current_balance
    if amount_sold < 0:
        amount_sold = 0
    if num_orders < 1:
        raise Exception('num_orders in calculate_order_amount_based_on_current_balance cannot be less than 1. Something went wrong. num_orders = {}'.format(num_orders))

    # The goal is to use 5% of the allocated daily amount on each round of orders
    amount_left_to_sell = max_sold_per_day - amount_sold
    if amount_left_to_sell < 0:
        amount_left_to_sell = 0

    amount_for_all_orders = amount_left_to_sell*Decimal('0.05')
    amount_per_order = amount_for_all_orders/num_orders
    return Decimal(amount_per_order)

def satoshi_to_actual(satoshi):
    satoshi = to_decimal(satoshi)
    return Decimal(satoshi/Decimal('100000000'))


#
# Tests
#
def test_calculate_order_amount_based_on_current_balance():
    initial_balance = 1
    max_sold_per_day = 0.05
    num_orders = 10

    current_balance = initial_balance
    for i in range(100):
        new_order_amount = calculate_order_amount_based_on_current_balance(initial_balance, current_balance, max_sold_per_day, num_orders)
        current_balance -= new_order_amount*num_orders
        print("Placing {} orders for {}. Current balance is {}".format(num_orders, new_order_amount, current_balance))

    assert(current_balance > (initial_balance-max_sold_per_day))
#test_calculate_order_amount_based_on_current_balance()

#get_weighted_buy_or_sell(0.00008, 0.0001, 0.00005)