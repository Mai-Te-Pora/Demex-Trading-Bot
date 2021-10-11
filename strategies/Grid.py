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


class GridBot(object):
    def __init__(self):
        self.loop = 0
        self.dem_client = demex_auth.auth_client()

        #Setting up logger
        self.root = logging.getLogger()
        self.root.setLevel(logging.INFO)
        #Setting handler, formatting text for print on terminal
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.root.addHandler(self.handler)

    def __call__():
        self.main()

    def load_markets(self):
        a = self.dem_client.get_market_stats()

        for i in range(len(a)):
            print("Market: " + a[i]['market'] + " - " + "Type: " + a[i]['market_type'] + " - " + "Last Price: " + a[i]['last_price'])

    def user_choices(self):
        pair = input("Trading pair (Ex: wbtc1_usdc1, eth1_usdc1, swth_usdc1): ")
        #order_type = input("Would you like to set parameters for a market or limit order (market or limit): ")
        order_type = 'limit'
        qty = float(input("Quantity: "))
        side = input("Is this a buy or sell order (buy or sell): ")
        if side == 'buy':
            buy_price = input("Buy Price (Note: You cannot place an order over 100x last price. [See notes on Maitepora about orderbook or contact c1im4cu5 on github]): ")
            buy_price = str(buy_price)
            sell_price = input("Sell Price: ")
            sell_price = str(sell_price)
        elif side == 'sell':
            sell_price = input("Sell Price: ")
            sell_price = str(sell_price)
            buy_price = input("Buy Price (Note: You cannot place an order 100x. [See notes on Maitepora about orderbook or contact c1im4cu5 on github]): ")
            buy_price = str(buy_price)
        #profit = input("Profit in base token or quote token (base or quote): ")
        profit = 'base'
        return pair, order_type, qty, side, buy_price, sell_price, profit


    def user_order(self):
        pair, order_type, qty, side, buy_price, sell_price, profit= self.user_choices()
        order_id = ''
        status = 'open'
        choices = {
                'pair': pair,
                'order_type': order_type,
                'quantity': qty,
                'side': side,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'order_id': order_id,
                'status': status,
                'profit': profit,
        }
        return choices

    def user_parameters(self):
        self.load_markets()
        user_orders = []
        p = self.user_order()
        user_orders.append(p)
        more = input("Would you like to create another order (yes or no): ")
        while more == 'yes':
            p = self.user_order()
            user_orders.append(p)
            more = input("Would you like to create another order (yes or no): ")

        return user_orders

    def create_limit_orders(self):

        #Trigger user input and get parameters
        orders = self.user_parameters()

        #Iterate over order list of dict orders
        for i in range(len(orders)):
            #Check if user input limit orders
            if orders[i]['order_type'] == 'limit':
                #If yes to limit, is it a buy order
                if orders[i]['side'] == 'buy':
                    m = orders[i]['pair']
                    q = orders[i]['quantity']
                    p = orders[i]['buy_price']
                    ord = self.dem_client.create_order(message=types.CreateOrderMessage(market= str(m),
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
                    q = str(orders[i]['quantity'])
                    p = str(orders[i]['sell_price'])
                    ord = self.dem_client.create_order(message=types.CreateOrderMessage(market=  str(m),
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

    def create_new_orders(self, orders):
        orders = orders
        #Iterate over order list of dict orders
        for i in range(len(orders)):
            #Check if user input limit orders
            if orders[i]['order_type'] == 'limit':
                #If yes to limit, is it a buy order
                if orders[i]['side'] == 'buy':
                    m = orders[i]['pair']
                    q = orders[i]['quantity']
                    p = orders[i]['buy_price']
                    ord = self.dem_client.create_order(message=types.CreateOrderMessage(market= str(m),
                                                          side="buy",
                                                          quantity= str(q),
                                                          price= str(p),
                                                          type="limit"))

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
                    q = str(orders[i]['quantity'])
                    p = str(orders[i]['sell_price'])
                    ord = self.dem_client.create_order(message=types.CreateOrderMessage(market=  str(m),
                                                        side="sell",
                                                        quantity= str(q),
                                                        price= str(p),
                                                        type="limit"))

                    #Iterate over received dict for txnHash
                    for k,v in ord.items():
                        if k == 'logs':
                            for a in range(len(v)):
                                for b, c in v[a].items():
                                    if b == 'log':
                                        c = json.loads(c)
                                        orders[i]['order_id'] = c['order']['order_id']

        print("New Orders Generated")
        for i in orders:
            print(i)
        return orders

    def monitor_limit_orders(self, records):
        records = records
        orders = []
        new_order = {}

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
                            print("Order Id: " + orders[z]['order_id'] + " - Status = FILLED")
                            print("Generating New Order")
                            new_order = self.process_closed_order(orders[z])
                            del orders[z]
                            orders.append(new_order)
                        else:
                            pass

        SavingRecords.save_active_orders(orders)

    def process_closed_order(self, order):
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
            self.root.info("There are no closed orders in the logs file.")

        if order['side'] == 'buy':
            if order['profit'] == 'base':
                new_order = {'pair': order['pair'],
                                'order_type': 'limit',
                                'quantity': order['quantity'],
                                'side': 'sell',
                                'buy_price': order['buy_price'],
                                'sell_price': order['sell_price'],
                                'order_id': '',
                                'status': 'open',
                                'profit': order['profit'],
                                }
                closed_orders.append(order)

            elif order['profit'] == 'quote':
                quantity = (float(order['quantity']) * float(order['buy_price'])) / float(order['sell_price'])
                new_order = {'pair': order['pair'],
                                'order_type': 'limit',
                                'quantity': str(quantity),
                                'side': 'sell',
                                'buy_price': order['buy_price'],
                                'sell_price': order['sell_price'],
                                'order_id': '',
                                'status': 'open',
                                'profit': order['profit'],
                                }
                closed_orders.append(order)

        elif order['side'] == 'sell':
            if order['profit'] == 'base':
                new_order = {'pair': order['pair'],
                                'order_type': 'limit',
                                'quantity': order['quantity'],
                                'side': 'buy',
                                'buy_price': order['buy_price'],
                                'sell_price': order['sell_price'],
                                'order_id': '',
                                'status': 'open',
                                'profit': order['profit'],
                                }
                closed_orders.append(order)

            elif order['profit'] == 'quote':
                quantity = (float(order['quantity']) * float(order['buy_price'])) / float(order['sell_price'])
                new_order = {'pair': order['pair'],
                                'order_type': 'limit',
                                'quantity': str(quantity),
                                'side': 'buy',
                                'buy_price': str(order['buy_price']),
                                'sell_price': str(order['sell_price']),
                                'order_id': '',
                                'status': 'open',
                                'profit': order['profit'],
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
        elif new_order['side'] == 'sell':
            ord_price = new_order['sell_price']
            ord_price = str(ord_price)


        m = new_order['pair']
        s = new_order['side']
        q = new_order['quantity']
        q = str(q)

        #Create new order
        ord = self.dem_client.create_order(message=types.CreateOrderMessage(market= m,
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

    def main(self):
        orders = self.create_limit_orders()
        self.monitor_limit_orders(orders)

if __name__ == "__main__":
    objName = GridBot().main()
