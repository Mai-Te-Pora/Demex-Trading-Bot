def balances(records):
    balance_dict = {}
    if 'channel' in records:
        if 'balances' in records['channel']:
            if balance_dict:
                pass
            else:
                try:
                    balance_dict = records['result']
                except:
                    print("Balance = Zero for All Tokens")
    return balance_dict

def market_stats(records):
    market_stats = {}
    if 'market_stats' in records['channel']:
        market_stats = records['result']

    return market_stats

def orders(records):
    orders_dict = {}
    if 'orders' in records['channel']:
        if orders_dict:
            orders_dict = records['result']
        else:
            try:
                orders_dict = records['result']
            except:
                print("No Active Orders")

    return orders_dict

def swth_usdc_book (records):
    swth_usdc_orderbook = {}
    if 'books.swth_usdc1' in records['channel']:
        swth_usdc_orderbook = records['result']

    return swth_usdc_orderbook

def swth_busd_book(records):
    swth_busd_orderbook = {}
    if 'books.swth_busd1' in records['channel']:
        swth_busd_orderbook = records['result']

    return swth_busd_orderbook

def eth_usdc_book(records):
    eth_usdc_orderbook = {}
    if 'books.eth1_usdc1' in records['channel']:
        eth_usdc_orderbook = records['result']

    return eth_usdc_orderbook

def swth_eth_book (records):
    swth_eth_orderbook = {}
    if 'books.swth_eth1' in records['channel']:
        #self.swth_eth_orderbook.update({key:[item[key] for item in records['result']] for key in records['result'][0].keys()})
        swth_eth_orderbook = records['result']

    return swth_eth_orderbook

def cel_eth_book (records):
    cel_eth_orderbook = {}
    if 'books.cel_eth' in records['channel']:
        #self.swth_eth_orderbook.update({key:[item[key] for item in records['result']] for key in records['result'][0].keys()})
        cel_eth_orderbook = records['result']

    return cel_eth_orderbook

def cel_usdc_book (records):
    cel_usdc_orderbook = {}
    if 'books.cel1_usdc1' in records['channel']:
        #self.swth_eth_orderbook.update({key:[item[key] for item in records['result']] for key in records['result'][0].keys()})
        cel_usdc_orderbook = records['result']

    return cel_usdc_orderbook

def wbtc_usdc_book (records):
    wbtc_usdc_orderbook = {}
    if 'books.wbtc1_usdc1' in records['channel']:
        #self.swth_eth_orderbook.update({key:[item[key] for item in records['result']] for key in records['result'][0].keys()})
        wbtc_usdc_orderbook = records['result']

    return wbtc_usdc_orderbook

def eth_wbtc_book (records):
    eth_wbtc_orderbook = {}
    if 'books.eth1_wbtc1' in records['channel']:
        #self.swth_eth_orderbook.update({key:[item[key] for item in records['result']] for key in records['result'][0].keys()})
        eth_wbtc_orderbook = records['result']

    return eth_wbtc_orderbook
