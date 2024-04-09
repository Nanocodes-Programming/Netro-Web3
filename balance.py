import Accounts
import requests
import blockcypher
from moneywagon import AddressBalance

def balance_BTC(addr):
    try:
        total = blockcypher.get_total_balance(addr)
        print('BTC Balance is '+ str(total))
    except:
        total = AddressBalance().action('btc', addr)
        print('Balance of BTC is '+ str(total))
balance_BTC(Accounts.btc_address)

