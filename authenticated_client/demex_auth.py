from tradehub.demex_client import DemexClient
from tradehub.authenticated_client import AuthenticatedClient
from tradehub.wallet import Wallet

def main():
    mnemonic='ENTER YOUR MNEMONIC HERE FOR CONNECTION TO DEMEX EXCHANGE'
    dem_client = DemexClient(mnemonic= mnemonic,
                network='mainnet',
                trusted_ips=None,
                trusted_uris=['http://175.41.151.35:5001', 'http://54.255.5.46:5001'])
    return dem_client
