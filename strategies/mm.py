#The Treway bot analysis will attempt to find an imbalance between three specific
# trading pairs -- swth-usdc, eth-usdc, swth-eth (if imbalance exists in favor of more swth---execute trades [see also - authenticated_client folder])
import json
import itertools
import asyncio
import time

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authenticated_client import demex_auth
from data_processing import SavingRecords


class Treway:
    def __init__(self):
        self.balances = []
        self.swth_usdc_orderbook = []
        self.swth_eth_orderbook = []
        self.eth_usdc_orderbook = []

        self.usdc_max_quantity = 210

        self.swth_min_quantity_extra = 180
        self.eth_min_quantity_extra = .0025
        self.dem_client = demex_auth.main()

    def analyze_records(self):
        loop = 0
        p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #Read data in data_processing--storage
        try:
            with open( p + r"/data_processing/storage/orderbooks/swth_usdc_orderbook.json", "r") as read_file:
                self.swth_usdc_orderbook = json.load(read_file)
            with open(p + r"/data_processing/storage/orderbooks/swth_eth_orderbook.json", "r") as read_file:
                self.swth_eth_orderbook = json.load(read_file)
            with open(p + r"./data_processing/storage/orderbooks/eth_usdc_orderbook.json", "r") as read_file:
                self.eth_usdc_orderbook = json.load(read_file)
            with open(p + r"./data_processing/storage/balances/balances.json", "r") as read_file:
                self.balances = json.load(read_file)
        except:
            #For whatever reason the documents failed to load. Did you run DemexWebsocketClass.py for a minute or two before
            #beginning the trading bot? Please see assistance from github/c1im4cu5
            print("Failed to pull data. See Treway.py - def analyze_records")

            if loop < 4:
                time.sleep(5)
                self.analyze_records()
                loop += 1
            else:
                print("Stopping Attempts at Connection")

    def swth_usdc_data(self):

        buys = []
        sells = []
        for i in range(len(self.swth_usdc_orderbook)):
            if self.swth_usdc_orderbook[i]['side'] == 'buy':
                buys.append([self.swth_usdc_orderbook[i]['price'], self.swth_usdc_orderbook[i]['quantity']])
            elif self.swth_usdc_orderbook[i]['side'] == 'sell':
                sells.append([self.swth_usdc_orderbook[i]['price'], self.swth_usdc_orderbook[i]['quantity']])

        #Sorting Buy orders for ease of quantity and price access
        buys = [k for k, g in itertools.groupby(sorted(buys))]

        #Sorting Sell orders for ease of quantity and price access
        sells = [k for k, g in itertools.groupby(sorted(sells))]

        first_price_sell = sells[0][0]
        second_price_sell = sells[1][0]

        first_quantity_sell = sells[0][1]
        second_quantity_sell = sells[1][1]

        first_price_buy = buys[-1][0]
        second_price_buy = buys[-2][0]

        first_quantity_buy = buys[-1][-1]
        second_quantity_buy = buys[-2][-1]

        return first_price_sell, second_price_sell, first_quantity_sell, second_quantity_sell, first_price_buy, second_price_buy, first_quantity_buy, second_quantity_buy

    def eth_usdc_data(self):

        buys = []
        sells = []
        for i in range(len(self.eth_usdc_orderbook)):
            if self.eth_usdc_orderbook[i]['side'] == 'buy':
                buys.append([self.eth_usdc_orderbook[i]['price'], self.eth_usdc_orderbook[i]['quantity']])
            elif self.eth_usdc_orderbook[i]['side'] == 'sell':
                sells.append([self.eth_usdc_orderbook[i]['price'], self.eth_usdc_orderbook[i]['quantity']])

        #Sorting Buy orders for ease of quantity and price access
        buys = [k for k, g in itertools.groupby(sorted(buys))]

        #Sorting Sell orders for ease of quantity and price access
        sells = [k for k, g in itertools.groupby(sorted(sells))]

        first_price_sell = sells[0][0]
        second_price_sell = sells[1][0]

        first_quantity_sell = sells[0][1]
        second_quantity_sell = sells[1][1]

        first_price_buy = buys[-1][0]
        second_price_buy = buys[-2][0]

        first_quantity_buy = buys[-1][-1]
        second_quantity_buy = buys[-2][-1]

        return first_price_sell, second_price_sell, first_quantity_sell, second_quantity_sell, first_price_buy, second_price_buy, first_quantity_buy, second_quantity_buy

    def swth_eth_data(self):
        buys = []
        sells = []
        for i in range(len(self.swth_eth_orderbook)):
            if self.swth_eth_orderbook[i]['side'] == 'buy':
                buys.append([self.swth_eth_orderbook[i]['price'], self.swth_eth_orderbook[i]['quantity']])
            elif self.swth_eth_orderbook[i]['side'] == 'sell':
                sells.append([self.swth_eth_orderbook[i]['price'], self.swth_eth_orderbook[i]['quantity']])

        #Sorting Buy orders for ease of quantity and price access
        buys = [k for k, g in itertools.groupby(sorted(buys))]

        #Sorting Sell orders for ease of quantity and price access
        sells = [k for k, g in itertools.groupby(sorted(sells))]

        first_price_sell = sells[0][0]
        second_price_sell = sells[1][0]

        first_quantity_sell = sells[0][1]
        second_quantity_sell = sells[1][1]

        first_price_buy = buys[-1][0]
        second_price_buy = buys[-2][0]

        first_quantity_buy = buys[-1][-1]
        second_quantity_buy = buys[-2][-1]

        return first_price_sell, second_price_sell, first_quantity_sell, second_quantity_sell, first_price_buy, second_price_buy, first_quantity_buy, second_quantity_buy

    def main(self):
        #run def to pull specified records from storage
        self.pair = input("Please input a trading pair: ")

if __name__ == "__main__":
    objName = Treway().main()
