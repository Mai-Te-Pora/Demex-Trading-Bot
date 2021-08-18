import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def save_swth_usdc_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/swth_usdc_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_swth_busd_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/swth_busd_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_swth_eth_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/swth_eth_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_eth_usdc_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/eth_usdc_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_cel_usdc_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/cel_usdc_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_cel_eth_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/cel_eth_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_eth_wbtc_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/eth_wbtc_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_wbtc_usdc_orderbook(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/orderbooks/wbtc_usdc_orderbook.json', 'w') as fout:
        json.dump(books , fout)

def save_wallet_balances(balances):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/balances/balances.json', 'w') as fout:
        json.dump(balances , fout)

def save_wallet_orders(orders):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/addressOrders/orders.json', 'w') as fout:
        json.dump(orders , fout)

def save_trades(order):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/trades/trades.json', 'w') as fout:
        json.update(order , fout)

def save_market_stats(books):
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(p + '/data_processing/storage/marketStats/market_stats.json', 'w') as fout:
        json.dump(books , fout)
