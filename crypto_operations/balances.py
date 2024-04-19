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

# Function to get the balance of a Solana address
def balance_SOL(addr : str):
    # Set your Solana RPC URL
    solana_rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    # Prepare the JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [addr]
    }
    # Send the request
    response = requests.post(solana_rpc_url, json=payload)
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        if 'result' in result and 'value' in result['result']:
            # The balance is returned in lamports, convert to SOL
            balance_lamports = result['result']['value']
            balance_sol = balance_lamports / 1e9 # 1 SOL = 1e9 lamports
            return balance_sol
        else:
            print("Error: Unable to retrieve balance.")
            return None
    else:
        print(f"Error: Request failed with status code {response.status_code}.")
        return None

# Function to get the balance of a Tron address
def get_trx_balance(address : str):
    # Define the provider for the Tron network
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    # Initialize the Tron client with the provider
    client = Tron(provider=provider)
    # Get the account balance of the Tron address
    return float(client.get_account_balance(address))

def USDT_balance( address: str):
    provider = HTTPProvider(api_key='d4e77476-2ae9-426e-b3aa-0488b3667048')
    client = Tron(provider=provider)
    contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
    precision = contract.functions.decimals()
    return contract.functions.balanceOf(address) / 10 ** precision