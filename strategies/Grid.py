import json
import itertools
import asyncio
import time
import ast
import tradehub.types as types

import os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authenticated_client import demex_auth
from data_processing import SavingRecords

slopes = {
        '3':[0.29,0.33,0.38],
        '4':[0.1,0.2,0.3,.4],
        '5':[0.1,0.15,0.2,0.25,0.3],
        '6':[0.1,0.125,0.15,0.175,0.2,0.25],
        '7':[0.035,0.07,0.105,0.14,0.175,0.22,0.255],
        '8':[0.02,0.05,0.08,0.11,0.13,0.17,0.21,0.23],
        '9':[0.03,0.05,0.07,0.08,0.1,0.12,0.15,0.18,0.22],
        '10':[0.01,0.02,0.04,0.06,0.09,0.11,0.13,0.16,0.18,0.2],
        '11':[0.01,0.02,0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.16,0.18],
        '12':[0.01,0.02,0.03,0.04,0.06,0.08,0.1,0.11,0.12,0.13,0.14,0.16],
        '13':[0.01,0.02,0.035,0.045,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.13],
        '14':[0.005,0.01,0.025,0.035,0.045,0.055,0.065,0.075,0.085,0.1,0.11,0.12,0.13,0.14],
        '15':[0.005,0.01,0.025,0.035,0.045,0.055,0.06,0.065,0.07,0.08,0.09,0.1,0.11,0.12,0.13],
        '16':[0.005,0.0075,0.0125,0.015,0.02,0.025,0.0275,0.0325,0.0375,0.045,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095,0.1]
        }

def save_potential_orders(orders):
    orders = orders
    #Open file for existing potential orders, add to orders and resave
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + r"/data_processing/logs/potential_orders.json", "r") as read_file:
        existing_orders = json.load(read_file)

    orders.extend(existing_orders)

    with open(p + '/data_processing/logs/potential_orders.json', 'w') as fout:
        json.dump(orders , fout)

def clean_potential_orders():
    orders = []
    #Open file for existing potential orders, add to orders and resave
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/logs/potential_orders.json', 'w') as fout:
        json.dump(orders , fout)

def clean_active_orders():
    orders = []
    #Open file for existing potential orders, add to orders and resave
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/logs/active_orders.json', 'w') as fout:
        json.dump(orders , fout)

def print_potential_orders():
    _rep = ""
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + r"/data_processing/logs/potential_orders.json", "r") as read_file:
        existing_orders = json.load(read_file)

    for i in range(len(existing_orders)):
        _rep += "=====================================================================\n"
        _rep += "Market: " + existing_orders[i]['pair'] + "\n"
        _rep += "Side: " + existing_orders[i]['side'] + "\n"
        _rep += "Buy Price: " + existing_orders[i]['buy_price'] + "\n"
        _rep += "Buy Quantity: " + existing_orders[i]['buy_quantity'] + "\n"
        _rep += "Sell Price: " + existing_orders[i]['sell_price'] + "\n"
        _rep += "Sell Quantity: " + existing_orders[i]['sell_quantity'] + "\n"
        _rep += "Profit: " + existing_orders[i]['profit'] + "\n"
        _rep += "=====================================================================\n\n"
    print(_rep)

def print_markets():
    _rep = ""
    markets = demex_auth.p_client().get_markets()

    for i in range(len(markets)):
        _rep += "=====================================================================\n"
        _rep += "Market: " + markets[i]['name'] + "\n"
        _rep += "Market Type: " + markets[i]['market_type'] + "\n"
        _rep += "Minimum Quantity: " + markets[i]['min_quantity'] + "\n"
        _rep += "Activity Status: " + str(markets[i]['is_active']) + "\n"
        _rep += "=====================================================================\n\n"
    print(_rep)

def print_active_orders():
    _rep = ""
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + r"/data_processing/logs/active_orders.json", "r") as read_file:
                orders = json.load(read_file)

    for i in range(len(orders)):
        _rep += "=====================================================================\n"
        _rep += "Market: " + orders[i]['pair'] + "\n"
        _rep += "Side: " + orders[i]['side'] + "\n"
        _rep += "Buy Price: " + orders[i]['buy_price'] + "\n"
        _rep += "Buy Quantity: " + orders[i]['buy_quantity'] + "\n"
        _rep += "Sell Price: " + orders[i]['sell_price'] + "\n"
        _rep += "Sell Quantity: " + orders[i]['sell_quantity'] + "\n"
        _rep += "Profit: " + orders[i]['profit'] + "\n"
        _rep += "Order ID: " + orders[i]['order_id'] + "\n"
        _rep += "=====================================================================\n\n"
    print(_rep)

def get_active_orders():
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + r"/data_processing/logs/potential_orders.json", "r") as read_file:
        existing_orders = json.load(read_file)
    return existing_orders

