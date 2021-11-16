from tradehub.demex_client import DemexClient
from tradehub.authenticated_client import AuthenticatedClient
from tradehub.public_account_client import PublicClient
from tradehub.wallet import Wallet

#Mnemonic should be entered in lowercase lettering
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

def rtn_address():
    w = Wallet(mnemonic= mnemonic,
       network='mainnet')

    pk = w.mnemonic_to_private_key(mnemonic_phrase=mnemonic)
    pub_k = w.private_key_to_public_key(private_key=pk)
    address = w.public_key_to_address(public_key= pub_k,
                                  hrp=None)
    return address
