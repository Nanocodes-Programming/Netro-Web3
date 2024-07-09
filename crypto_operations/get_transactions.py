import requests
import json
from . import tron_base58ToHex as ToHex

def get_bitcoin_transactions(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full"
    response = requests.get(url)
    transactions = response.json().get('txs', [])
    result = []
    for tx in transactions:
        for output in tx['outputs']:
            if output['addresses'] is not None and address in output['addresses']:
                result.append({
                    "type": "Incoming",
                    "amount": int(output['value']) / 100000000,
                    # "address": output['addresses'][0]
                })
            elif output['addresses'] is not None:
                result.append({
                    "type": "Outgoing",
                    "amount": int(output['value']) / 100000000,
                    "address": output['addresses'][0]
                })
    return result  # latest transaction comes first
def get_ethereum_transactions(address):
    # Replace with the actual API endpoint and parameters for Ethereum block explorer
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=999999999999999999&sort=asc&apikey=CN7UWIVH6QGEPEIHZNUUUA1I8PNI1KQ4G9"
    response = requests.get(url)
    transactions = response.json().get('result', [])
    result = []
    for tx in transactions:
        if address.lower() ==tx['to'].lower() :
            result.append({
                "type" : "incoming",
                "hash": tx['hash'],
                "amount" : (int(tx['value'])/1000000000000000000), #wei to eth coversion
                "from": tx['from'],
            })

        elif tx['from'].lower() == address.lower():
            result.append({
                "type" : "outgoing",
                "hash": tx['hash'],
                "amount" : (int(tx['value'])/1000000000000000000),
                "to": tx['to']
            })
    return list(reversed(result)) # latest transaction comes first



def get_litecoin_transactions(address):
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full"
    response = requests.get(url)
    transactions = response.json().get('txs', [])
    result = []
    for tx in transactions:
        for output in tx['outputs']:
            if output['addresses'] is not None and address in output['addresses']:
                result.append({
                    "type": "Incoming",
                    "amount": int(output['value']) / 100000000,
                    # "address": output['addresses'][0]
                })
            elif output['addresses'] is not None:
                result.append({
                    "type": "Outgoing",
                    "amount": int(output['value']) / 100000000,
                    "address": output['addresses'][0]
                })
    return result #latest transactions first,


# # Example usage
# bitcoin_address = "bc1pnn6yf00yk0x6ju9zrz6m59gykj2l3m07llvjnyg7970m4etvss5sp0hm4s"
# ethereum_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

# solana_address = "AirDCHp6eyPyPxSazfVxhCREPDf2E9FrGn9d4wSbePwE"

# # print(get_bitcoin_transactions(bitcoin_address))
# print(get_ethereum_transactions('0x7D788Fdc21CB6545310e9Ec7b45Da268070D7Dd5'))

# print(get_solana_transactions(solana_address))
# # print(get_usdt_transactions('tron_address'))