def question_hub():
    o_style =  input("Would you like to build manual or auto-generated orders (manual, auto, orders = print current orders, done = generate orders, so = start over): ")
    if o_style == "manual":
        user_parameters()
    elif o_style == 'auto':
        cascade_parameters()
    elif o_style == 'orders':
        print_potential_orders()
        question_hub()
    elif o_style == 'so':
        clean_potential_orders()
        question_hub()
        pass
    elif o_style == 'done':
        #BUILD ORDERS!!!
        print("READY TO BUILD ORDERS")
        pass

def load_markets():
    a = dem_client.get_market_stats()

def user_choices():
    pair = input("Trading pair (Ex: wbtc1_usdc1, eth1_usdc1, swth_usdc1): ")
    #order_type = input("Would you like to set parameters for a market or limit order (market or limit): ")
    order_type = 'limit'
    qty = float(input("Quantity (Ex: 0.055): "))
    side = input("Is this a buy or sell order (buy or sell): ")
    if side == 'buy':
        buy_price = input("Buy Price (Note: You cannot place an order over 100x last price.): ")
        sell_price = input("Sell Price: ")
    elif side == 'sell':
        sell_price = input("Sell Price: ")
        buy_price = input("Buy Price (Note: You cannot place an order 100x last price): ")
    profit = input("Profit Taking (base or quote): ")
    buy_price = float(buy_price)
    sell_price = float(sell_price)
    return pair, order_type, qty, side, buy_price, sell_price, profit

def user_order():
    pair, order_type, qty, side, buy_price, sell_price, profit= user_choices()
    order_id = ''
    status = 'open'

    if side == 'buy':
        if profit == "quote":
            qty = qty
            choices = {
                    'pair': pair,
                    'order_type': "limit",
                    'buy_quantity': str(qty),
                    'sell_quantity': str(qty),
                    'side': side,
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': profit,
                    'p_profit': "0",
                }

        elif profit == "base":
            buy_qty = qty
            sell_qty = (float(buy_qty) * float(buy_price)) / float(sell_price)
            choices = {
                    'pair': pair,
                    'order_type': "limit",
                    'buy_quantity': str(buy_qty),
                    'sell_quantity': str(sell_qty),
                    'side': side,
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': profit,
                    'p_profit': "0",
                }


    elif side == 'sell':
        if profit == "quote":
            qty = qty
            choices = {
                    'pair': pair,
                    'order_type': "limit",
                    'buy_quantity': str(qty),
                    'sell_quantity': str(qty),
                    'side': side,
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': profit,
                    'p_profit': "0",
                }

        elif profit == "base":
            sell_qty = qty
            buy_qty = (float(sell_qty) * float(buy_price)) / float(sell_price)
            choices = {
                    'pair': pair,
                    'order_type': "limit",
                    'buy_quantity': str(buy_qty),
                    'sell_quantity': str(sell_qty),
                    'side': side,
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': profit,
                    'p_profit': "0",
                    }

    return choices

def user_parameters():
    user_orders = []
    p = user_order()
    user_orders.append(p)
    more = input("Would you like to create another order (yes or no): ")
    while more == 'yes':
        p = user_order()
        user_orders.append(p)
        more = input("Would you like to create another order (yes or no): ")
    save_potential_orders(user_orders)
    question_hub()

def cascade_parameters():
    cascade_orders = []
    p = cascade_choices()
    b = auto_build_orders(p)
    more = input("Would you like to create another order set (yes or no): ")
    while more == 'yes':
        p = cascade_choices()
        b = auto_build_orders(p)
        more = input("Would you like to create another order set (yes or no): ")
    question_hub()


def cascade_choices():
    pair = input("Trading pair (Ex: wbtc1_usdc1, eth1_usdc1): ")
    side = input("Would you like to build buy or sell orders (buy/sell): ")
    order_style = input("Would you like to use linear or cascade order creation (linear/cascade): ")
    total_quantity = input("Max quantity to use for order building: ")
    num_orders = input("Max number of orders to build (If cascade: Min=3, Max=16): ")
    start_price = input("Starting price for order build: ")
    p_spacing = input("Percentage for order spacing (Ex: 0.05): ")
    profit = input("Base or Quote profit taking (base/quote): ")
    p_profit = input("Percentage for profit (Ex: 0.075): ")

    order_options = {
                'pair': pair,
                'side': side,
                'order_style': order_style,
                'total_quantity': float(total_quantity),
                'num_orders': int(num_orders),
                'start_price': float(start_price),
                'p_spacing': float(p_spacing),
                'profit': profit,
                'p_profit': float(p_profit)
                }
    return order_options

