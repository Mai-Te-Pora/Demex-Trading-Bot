#The Treway bot analysis will attempt to find an imbalance between three specific
# trading pairs -- swth-usdc, eth-usdc, swth-eth (if imbalance exists in favor of more swth---execute trades [see also - authenticated_client folder])
import json
import itertools
import asyncio
import time

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
import db

from authenticated_client import demex_auth
from data_processing import SavingRecords


class Treway:
    def __init__(self):
        self.balances = []
        self.cel_usdc_orderbook = []
        self.cel_eth_orderbook = []
        self.eth_usdc_orderbook = []

        self.usdc_max_quantity = 150

        self.cel_min_quantity_extra = 200
        self.eth_min_quantity_extra = .0025
        self.dem_client = demex_auth.main()

    def analyze_records(self):
        loop = 0
        #Read data in data_processing--storage
        try:
            with open(r"./data_processing/storage/orderbooks/cel_usdc_orderbook.json", "r") as read_file:
                self.cel_usdc_orderbook = json.load(read_file)
            with open(r"./data_processing/storage/orderbooks/cel_eth_orderbook.json", "r") as read_file:
                self.cel_eth_orderbook = json.load(read_file)
            with open(r"./data_processing/storage/orderbooks/eth_usdc_orderbook.json", "r") as read_file:
                self.eth_usdc_orderbook = json.load(read_file)
            with open(r"./data_processing/storage/balances/balances.json", "r") as read_file:
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

    def cel_usdc_data(self):

        buys = []
        sells = []
        for i in range(len(self.cel_usdc_orderbook)):
            if self.cel_usdc_orderbook[i]['side'] == 'buy':
                buys.append([self.cel_usdc_orderbook[i]['price'], self.cel_usdc_orderbook[i]['quantity']])
            elif self.cel_usdc_orderbook[i]['side'] == 'sell':
                sells.append([self.cel_usdc_orderbook[i]['price'], self.cel_usdc_orderbook[i]['quantity']])

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

    def cel_eth_data(self):
        buys = []
        sells = []
        for i in range(len(self.cel_eth_orderbook)):
            if self.cel_eth_orderbook[i]['side'] == 'buy':
                buys.append([self.cel_eth_orderbook[i]['price'], self.cel_eth_orderbook[i]['quantity']])
            elif self.cel_eth_orderbook[i]['side'] == 'sell':
                sells.append([self.cel_eth_orderbook[i]['price'], self.cel_eth_orderbook[i]['quantity']])

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
        self.analyze_records()

        ce_fps, ce_sps, ce_fqs, ce_sqs, ce_fpb, ce_spb, ce_fqb, ce_sqb = self.swth_eth_data()
        cu_fps, cu_sps, cu_fqs, cu_sqs, cu_fpb, cu_spb, cu_fqb, cu_sqb = self.swth_usdc_data()
        eu_fps, eu_sps, eu_fqs, eu_sqs, eu_fpb, eu_spb, eu_fqb, eu_sqb = self.eth_usdc_data()

        cu_max_buy_quantity_p1 = round(self.usdc_max_quantity/cu_fps, 2)
        cu_max_sell_quantity_p1 = round(self.usdc_max_quantity/cu_fpb, 2)

        cu_max_buy_quantity_p1 = round(self.usdc_max_quantity/cu_fps, 2)
        cu_max_sell_quantity_p1 = round(self.usdc_max_quantity/cu_fpb, 2)

        eu_max_buy_quantity = round(self.usdc_max_quantity/eu_sps, 3)
        eu_max_sell_quantity = round(self.usdc_max_quantity/eu_spb, 3)

        se_max_buy_quantity = round(self.usdc_max_quantity*se_fps)
        se_max_sell_quantity = round(self.usdc_max_quantity*se_fpb)

        #Prices paid for paying and selling into asks/bids to acquire more swth (sell into swth_usdc, buy into eth_usdc, buy into swth_eth)
        usdc_one = round(su_max_sell_quantity*su_fpb, 2)
        eu_qty = round(usdc_one/eu_sps, 3)
        total = round(eu_qty/se_fps)

        if (total - su_max_sell_quantity) >= self.swth_min_quantity_extra:
            print("Trade Recommended (swth_usdc, eth_usdc, swth_eth)")
            self.dem_client.market_sell(pair='swth_usdc1', quantity=str(su_max_sell_quantity))
            self.dem_client.market_buy(pair='eth1_usdc1', quantity=str(eu_qty))
            self.dem_client.market_buy(pair='swth_eth1', quantity=str(total))
            print("Trades Performed: Check Demex Log")
            print("Sleeping for ten minutes before restarting.")
            time.sleep(600)
            self.main()
        else:
            print("NO Trade Recommended (swth_usdc, eth_usdc, swth_eth)")

        #Prices paid for paying and selling into asks/bids to acquire more swth (sell eth_usdc, buy swth_usdc, sell swth_eth )
        usdc_one = round(eu_max_sell_quantity*eu_spb, 2)
        su_qty = round(usdc_one/su_fps)
        total = round(su_qty*se_fpb, 3)
        total_buy = round(su_qty/se_fpb)


        if (eu_max_sell_quantity - su_qty) >= self.eth_min_quantity_extra:
            print("Trade Recommended (eth_usdc, swth_usdc, swth_eth)")
            self.dem_client.market_sell(pair='eth1_usdc1', quantity=str(eu_max_sell_quantity))
            self.dem_client.market_buy(pair='swth_usdc1', quantity=str(su_qty))
            self.dem_client.market_sell(pair='swth_eth1', quantity=str(su_qty))
            print("Trades Performed: Check Demex Log")
            print("Sleeping for ten minutes before restarting.")
            time.sleep(600)
            self.main()
        else:
            print("NO Trade Recommended (eth_usdc, swth_usdc, swth_eth)")

        #Prices paid for paying and selling into asks/bids to acquire more swth (swth_eth, eth_usdc, swth_usdc)
        eu_qty = round(su_max_sell_quantity*se_fpb, 3)
        usdc_one = round(eu_qty*eu_spb)
        total = round(usdc_one/su_fps)


        if (total - su_max_sell_quantity) >= self.eth_min_quantity_extra:
            print("Trade Recommended (swth_eth, eth_usdc, swth_usdc)")
            self.dem_client.market_sell(pair='swth_eth1', quantity=str(su_max_sell_quantity))
            self.dem_client.market_sell(pair='eth1_usdc1', quantity=str(eu_qty))
            self.dem_client.market_buy(pair='swth_usdc1', quantity=str(total))
            print("Trades Performed: Check Demex Log")
            print("Sleeping for ten minutes before restarting.")
            time.sleep(600)
            self.main()
        else:
            print("NO Trade Recommended (swth_eth, eth_usdc, swth_usdc)")
        #print('{0:.10f}'.format(se_fpb))

        print("No Trades to Perform. Sleeping for two minutes.")
        time.sleep(120)
        self.main()

if __name__ == "__main__":
    objName = Treway().main()
