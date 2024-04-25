import requests
import json
from web3 import Web3
from tronapi import Tron
import tron_base58ToHex as ToHex

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
    return result # latest transaction comes last

def get_tron_transactions(address):
    address = ToHex.base58_to_hex(address)
    url =  f'https://api.trongrid.io/v1/accounts/{address}/transactions'
    headers = {'accept': "application/json"}
    response = requests.get(url, headers=headers)
    transactions = response.json()
    result = []
    for transaction in transactions['data']: # Assuming 'data' is the key containing the transactions
        if transaction['raw_data']['contract'][0]['parameter']['value']['owner_address'].lower() == address.lower():
            result.append({
                "type" : "outgoing",
                'amount' : int(transaction['raw_data']['contract'][0]['parameter']['value']['amount'])/1000000,
                'to'  : transaction['raw_data']['contract'][0]['parameter']['value']['to_address']
            })
        else:
            result.append({
                "type" : "incoming",
                'amount' : int(transaction['raw_data']['contract'][0]['parameter']['value']['amount'])/1000000,
                "from" : transaction['raw_data']['contract'][0]['parameter']['value']['owner_address']
            })

    return result # latest transaction comes first

def get_usdt_transactions(address):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20?&contract_address=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&only_confirmed=true&limit=25"
    headers = {"accept": "application/json"}
    res = requests.get(url, headers=headers)
    transactions = res.json()
    result = []
    for transaction in transactions['data']: # Assuming 'data' is the key containing the transactions
        if transaction['to'].lower() == address.lower():
            result.append({
                "type": "incoming",
                'amount': int(transaction['value'])/1000000, # Assuming 'value' is the amount in the smallest unit
                "from": transaction['from']
            })
        else:
            result.append({
                "type": "outgoing",
                'amount': int(transaction['value'])/1000000, # Assuming 'value' is the amount in the smallest unit
                'to': transaction['to']
            })


    return result # latest transaction comes first

def get_solana_transactions(address):
    url = "https://api.mainnet-beta.solana.com"
    endpoint = "/api/v1/account/{}/transactions".format(address)
    response = requests.get(url + endpoint)
    transactions = []

    # Check if the response status code is successful (200)
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            transactions = response.json().get('result', [])
            print(transactions)
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode JSON response.")
    else:
        print(f"Error: Request failed with status code {response.status_code}.")

    # Filter transactions based on the address
    incoming = []
    outgoing = []
    for tx in transactions:
        if tx['memo']:
            # This is a simple way to check if the transaction is incoming or outgoing
            # based on the memo. Adjust this logic based on your specific requirements.
            if tx['memo'].startswith("Incoming"):
                incoming.append(tx)
            elif tx['memo'].startswith("Outgoing"):
                outgoing.append(tx)
    print("Incoming Transactions:")
    for tx in incoming:
        print(tx)

    print("\nOutgoing Transactions:")
    for tx in outgoing:
        print(tx)

# Example usage
bitcoin_address = "bc1pnn6yf00yk0x6ju9zrz6m59gykj2l3m07llvjnyg7970m4etvss5sp0hm4s"
ethereum_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
tron_address = 'TDvmd3jyLK8mBdvTJZpCdTJBL2Pod2c8Jt'
solana_address = "6cm4vNugtBYGeDJrXYnNC2uGPgVeYBtKQLzPW8HwvFVA"

# print(get_bitcoin_transactions(bitcoin_address))
# print(get_ethereum_transactions('0x7D788Fdc21CB6545310e9Ec7b45Da268070D7Dd5'))
# print(get_tron_transactions(tron_address))
print(get_solana_transactions(solana_address))
# print(get_usdt_transactions('tron_address'))