def auto_build_orders(user_p):
    p = user_p
    existing_orders=[]

    status = 'open'
    order_id = ''
    orders = []
    count = 0
    slope_count = str(p['num_orders'])
    linear_qty = p['total_quantity']/p['num_orders']

    if p['side'] == 'buy':
        buy_price = p['start_price']
        sell_price = p['start_price']+(p['start_price']*p['p_profit'])
        if p['profit'] == "quote":
            while count < p['num_orders']:
                if p['order_style'] == "linear":
                    qty = linear_qty
                elif p['order_style'] == "cascade":
                    qty = round((p['total_quantity']*slopes[slope_count][count]), 5)
                count += 1
                choices = {
                    'pair': p['market'],
                    'order_type': "limit",
                    'buy_quantity': str(qty),
                    'sell_quantity': str(qty),
                    'side': p['side'],
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': p['profit'],
                    'p_profit': p['p_profit'],
                    }
                buy_price = buy_price-(buy_price*p['p_spacing'])
                sell_price = buy_price+(buy_price*p['p_profit'])
                orders.append(choices)

        elif p['profit'] == "base":
            while count < p['num_orders']:
                if p['order_style'] == "linear":
                    buy_qty = linear_qty
                    sell_qty = (float(buy_qty) * float(buy_price)) / float(sell_price)
                elif p['order_style'] == "cascade":
                    buy_qty = round((p['total_quantity']*slopes[slope_count][count]), 5)
                    sell_qty = (float(buy_qty) * float(buy_price)) / float(sell_price)
                count += 1
                choices = {
                    'pair': p['pair'],
                    'order_type': "limit",
                    'buy_quantity': str(buy_qty),
                    'sell_quantity': str(sell_qty),
                    'side': p['side'],
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': p['profit'],
                    'p_profit': p['p_profit'],
                    }
                buy_price = buy_price-(buy_price*p['p_spacing'])
                sell_price = buy_price+(buy_price*p['p_profit'])
                orders.append(choices)

    elif p['side'] == 'sell':
        sell_price = p['start_price']
        buy_price = p['start_price']-(p['start_price']*p['p_profit'])
        if p['profit'] == "quote":
            while count < p['num_orders']:
                if p['order_style'] == "linear":
                    qty = linear_qty
                elif p['order_style'] == "cascade":
                    qty = round((p['total_quantity']*slopes[slope_count][count]), 5)
                count += 1
                choices = {
                    'pair': p['pair'],
                    'order_type': "limit",
                    'buy_quantity': str(qty),
                    'sell_quantity': str(qty),
                    'side': p['side'],
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': p['profit'],
                    'p_profit': p['p_profit'],
                    }
                sell_price = sell_price+(sell_price*p['p_spacing'])
                buy_price = sell_price-(sell_price*p['p_profit'])
                orders.append(choices)

        elif p['profit'] == "base":
            while count < p['num_orders']:
                if p['order_style'] == "linear":
                    sell_qty = linear_qty
                    buy_qty = (float(sell_qty) * float(buy_price)) / float(sell_price)
                elif p['order_style'] == "cascade":
                    sell_qty = round((p['total_quantity']*slopes[slope_count][count]), 5)
                    buy_qty = (float(sell_qty) * float(buy_price)) / float(sell_price)
                count += 1
                choices = {
                    'pair': p['pair'],
                    'order_type': "limit",
                    'buy_quantity': str(buy_qty),
                    'sell_quantity': str(sell_qty),
                    'side': p['side'],
                    'buy_price': str(round(buy_price, 8)),
                    'sell_price': str(round(sell_price, 8)),
                    'order_id': order_id,
                    'status': status,
                    'profit': p['profit'],
                    'p_profit': p['p_profit'],
                    }
                sell_price = sell_price+(sell_price*p['p_spacing'])
                buy_price = sell_price-(sell_price*p['p_profit'])
                orders.append(choices)

    #Open file for existing potential orders, add to orders and resave
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + r"/data_processing/logs/potential_orders.json", "r") as read_file:
        existing_orders = json.load(read_file)

    orders.extend(existing_orders)

    with open(p + '/data_processing/logs/potential_orders.json', 'w') as fout:
        json.dump(orders , fout)

    print("Orders Built for Review")

