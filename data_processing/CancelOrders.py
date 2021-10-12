import json
import os, sys
import tradehub.types as types
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from authenticated_client import demex_auth


def cancel_active_orders():
    ac = demex_auth.auth_client()
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open( p + "/data_processing/logs/active_orders.json", "r") as read_file:
        orders = json.load(read_file)

    for i in range(len(orders)):
        ac.cancel_order(message=types.CancelOrderMessage(id=orders[i]['order_id']))
        time.sleep(1)
