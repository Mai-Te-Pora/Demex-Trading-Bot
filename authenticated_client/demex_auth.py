from tradehub.demex_client import DemexClient
from tradehub.authenticated_client import AuthenticatedClient
from tradehub.public_account_client import PublicClient
from tradehub.wallet import Wallet

mnemonic='ENTER YOUR MNEMONIC HERE FOR CONNECTION TO TRADEHUB'

def dem_client():
    dem_client = DemexClient(mnemonic= mnemonic,
                network='mainnet',
                trusted_ips=None,
                trusted_uris=['http://175.41.151.35:5001', 'http://54.255.5.46:5001'])
    return dem_client

def auth_client():
    ac = AuthenticatedClient(network='mainnet',
                    wallet=Wallet(mnemonic=mnemonic, network='mainnet'),
                    trusted_ips=None,
                    trusted_uris=["http://54.255.5.46:5001", "http://175.41.151.35:5001"])
    return ac

def p_client():
    pc = PublicClient(network='mainnet', trusted_uris=["http://54.255.5.46:5001", "http://175.41.151.35:5001"])
    return pc
