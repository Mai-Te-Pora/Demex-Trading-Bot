from tradehub.websocket_client import DemexWebsocket
import asyncio
import json

import sys, os, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing import ReceivingRecords
from data_processing import CleaningRecords
from data_processing import SavingRecords
from data_processing import CancelOrders
from data_processing import *
from strategies import Treway
from strategies import Grid
from authenticated_client import demex_auth


balances = []
orders = []
hld = []
market_stats = []
swth_usdc = []
swth_busd = []
swth_eth = []
eth_usdc = []
cel_eth = []
cel_usdc = []
eth_wbtc = []
wbtc_usdc = []

wbtc_usdc_15_minute = []

#Setting up logger
root = logging.getLogger()
root.setLevel(logging.INFO)
#Setting handler, formatting text for print on terminal
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

address = demex_auth.rtn_address()

async def on_error():
    print("Websocket connection has been terminated")
    try:
        print("Canceling all active user orders")
        CancelOrders.cancel_active_orders()
        print("Orders Canceled. Please check Carbon (or Demex) for confirmation of cancelations.")
    except:
        print("Unable to cancel orders. Please check Carbon (or Demex) immediately!!!!!!!!!!!!")
        print("System exiting")
        sys.exit()

#On successful connection
async def on_connect():
    #candlestick granularity - allowed values: 1, 5, 15, 30, 60, 360, 1440
    return await demex.subscribe("Subscription", [
                                                f"market_stats.{'market_stats'}",
                                                #f"books.{'wbtc1_usdc1'}",
                                                #f"books.{'eth1_wbtc1'}",
                                                #f"books.{'cel_eth'}",
                                                #f"books.{'cel1_usdc1'}",
                                                #f"books.{'eth1_usdc1'}",
                                                #f"books.{'swth_usdc1'}",
                                                #f"books.{'swth_eth1'}",
                                                #f"books.{'swth_busd1'}",
                                                #f"candlesticks.{'swth_usdc1'}.{15}",
                                                #f"balances.{'ENTER YOUR WALLET ADDRESS HERE'}",
                                                f"orders.{address}"])

#Receiving feed from websocket
async def on_receive(records: dict):

    #Check if "Channel" is in records (Initial response will be missing "Channel")
    if 'channel' in records:

        #Wallet Token Balances
        if 'balances' in records['channel']:
            #Send data to balance def in ReceivingRecords
            balances = ReceivingRecords.balances(records)
            SavingRecords.save_wallet_balances(balances)

        #Wallet Orders
        #Check if orders in record
        if 'orders.' in records['channel']:
            Grid.monitor_limit_orders(records)
            print("Active Orders Updated")
            print("Websocket will stay active without printing status until next order update.")

        #Market Statistics
        if 'market_stats' in records['channel']:
            #Send data to market_stats def in ReceivingRecords
            market_stats = ReceivingRecords.market_stats(records)
            #Market stats is an overwriting data dump of info. There is no need to clean records
            #JSON file wil be overwritten with each new sequence update (Saves as dict of dicts) See storage file
            SavingRecords.save_market_stats(market_stats)

        #Orderbook receiving, saving and upkeep
        #Check if swth_usdc books are in the "channel"
        if 'books.swth_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            swth_usdc.extend(ReceivingRecords.swth_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(swth_usdc)
            #Send to function for saving file
            SavingRecords.save_swth_usdc_orderbook(swth_usdc)
        #Check if swth_eth books are in the "channel"
        if 'books.swth_eth1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            swth_eth.extend(ReceivingRecords.swth_eth_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(swth_eth)
            #Send to function for saving file
            SavingRecords.save_swth_eth_orderbook(swth_eth)
        #Check if swth_eth books are in the "channel"
        if 'books.eth1_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            eth_usdc.extend(ReceivingRecords.eth_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(eth_usdc)
            #Send to function for saving file
            SavingRecords.save_eth_usdc_orderbook(eth_usdc)
        #Check if eth_wbtc books are in the "channel"
        if 'books.eth1_wbtc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            eth_wbtc.extend(ReceivingRecords.eth_wbtc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(eth_wbtc)
            #Send to function for saving file
            SavingRecords.save_eth_wbtc_orderbook(eth_wbtc)
        #Check if wbtc_usdc books are in the "channel"
        if 'books.wbtc1_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            wbtc_usdc.extend(ReceivingRecords.wbtc_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(wbtc_usdc)
            #Send to function for saving file
            SavingRecords.save_wbtc_usdc_orderbook(wbtc_usdc)

async def bot_task():
    while True:
        Treway.analyze_eth("1.25", "0.0125")
        root.info("No trades to perform. Sleeping for two minutes.")
        await asyncio.sleep(120)

async def main():
    orders = []

    #Print any active orders (FOR EXPERIENCED USERS)
    Grid.print_active_orders()

    loading_user = input("Please ignore this request unless you are an experience user. The websocket will, at times, lose connection. Existing orders are stored in a json file at '/data_processing/logs/active_orders.json'. This file is a list of dicts. Users can freely adjust the parameters of this file, load them or just reload exisiting acitive orders. If you possessed active orders on file, they would have printed out above this message. If so, you can restart the bot to continue monitoring those orders.  Would you like to monitor old orders or generate new orders (old/new): ")
    if loading_user == 'new':
        Grid.print_markets()
        Grid.clean_potential_orders()
        Grid.clean_active_orders()
        loop = 0
        Grid.question_hub()
        orders = Grid.get_active_orders()
        orders = Grid.create_limit_orders(orders)
        SavingRecords.save_active_orders(orders)
        print("Orders Saved...proceeding with monitor status")
    elif loading_user == 'old':
        pass

    print("**************  Websocket will stay active with no activity in terminal  *********************")

    #Create Websocket asyncio task
    socket = asyncio.create_task(demex.connect(on_receive, on_connect))
    #Create Treway Bot task via bot_task function

    #Gather and run functions concurrently
    asyncio.gather(
                    asyncio.get_event_loop().run_until_complete(await socket)
                    #asyncio.get_event_loop().run_until_complete(await bot)
                    )

if __name__ == '__main__':
    demex: DemexWebsocket = DemexWebsocket('wss://ws.dem.exchange/ws')
    asyncio.run(main())
