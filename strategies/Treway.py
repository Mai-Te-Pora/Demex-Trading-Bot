import pandas as pd
import json
import itertools
import asyncio
import time

import os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authenticated_client import demex_auth
from data_processing import SavingRecords

loop = 0
balances = []
swth_usdc_orderbook = []
swth_eth_orderbook = []
eth_usdc_orderbook = []
eth_wbtc_orderbook = []
wbtc_usdc_orderbook = []

usdc_max_quantity = 400
wbtc_max_quantity = 0.01
swth_max_quantity = 50000
eth_max_quantity = 0.125

swth_min_quantity_extra = 180
eth_min_quantity_extra = 0.00025

dem_client = demex_auth.auth_client()

logger = logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def analyze_wbtc(wbtc_max_quantity, over):
    wbtc_max_quantity = wbtc_max_quantity
    over = over

    with open(p + r"/data_processing/storage/orderbooks/eth_usdc_orderbook.json", "r") as read_file:
        eth_usdc_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/eth_wbtc_orderbook.json", "r") as read_file:
        eth_wbtc_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/wbtc_usdc_orderbook.json", "r") as read_file:
        wbtc_usdc_orderbook = pd.read_json(read_file)

    eth_usdc_orderbook['total'] = eth_usdc_orderbook['quantity'] * eth_usdc_orderbook['price']
    eth_wbtc_orderbook['total'] = eth_wbtc_orderbook['quantity'] * eth_wbtc_orderbook['price']
    wbtc_usdc_orderbook['total'] = wbtc_usdc_orderbook['quantity'] * wbtc_usdc_orderbook['price']

    #Checking WBTC-USDC (sell), ETH-USDC (Buy), ETH-WBTC (Sell) balance
    #WBTC-USDC
    logger.info("Starting WBTC-USDC, ETH-USDC, ETH-WBTC Imbalance Check")
    logger.info("Starting WBTC Qty: " + str(wbtc_max_quantity))
    hold_qty = wbtc_max_quantity
    hold_price = 0
    paid_percentage = .0025
    df = wbtc_usdc_orderbook.loc[(wbtc_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            hold_price += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            #Document prices for next order
            hold_price += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    usdc_paid = hold_price*paid_percentage
    total = hold_price-usdc_paid
    wbtc_usdc_received = total

    logger.info("Received USDC Qty: " + str(wbtc_usdc_received))

    #ETH-USDC
    hold_qty = wbtc_usdc_received
    new_hold_qty = 0
    hold_price = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
            hold_price += df.iloc[position]['total']
        elif df.iloc[position]['total'] > hold_qty:
            #Document prices for next order
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_price += hold_qty
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_usdc_received = total

    logger.info("Received ETH Qty: " + str(eth_usdc_received))

    #ETH-WBTC
    hold_qty = eth_usdc_received
    hold_price = 0
    df = eth_wbtc_orderbook.loc[(eth_wbtc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            hold_price += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            #Document prices for next order
            hold_price += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    wbtc_paid = hold_price*paid_percentage
    total = hold_price-wbtc_paid
    eth_wbtc_received = total

    logger.info("End Result WBTC Qty: " + str(eth_wbtc_received))

    if (eth_wbtc_received-wbtc_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_sell(pair='wbtc1_usdc1', quantity=str(wbtc_max_quantity))
        dem_client.market_buy(pair='eth1_usdc1', quantity=str(wbtc_usdc_received))
        dem_client.market_sell(pair='eth1_wbtc1', quantity=str(eth_usdc_received))
    else:
        logger.info("No Trades Recommended")
    #Checking ETH-WBTC (sell), ETH-USDC (Sell), WBTC-USDC (Buy) balance
    #WBTC-USDC
    logger.info("Starting ETH-WBTC, ETH-USDC, WBTC-USDC Imbalance Check")
    logger.info("Starting WBTC Qty: " + str(wbtc_max_quantity))
    hold_qty = wbtc_max_quantity
    new_hold_qty = 0
    hold_price = 0
    df = eth_wbtc_orderbook.loc[(eth_wbtc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
            #hold_price += df.iloc[position]['total']
        elif df.iloc[position]['total'] > hold_qty:
            #Document prices for next order
            new_hold_qty += hold_qty/df.iloc[position]['price']
            #hold_price += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_wbtc_received = total
    logger.info("Received ETH Qty: " + str(eth_wbtc_received))

    #ETH-USDC
    hold_qty = eth_wbtc_received
    new_hold_qty = 0
    hold_price = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            #Document prices for next order
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_usdc_received = total
    logger.info("Received USDC Qty: " + str(eth_usdc_received))

    #WBTC-USDC
    hold_qty = eth_usdc_received
    new_hold_qty = 0
    hold_price = 0
    df = wbtc_usdc_orderbook.loc[(wbtc_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            #Document prices for next order
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    wbtc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-wbtc_paid
    wbtc_usdc_received = total
    logger.info("Received WBTC Qty: " + str(wbtc_usdc_received))

    if (wbtc_usdc_received - wbtc_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_buy(pair='eth1_wbtc1', quantity=str(wbtc_max_quantity))
        dem_client.market_sell(pair='eth1_usdc1', quantity=str(eth_wbtc_received))
        dem_client.market_buy(pair='wbtc1_usdc1', quantity=str(eth_usdc_received))
    else:
        logger.info("No Trades Recommended")

def analyze_swth(swth_max_quantity, over):
    swth_max_quantity = swth_max_quantity
    over = over

    with open( p + r"/data_processing/storage/orderbooks/swth_usdc_orderbook.json", "r") as read_file:
        swth_usdc_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/swth_eth_orderbook.json", "r") as read_file:
        swth_eth_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/eth_usdc_orderbook.json", "r") as read_file:
        eth_usdc_orderbook = pd.read_json(read_file)

    swth_usdc_orderbook['total'] = swth_usdc_orderbook['quantity'] * swth_usdc_orderbook['price']
    swth_eth_orderbook['total'] = swth_eth_orderbook['quantity'] * swth_eth_orderbook['price']
    eth_usdc_orderbook['total'] = eth_usdc_orderbook['quantity'] * eth_usdc_orderbook['price']

    #Checking SWTH-USDC (Sell), ETH-USDC (Buy), SWTH-ETH (Buy)
    #SWTH-USDC
    logger.info("Starting SWTH-USDC, ETH-USDC, SWTH-ETH Imbalance Check")
    logger.info("Starting SWTH Qty: " + str(swth_max_quantity))
    hold_qty = swth_max_quantity
    new_hold_qty = 0
    paid_percentage = 0.0025
    paid_qty = 0
    df = swth_usdc_orderbook.loc[(swth_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    usdc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-usdc_paid
    swth_usdc_received = total

    logger.info("Received USDC Qty: " + str(swth_usdc_received))

    #ETH-USDC
    hold_qty = swth_usdc_received
    new_hold_qty = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_usdc_received = total

    logger.info("Received ETH Qty: " + str(eth_usdc_received))

    #SWTH-ETH
    hold_qty = eth_usdc_received
    new_hold_qty = 0
    df = swth_eth_orderbook.loc[(swth_eth_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    swth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-swth_paid
    swth_eth_received = total

    logger.info("Received SWTH Qty: " + str(swth_eth_received))

    if (swth_eth_received - swth_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_sell(pair='swth_usdc1', quantity=str(swth_max_quantity))
        dem_client.market_buy(pair='eth1_usdc1', quantity=str(swth_usdc_received))
        dem_client.market_buy(pair='swth_eth1', quantity=str(eth_usdc_received))
    else:
        logger.info("No Trades Recommended")

    #Checking SWTH-ETH, ETH-USDC, SWTH-USDC
    #SWTH-ETH
    logger.info("Starting SWTH-ETH, ETH-USDC, SWTH-USDC Imbalance Check")
    logger.info("Starting SWTH Qty: " + str(swth_max_quantity))
    hold_qty = swth_max_quantity
    new_hold_qty = 0
    df = swth_eth_orderbook.loc[(swth_eth_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    swth_eth_received = total

    logger.info("Received ETH Qty: " + str(swth_eth_received))

    #ETH-USDC
    hold_qty = swth_eth_received
    new_hold_qty = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    usdc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-usdc_paid
    eth_usdc_received = total

    logger.info("Received USDC Qty: " + str(eth_usdc_received))

    #SWTH-USDC
    hold_qty = eth_usdc_received
    new_hold_qty = 0
    df = swth_usdc_orderbook.loc[(swth_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    swth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-swth_paid
    swth_usdc_received = total

    logger.info("Received USDC Qty: " + str(swth_usdc_received))

    if (swth_usdc_received - swth_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_sell(pair='swth_eth1', quantity=str(swth_max_quantity))
        dem_client.market_sell(pair='eth1_usdc1', quantity=str(swth_eth_received))
        dem_client.market_buy(pair='swth_usdc1', quantity=str(eth_usdc_received))
    else:
        logger.info("No Trades Recommended")

def analyze_eth(eth_max_quantity, over):
    eth_max_quantity = eth_max_quantity
    over = over

    with open( p + r"/data_processing/storage/orderbooks/wbtc_usdc_orderbook.json", "r") as read_file:
        wbtc_usdc_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/eth_usdc_orderbook.json", "r") as read_file:
        eth_usdc_orderbook = pd.read_json(read_file)
    with open(p + r"/data_processing/storage/orderbooks/eth_wbtc_orderbook.json", "r") as read_file:
        eth_wbtc_orderbook = pd.read_json(read_file)

    wbtc_usdc_orderbook['total'] = wbtc_usdc_orderbook['quantity'] * wbtc_usdc_orderbook['price']
    eth_wbtc_orderbook['total'] = eth_wbtc_orderbook['quantity'] * eth_wbtc_orderbook['price']
    eth_usdc_orderbook['total'] = eth_usdc_orderbook['quantity'] * eth_usdc_orderbook['price']

    #Checking ETH-WBTC (Sell), WBTC-USDC(Sell), ETH-USDC(Buy)
    #ETH-WBTC
    logger.info("Starting ETH-WBTC, WBTC-USDC, ETH-USDC Imbalance Check")
    logger.info("Starting ETH Qty: " + str(eth_max_quantity))
    hold_qty = eth_max_quantity
    new_hold_qty = 0
    paid_percentage = 0.0025
    df = eth_wbtc_orderbook.loc[(eth_wbtc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    wbtc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-wbtc_paid
    eth_wbtc_received = total

    logger.info("Received WBTC Qty: " + str(eth_wbtc_received))

    hold_qty = eth_wbtc_received
    new_hold_qty = 0
    df = wbtc_usdc_orderbook.loc[(wbtc_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    usdc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-usdc_paid
    wbtc_usdc_received = total

    logger.info("Received WBTC Qty: " + str(wbtc_usdc_received))

    hold_qty = wbtc_usdc_received
    new_hold_qty = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_usdc_received = total

    logger.info("Received ETH Qty: " + str(eth_usdc_received))

    if (eth_usdc_received - eth_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_sell(pair='eth1_wbtc1', quantity=str(eth_max_quantity))
        dem_client.market_sell(pair='wbtc1_usdc1', quantity=str(eth_wbtc_received))
        dem_client.market_buy(pair='eth1_usdc1', quantity=str(wbtc_usdc_received))
    else:
        logger.info("No Trades Recommended")

    #Checking ETH-USDC (Sell), WBTC-USDC(Buy), ETH-WBTC(Buy)
    #ETH-USDC
    logger.info("Starting ETH-USDC, WBTC-USDC, ETH-WBTC Imbalance Check")
    logger.info("Starting ETH Qty: " + str(eth_max_quantity))
    hold_qty = eth_max_quantity
    new_hold_qty = 0
    df = eth_usdc_orderbook.loc[(eth_usdc_orderbook['side'] == 'buy')]
    df = df.sort_values(by='price', ascending=False)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['quantity'] <= hold_qty:
            hold_qty -= df.iloc[position]['quantity']
            new_hold_qty += df.iloc[position]['total']
        elif df.iloc[position]['quantity'] > hold_qty:
            new_hold_qty += hold_qty*df.iloc[position]['price']
            hold_qty = 0
        position += 1
    usdc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-usdc_paid
    eth_usdc_received = total

    logger.info("Received USDC Qty: " + str(eth_usdc_received))

    #WBTC-USDC
    hold_qty = eth_usdc_received
    new_hold_qty = 0
    df = wbtc_usdc_orderbook.loc[(wbtc_usdc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    wbtc_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-wbtc_paid
    wbtc_usdc_received = total

    logger.info("Received WBTC Qty: " + str(wbtc_usdc_received))

    #ETH-WBTC
    hold_qty = wbtc_usdc_received
    new_hold_qty = 0
    df = eth_wbtc_orderbook.loc[(eth_wbtc_orderbook['side'] == 'sell')]
    df = df.sort_values(by='price', ascending=True)
    position = 0
    while hold_qty > 0:
        if df.iloc[position]['total'] <= hold_qty:
            hold_qty -= df.iloc[position]['total']
            new_hold_qty += df.iloc[position]['quantity']
        elif df.iloc[position]['total'] > hold_qty:
            new_hold_qty += hold_qty/df.iloc[position]['price']
            hold_qty = 0
        position += 1
    eth_paid = new_hold_qty*paid_percentage
    total = new_hold_qty-eth_paid
    eth_wbtc_received = total

    logger.info("Received ETH Qty: " + str(eth_wbtc_received))

    if (eth_wbtc_received - eth_max_quantity) > over:
        logger.info("Trades Recommended")
        logger.info("Performing Recommended Trades")
        dem_client.market_sell(pair='eth1_usdc1', quantity=str(eth_max_quantity))
        dem_client.market_buy(pair='wbtc1_usdc1', quantity=str(eth_usdc_received))
        dem_client.market_buy(pair='eth1_wbtc1', quantity=str(wbtc_usdc_received))
    else:
        logger.info("No Trades Recommended")