def create_limit_orders(orders):
    orders = orders

    dem_client = demex_auth.auth_client()

    #Iterate over order list of dict orders
    for i in range(len(orders)):
        #Check if user input limit orders
        if orders[i]['order_type'] == 'limit':
            #If yes to limit, is it a buy order
            if orders[i]['side'] == 'buy':
                m = orders[i]['pair']
                q = orders[i]['buy_quantity']
                p = orders[i]['buy_price']
                ord = dem_client.create_order(message=types.CreateOrderMessage(market= str(m),
                                                      side="buy",
                                                      quantity= str(q),
                                                         price= str(p),
                                                         type="limit"))
                time.sleep(1)

                #Iterate over received dict for txnHash
                for k,v in ord.items():
                    if k == 'logs':
                        for a in range(len(v)):
                            for b, c in v[a].items():
                                if b == 'log':
                                    c = json.loads(c)
                                    orders[i]['order_id'] = c['order']['order_id']

            elif orders[i]['side'] == 'sell':
                m = orders[i]['pair']
                q = str(orders[i]['sell_quantity'])
                p = str(orders[i]['sell_price'])
                ord = dem_client.create_order(message=types.CreateOrderMessage(market=  str(m),
                                                    side="sell",
                                                    quantity= str(q),
                                                    price= str(p),
                                                    type="limit"))
                time.sleep(1)

                #Iterate over received dict for txnHash
                for k,v in ord.items():
                    if k == 'logs':
                        for a in range(len(v)):
                            for b, c in v[a].items():
                                if b == 'log':
                                    c = json.loads(c)
                                    orders[i]['order_id'] = c['order']['order_id']

    print("Orders Generated")
    return orders

def monitor_limit_orders(records):
    records = records
    orders = []
    new_order = {}
    _rep = ""

    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #Read data in data_processing--storage
    try:
        with open( p + "/data_processing/logs/active_orders.json", "r") as read_file:
            orders = json.load(read_file)
    except:
        print("Unable to open active_orders.json file")
        sys.exit()

    if 'orders' in records['channel']:
        for i in range(len(records['result'])):
            for z in range(len(orders)):
                if records['result'][i]['order_id'] == orders[z]['order_id']:
                    if records['result'][i]['order_status'] == 'filled':
                        _rep += "=====================================================================\n"
                        _rep += "Order Id: " + orders[z]['order_id'] + " - Status = FILLED\n"
                        _rep += "+++++++++ Generating New Order ++++++++++++\n"
                        _rep += "=====================================================================\n\n"
                        print(_rep)
                        new_order = process_closed_order(orders[z])
                        del orders[z]
                        orders.append(new_order)
                    else:
                        pass

    SavingRecords.save_active_orders(orders)

def process_closed_order(order):
    order = order
    ord_price = ''
    closed_orders = []
    new_order = {}

    order_id = ''
    status = 'open'

    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #Check if existing orders in closed_orders.json in logs folder
    try:
        with open( p + "/data_processing/logs/closed_orders.json", "r") as read_file:
            closed_orders = json.load(read_file)
    except:
        print("There are no closed orders in the logs file.")

    if order['side'] == 'buy':
        new_order = {'pair': order['pair'],
                        'order_type': 'limit',
                        'buy_quantity': order['buy_quantity'],
                        'sell_quantity': order['sell_quantity'],
                        'side': 'sell',
                        'buy_price': order['buy_price'],
                        'sell_price': order['sell_price'],
                        'order_id': '',
                        'status': 'open',
                        'profit': order['profit'],
                        'p_profit': order['p_profit']
                        }
        closed_orders.append(order)

    elif order['side'] == 'sell':
        new_order = {'pair': order['pair'],
                        'order_type': 'limit',
                        'buy_quantity': order['buy_quantity'],
                        'sell_quantity': order['sell_quantity'],
                        'side': 'buy',
                        'buy_price': order['buy_price'],
                        'sell_price': order['sell_price'],
                        'order_id': '',
                        'status': 'open',
                        'profit': order['profit'],
                        'p_profit': order['p_profit']
                        }
        closed_orders.append(order)

    #Saved closed orders to logs folder
    try:
        with open(p + '/data_processing/logs/closed_orders.json', 'w') as fout:
            json.dump(closed_orders , fout)
        print("Saved closed orders to logs file")
    except:
        print("FAILED TO SAVE CLOSED ORDERS")

    if new_order['side'] == 'buy':
        ord_price = new_order['buy_price']
        ord_price = str(ord_price)
        q = str(new_order['buy_quantity'])
    elif new_order['side'] == 'sell':
        ord_price = new_order['sell_price']
        ord_price = str(ord_price)
        q = str(new_order['sell_quantity'])

    m = new_order['pair']
    s = new_order['side']
    q = str(q)

    #Create new order
    ord = dem_client.create_order(message=types.CreateOrderMessage(market= m,
                                            side =s,
                                            quantity = q,
                                            price= ord_price,
                                            type="limit"))

    #Iterate over received dict for txnHash
    for k,v in ord.items():
        if k == 'logs':
            for a in range(len(v)):
                for b, c in v[a].items():
                    if b == 'log':
                        c = json.loads(c)
                        new_order['order_id'] = c['order']['order_id']
                        print("Created New Order for  " + new_order['pair'] + " - " + "Order ID: " + new_order['order_id'])
    return new_order
