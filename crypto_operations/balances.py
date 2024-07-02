# Import necessary libraries
import requests
import os
from web3 import Web3
import blockcypher
from moneywagon import AddressBalance
from tronpy import Tron
from tronpy.providers import HTTPProvider

# Function to get the balance of a Bitcoin address
def balance_BTC(addr : str):
    try:
        # Use the blockcypher library to get the total balance of the BTC address
        total = blockcypher.get_total_balance(addr)
        return total
    except:
        # If blockcypher fails, use the moneywagon library as a fallback
        total = AddressBalance().action('btc', addr)
        return total

# Function to get the balance of an Ethereum address
def balance_ETH(addr : str):
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/4f32e758e9ae4046ba13e6a4b00a2e88'))
    ethereum_address = addr
    balance_wei = web3.eth.get_balance(ethereum_address)
    result1 = web3.from_wei(balance_wei, 'ether')
    return result1

# Function to get the balance of a Litecoin address
def balance_LTC(addy):
    # Fetch balance data from BlockCypher API
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{addy}/balance')
    if response.status_code != 200:
        if response.status_code == 400:
            print("Invalid LTC address.")
        else:
            print(f"Failed to retrieve balance. Error {response.status_code}. Please try again later.")
        return

    data = response.json()
    balance = data['balance'] / 10 ** 8
    return balance



def USDT_balance( address: str):
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
    precision = contract.functions.decimals()
    return contract.functions.balanceOf(address) / 10 ** precision
